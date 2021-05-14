"""Philips Somneo All V1"""
import asyncio
import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.discovery import load_platform
from homeassistant.const import TEMP_CELSIUS

from .const import *

_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    """Setup the Somneo component."""
    try:
        conf = config[DOMAIN]
        entity_id = DOMAIN + ".status"
        sensor_id = DOMAIN + ".sensors"
        name = conf.get(CONF_NAME, DEFAULT_NAME)
        host = conf.get(CONF_HOST, DEFAULT_HOST)
        #port_int = conf.get(CONF_PORT, DEFAULT_PORT)
        #port = str(port_int)
        sc_interval = conf.get(CONF_INTERVAL, DEFAULT_INTERVAL)
        scan_int = sc_interval.total_seconds()
        sens_url = 'https://' + host + '/di/v1/products/1/wusrd'
        light_url = 'https://' + host + '/di/v1/products/1/wulgt'
        sens = []
        for xsensor in conf.get(CONF_SENS):
            sens.append(xsensor)
        ### DATA_SETS ###
        host_data = {ATTR_C_NAME: name, ATTR_C_HOST: host, ATTR_C_SENS: sens, ATTR_C_INT: scan_int}
        sens_data = {ATTR_S_TEMP: None, ATTR_S_HUM: None, ATTR_S_LIGHT: None, ATTR_S_NOISE: None}
        light_data = {ATTR_L_ONOFF: None, ATTR_L_LTLVL: None, ATTR_L_CTYPE: None, ATTR_L_NGTLT: None}
        data = {"component": host_data, "sensors": sens_data, "light": light_data}
        hass.data[DATA_PSC] = host_data
        hass.data[DOMAIN] = data

        load_platform(hass, 'light', DOMAIN, {}, config)
        hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)

        
        hass.states.set(entity_id, "Active", data)
        #### NOTHING BELOW THIS LINE ####
        # If Success:
        _LOGGER.info("Somneo_V1 has been set up!")
        return True
    except Exception as ex:
        _LOGGER.error('Error while initializing Somneo, exception: {}'.format(str(ex)))
        hass.components.persistent_notification.create(
            f'Error: {str(ex)}<br />Fix issue and restart',
            title=NOTIFICATION_TITLE,
            notification_id=NOTIFICATION_ID)
        # If Fail:
        return False



