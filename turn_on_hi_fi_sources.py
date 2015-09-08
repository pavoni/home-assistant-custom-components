"""
custom_components.turn_on_hi_fi_sources
~~~~~~~~~~~~~~~~~~~~~~~~~

Example component to target an entity_id to:
 - turn it on at 7AM in the morning
 - turn it on if anyone comes home and it is off
 - turn it off if all lights are turned off
 - turn it off if all people leave the house
 - offer a service to turn it on for 10 seconds

Configuration:

To use the Example custom component you will need to add the following to
your config/configuration.yaml

example:
  target: TARGET_ENTITY

Variable:

target
*Required
TARGET_ENTITY should be one of your devices that can be turned on and off,
ie a light or a switch. Example value could be light.Ceiling or switch.AC
(if you have these devices with those names).
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

global_hass = 0
global_target1 = 0
global_target2 = 0
global_source = 0
global_maker = 0


def setup(hass, config):
    """ Setup example component. """
    global global_hass, global_target1, global_target2, global_source, global_maker
    global_hass = hass
    # Validate that all required config options are given

    if not validate_config(config, {DOMAIN: [CONF_TARGET1]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_TARGET2]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_SOURCE]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_MAKER]}, _LOGGER):
        return False

    global_target1 = config[DOMAIN][CONF_TARGET1]
    global_target2 = config[DOMAIN][CONF_TARGET2]

    # Validate that the target entity id exists
    if hass.states.get(global_target1) is None:
        _LOGGER.error("Target entity id %s does not exist", global_target1)

        # Tell the bootstrapper that we failed to initialize
        return False

    if hass.states.get(global_target2) is None:
        _LOGGER.error("Target entity id %s does not exist", global_target2)

        # Tell the bootstrapper that we failed to initialize
        return False

    global_source = config[DOMAIN][CONF_SOURCE]

    # Validate that the source entity ids exist
    if hass.states.get(global_source) is None:
        _LOGGER.error("Source entity id %s does not exist", global_source1)

        # Tell the bootstrapper that we failed to initialize
        return False

    global_maker = config[DOMAIN][CONF_MAKER]

    if hass.states.get(global_maker) is None:
        _LOGGER.error("Source entity id %s does not exist", global_source2)

        # Tell the bootstrapper that we failed to initialize
        return False

    def track_sources(entity_id, old_state, new_state):
        """ Fired when one of the sources state updates unit """
        # During startup states are uncertain - so don't do anything
        if (global_hass.states.get(global_maker).attributes.get('sensor_state', None) == None ):
            return
        systemline_on = global_hass.states.get(global_maker).attributes.get('sensor_state', 0) == 'on'
        pre_amp_on = global_hass.states.get(global_source).state == 'on'
        if systemline_on or pre_amp_on :
            if systemline_on :
                print('turn_on_hi_fi_sources: turn on for SYSTEMLINE')
                if not core.is_on(global_hass, global_target1):
                    core.turn_on(global_hass, global_target1)
            if pre_amp_on :
                print('turn_on_hi_fi_sources: turn on for MAIN HI FI')
                if not core.is_on(global_hass, global_target1):
                    core.turn_on(global_hass, global_target1)
                if not core.is_on(global_hass, global_target2):
                    core.turn_on(global_hass, global_target2)
            elif core.is_on(global_hass, global_target2):
                core.turn_off(global_hass, global_target2)

        else :
            print('turn_on_hi_fi_sources: turn off ALL')
            if core.is_on(global_hass, global_target1):
                core.turn_off(global_hass, global_target1)
            if core.is_on(global_hass, global_target2):
                core.turn_off(global_hass, global_target2)

    hass.states.track_change(global_source, track_sources)
    hass.states.track_change(global_maker, track_sources)

    # Tells the bootstrapper that the component was successfully initialized
    return True
