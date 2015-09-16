"""
custom_components.turn_on_hi_fi_sources

"""
import time
import logging

from homeassistant.const import STATE_HOME, STATE_NOT_HOME, STATE_ON, STATE_OFF
import homeassistant.loader as loader
from homeassistant.helpers import validate_config
import homeassistant.components as core

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

# Name of the service that we expose
SERVICE_FLASH = 'on'

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

    # Validate that the target entity id exists
    if hass.states.get(target1) is None:
        _LOGGER.error("Target entity id %s does not exist", target1)

        # Tell the bootstrapper that we failed to initialize
        return False

    if hass.states.get(target2) is None:
        _LOGGER.error("Target entity id %s does not exist", target2)

        # Tell the bootstrapper that we failed to initialize
        return False

    source = config[DOMAIN][CONF_SOURCE]

    # Validate that the source entity ids exist
    if hass.states.get(source) is None:
        _LOGGER.error("Source entity id %s does not exist", source)

        # Tell the bootstrapper that we failed to initialize
        return False

    maker = config[DOMAIN][CONF_MAKER]

    if hass.states.get(maker) is None:
        _LOGGER.error("Source entity id %s does not exist", maker)

        # Tell the bootstrapper that we failed to initialize
        return False

    def track_sources(entity_id, old_state, new_state):
        """ Fired when one of the sources state updates unit """
        # During startup states are uncertain - so don't do anything
        if (hass.states.get(maker).attributes.get('sensor_state', None) == None ):
            print('NOT INITIALISED')
            return
        systemline_on = hass.states.get(maker).attributes.get('sensor_state', 0) == 'on'
        pre_amp_on = hass.states.get(source).state == 'on' and (hass.states.get(source).attributes.get('today_mwh', None) != None )
        if systemline_on or pre_amp_on :
            if systemline_on :
                print('turn_on_hi_fi_sources: turn on for SYSTEMLINE')
                if not core.is_on(hass, target1):
                    core.turn_on(hass, target1)
            if pre_amp_on :
                print('turn_on_hi_fi_sources: turn on for MAIN HI FI')
                if not core.is_on(hass, target1):
                    core.turn_on(hass, target1)
                if not core.is_on(hass, target2):
                    core.turn_on(hass, target2)
            elif core.is_on(hass, target2):
                core.turn_off(hass, target2)

        else :
            print('turn_on_hi_fi_sources: turn off ALL')
            if core.is_on(hass, target1):
                core.turn_off(hass, target1)
            if core.is_on(hass, target2):
                core.turn_off(hass, target2)

    hass.states.track_change(source, track_sources)
    hass.states.track_change(maker, track_sources)

    # Tells the bootstrapper that the component was successfully initialized
    return True
