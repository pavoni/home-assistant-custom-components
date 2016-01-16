"""
custom_components.open_skylight_when_hot

"""
import time
import logging
from datetime import timedelta


from homeassistant.helpers import validate_config
import homeassistant.components as core
import homeassistant.util.dt as dt_util
from homeassistant.helpers.event import track_state_change

# The domain of your component. Should be equal to the name of your component
DOMAIN = "open_skylight_when_hot"

# List of component names (string) your component depends upon
# We depend on group because group will be loaded after all the components that
# initialize devices have been setup.
DEPENDENCIES = ['group']

# Configuration key for the entity id we are targetting
CONF_THERMOSTAT = 'thermostat'
CONF_SKYLIGHT = 'skylight'
CONF_OPEN = 'open_at'
CONF_CLOSE = 'close_at'

# Shortcut for the logger
_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    # Validate that all required config options are given
    if not validate_config(config, {DOMAIN: [CONF_THERMOSTAT]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_SKYLIGHT]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_OPEN]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_CLOSE]}, _LOGGER):
        return False

    thermostat = config[DOMAIN][CONF_THERMOSTAT]
    skylight = config[DOMAIN][CONF_SKYLIGHT]
    open_at = config[DOMAIN][CONF_OPEN]
    close_at = config[DOMAIN][CONF_CLOSE]

    def track_temperature(entity_id, old_state, new_state):
        """ Fired when one of the sources state updates unit """
        if not (hass.states.get(thermostat) and hass.states.get(skylight)):
            _LOGGER.warning('Components not initialised')
            return
        # if it's a thermostat this will work
        current = hass.states.get(thermostat).attributes.get('current_temperature', None)
        # if not try a sensor
        if current is None:
            current = hass.states.get(thermostat).state
        now = dt_util.now()
        start_window = now.replace( hour=8, minute=00)
        end_window  = now.replace( hour=23, minute=00)
        if (now > start_window and now < end_window):
            if current >= open_at and not core.is_on(hass, skylight):
                _LOGGER.warning('open skylight at {}'.format(current))
                core.turn_on(hass, skylight)
            elif current <= close_at and core.is_on(hass, skylight):
                _LOGGER.warning('close skylight at {}'.format(current))
                core.turn_off(hass, skylight)

    track_state_change(hass, thermostat, track_temperature)

    # Tells the bootstrapper that the component was successfully initialized
    return True
