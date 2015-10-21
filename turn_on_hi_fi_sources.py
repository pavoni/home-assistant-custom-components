"""
custom_components.turn_on_hi_fi_sources

"""
import time
import logging

from homeassistant.helpers import validate_config
import homeassistant.components as core
from homeassistant.helpers.event import track_state_change

# The domain of your component. Should be equal to the name of your component
DOMAIN = "turn_on_hi_fi_sources"

# List of component names (string) your component depends upon
# We depend on group because group will be loaded after all the components that
# initialize devices have been setup.
DEPENDENCIES = ['group']

# Configuration key for the entity id we are targetting
CONF_TARGET1 = 'target1'
CONF_TARGET2 = 'target2'

CONF_SOURCE = 'source'
CONF_MAKER = 'maker'

# Shortcut for the logger
_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    # Validate that all required config options are given
    if not validate_config(config, {DOMAIN: [CONF_TARGET1]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_TARGET2]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_SOURCE]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_MAKER]}, _LOGGER):
        return False

    target1 = config[DOMAIN][CONF_TARGET1]
    target2 = config[DOMAIN][CONF_TARGET2]
    source = config[DOMAIN][CONF_SOURCE]
    maker = config[DOMAIN][CONF_MAKER]

    def track_sources(entity_id, old_state, new_state):
        """ Fired when one of the sources state updates unit """
        if not (hass.states.get(maker) and hass.states.get(source)):
            _LOGGER.warning('Source components not initialised')
            return
        # During startup states are uncertain - so don't do anything
        if (hass.states.get(maker).attributes.get('sensor_state', None) == None ):
            _LOGGER.warning('Systemline switch not initialised')
            return
        systemline_on = hass.states.get(maker).attributes.get('sensor_state', 0) == 'on'
        pre_amp_on = hass.states.get(source).state == 'on' and (hass.states.get(source).attributes.get('current_power_mwh', None) != None )
        if systemline_on or pre_amp_on :
            if systemline_on :
                if not core.is_on(hass, target1):
                    _LOGGER.warning('turn on for SYSTEMLINE')
                    core.turn_on(hass, target1)
            if pre_amp_on :
                if not core.is_on(hass, target1):
                    core.turn_on(hass, target1)
                if not core.is_on(hass, target2):
                    _LOGGER.warning('turn on for MAIN HI FI')
                    core.turn_on(hass, target2)
            elif core.is_on(hass, target2):
                core.turn_off(hass, target2)

        else :
            if core.is_on(hass, target1):
                _LOGGER.warning('turn off all')
                core.turn_off(hass, target1)
            if core.is_on(hass, target2):
                core.turn_off(hass, target2)

    track_state_change(hass, source, track_sources)
    track_state_change(hass, maker, track_sources)

    # Tells the bootstrapper that the component was successfully initialized
    return True
