"""Platform for sensor integration."""
from datetime import timedelta
import logging
import urllib3
import requests
urllib3.disable_warnings()

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

from .const import *

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Somneo sensor platform."""
    somneo_data = hass.data[DATA_PSC]
    host = somneo_data[ATTR_C_HOST]
    port = somneo_data[ATTR_C_PORT]
    sc_int = somneo_data[ATTR_C_INT]
    sensor_url = 'https://' + host + ':' + str(port) + '/di/v1/products/1/wusrd'
    data = SomneoData(sensor_url)
    dev = []
    for sensor in somneo_data[ATTR_C_SENS]:
        dev.append(SomneoSensor(data, sensor))
    add_entities(dev, True)

class SomneoSensor(Entity):
    """Representation of a Sensor."""
    def __init__(self, data, sensor_types):
        """Initialize the sensor."""
        self.data = data
        self._name = (PREFIX + SENSOR_TYPES[sensor_types][0])
        self._unit_of_measurement = SENSOR_TYPES[sensor_types][1]
        self.type = sensor_types
        self._state = None
    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state
    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._unit_of_measurement
    def update(self):
        """Get the latest data and updates the states."""
        self.data.update()
        if self.type == "temperature":
            self._state = self.data.temperature
        if self.type == "humidity":
            self._state = self.data.humidity
        if self.type == "light":
            self._state = self.data.light
        if self.type == "noise":
            self._state = self.data.noise

class SomneoData:
    """Get the latest data and update."""
    def __init__(self, url):
        """Initialize the data object."""
        self.temperature = None
        self.humidity = None
        self.light = None
        self.noise = None
        self.url = url
        #scan_int = sc_int

    def get_sensor_data(self):
        sensor_data_update = {'mslux': None, 'mstmp': None, 'msrhu': None, 'mssnd': None, 'avlux': None, 'avtmp': None, 'avhum': None, 'avsnd': None, 'enscr': None}
        r = requests.get(self.url, verify=False, timeout=30, stream=True)
        if r.status_code == 200:
            r_data = r.json()
            for key, value in r_data.items():
                sensor_data_update[key] = value
        return sensor_data_update

    @Throttle(DEFAULT_INTERVAL)
    def update(self):
        """Get the latest data from Somneo."""
        sensor_data = self.get_sensor_data()
        self.temperature = sensor_data['mstmp']
        self.humidity = sensor_data['msrhu']
        self.light = sensor_data['mslux']
        self.noise = sensor_data['mssnd']




