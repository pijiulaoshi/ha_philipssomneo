import voluptuous as vol
from datetime import timedelta

from homeassistant.helpers import config_validation as cv
from homeassistant.const import (TEMP_CELSIUS, PERCENTAGE)
DOMAIN = 'philips_somneo'
PREFIX = 'somneo_'
DATA_SOMNEO = 'data_somneo'
DATA_PSC = 'PSC'
VERSION = "0.2"

DEFAULT_NAME = "somneo"
DEFAULT_HOST = "192.168.2.131"
DEFAULT_PORT = 443
DEFAULT_CTYPE = "3"
DEFAULT_INTERVAL = timedelta(seconds=60)

CONF_NAME = 'name'
CONF_HOST = 'host'
CONF_PORT = 'port'
CONF_SENS = 'sensors'
CONF_INTERVAL = 'scan_interval'

CONF_CTYPE = "ctype"
MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)
#SCAN_INTERVAL = timedelta(seconds=60)


SENSOR_TYPES = {
    "temperature": ["temperature", TEMP_CELSIUS],
    "humidity": ["humidity", PERCENTAGE],
    "light": ["light", "lux"],
    "noise": ["noise", "db"]
}

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_INTERVAL): cv.int,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
        vol.Optional(CONF_SENS, default=list(SENSOR_TYPES)): [vol.In(SENSOR_TYPES)],
    })
}, extra=vol.ALLOW_EXTRA)


NOTIFICATION_ID = "somneosensor_notification"
NOTIFICATION_TITLE = "SomneoSensor Setup"

ATTR_C_NAME = "name"
ATTR_C_HOST = "host"
ATTR_C_PORT = "port"
ATTR_C_SENS = "sensors"
ATTR_C_SURL = "sensor_url"
ATTR_C_LURL = "light_url"

ATTR_S_TEMP = "temperature"
ATTR_S_HUM = "humidity"
ATTR_S_LIGHT = "light"
ATTR_S_NOISE = "noise"

ATTR_L_ONOFF = "state"
ATTR_L_LTLVL = "intensity"
ATTR_L_CTYPE = "light_type"
ATTR_L_NGTLT = "night_light"


#ENTITY_ID_FORMAT = DOMAIN + ".{}"
#SOMNEO_COMPONENTS = ["sensor", "light"]




