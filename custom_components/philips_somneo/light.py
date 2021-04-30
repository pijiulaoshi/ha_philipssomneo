"""Platform for light integration."""
import logging
import requests

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
# Import the device class from the component that you want to support
from homeassistant.components.light import (PLATFORM_SCHEMA, LightEntity)

from .const import *

_LOGGER = logging.getLogger(__name__)

TIMEOUT = 5.0
CONNFAILCOUNT = 5


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Somneo Light platform."""
    somneo_data = hass.data[DATA_PSC]
    host = somneo_data['host']
    port = somneo_data['port']
    name = somneo_data['name']
    url = 'https://' + host + ':' + port + '/di/v1/products/1/wulgt'
    ctype = 3
    ltlvl = 15
    add_entities([SomneoLight(name, url, ctype, ltlvl)])


class SomneoLight(LightEntity):
    """Representation of an Somneo Light."""

    def __init__(self, name, url, ctype, ltlvl):
        """Initialize an SomneoLight."""
        self._name = name
        self._state = None
        self._intensity = ltlvl
        self._colortype = ctype
        self.url = url
        self._connfail = 0
        self._session = requests.Session()

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name
    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state
    @property
    def should_poll(self):
        return False


    def turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        payload_on = {"ltlvl":15,"onoff":True,"tempy":False,"ctype":3,"ngtlt":False,"wucrv":[],"pwmon":False,"pwmvs":[0,0,0,0,0,0],"diman":0}
        self._putReq(payload_on)
        self._state = True
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        payload_off = {"ltlvl":15,"onoff":False,"tempy":False,"ctype":3,"ngtlt":False,"wucrv":[],"pwmon":False,"pwmvs":[0,0,0,0,0,0],"diman":0}
        self._putReq(payload_off)
        self._state = False
        self.schedule_update_ha_state()

### Needs work -> use _getReq()
    def get_light_data(url):
        light_data_update = {'ltlvl': None, 'onoff': None, 'tempy': None, 'ctype': None, 'ngtlt': None, 'wucrv': None, 'pwmon': None, 'pwmvs': None, 'diman': None}
        r = requests.get(url, verify=False, timeout=TIMEOUT)
        if r.status_code == 200:
            r_data = r.json()
            for key, value in r_data.items():
                light_data_update[key] = value
        return light_data_update


    def update(self):
        """Fetch new state data for this light."""
        light_data = self.get_light_data(self.url)
        self._state = light_data['onoff']
        

    def _getReq(self):
        try:
            if self._connfail:
                self._connfail -= 1
                return None
            resp = self._session.get(self.url, verify=False, timeout=TIMEOUT)
            self.on = True
            return json.loads(resp.text)
        except requests.exceptions.RequestException as err:
            self._connfail = CONNFAILCOUNT
            self.on = False
            return None

    def _putReq(self, data):
        try:
            if self._connfail:
                self._connfail -= 1
                return False
            resp = self._session.put(self.url, json=data, verify=False, timeout=TIMEOUT)
            self.on = True
            if resp.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException as err:
            self._connfail = CONNFAILCOUNT
            self.on = False
            return False
