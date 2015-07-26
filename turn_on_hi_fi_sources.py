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
CONF_TARGET = 'target'

CONF_SOURCE1 = 'source1'
CONF_SOURCE1_MW = 'source1_mw'
CONF_SOURCE2 = 'source2'
CONF_SOURCE2_MW = 'source2_mw'

# Name of the service that we expose
SERVICE_FLASH = 'on'

# Shortcut for the logger
_LOGGER = logging.getLogger(__name__)

global_hass = 0
global_target = 0
global_source1 = 0
global_source2 = 0
global_source1_mw = 0
global_source2_mw = 0


def setup(hass, config):
    """ Setup example component. """
    global global_hass, global_target, global_source1, global_source2, global_source1_mw, global_source2_mw
    global_hass = hass
    # Validate that all required config options are given
    if not validate_config(config, {DOMAIN: [CONF_TARGET]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_SOURCE1]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_SOURCE2]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_SOURCE1_MW]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_SOURCE2_MW]}, _LOGGER):
        return False

    global_target = config[DOMAIN][CONF_TARGET]

    # Validate that the target entity id exists
    if hass.states.get(global_target) is None:
        _LOGGER.error("Target entity id %s does not exist", global_target)

        # Tell the bootstrapper that we failed to initialize
        return False

    global_source1 = config[DOMAIN][CONF_SOURCE1]

    # Validate that the source entity ids exist
    if hass.states.get(global_source1) is None:
        _LOGGER.error("Source entity id %s does not exist", global_source1)

        # Tell the bootstrapper that we failed to initialize
        return False

    global_source2 = config[DOMAIN][CONF_SOURCE2]

    if hass.states.get(global_source2) is None:
        _LOGGER.error("Source entity id %s does not exist", global_source2)

        # Tell the bootstrapper that we failed to initialize
        return False

    global_source1_mw = float(config[DOMAIN][CONF_SOURCE1_MW])
    global_source2_mw = float(config[DOMAIN][CONF_SOURCE2_MW])

    def track_sources(entity_id, old_state, new_state):
        """ Fired when the systemline unit power useage updates """
        source1_current_mw = global_hass.states.get(global_source1).attributes.get('current_power_mwh', 0)
        source2_current_mw = global_hass.states.get(global_source2).attributes.get('current_power_mwh', 0)
        if source1_current_mw >= global_source1_mw or source2_current_mw >= global_source2_mw :
            if source1_current_mw >= global_source1_mw :
              print('turn_on_hi_fi_sources: turn on for %s', global_source1)
            if source2_current_mw >= global_source2_mw :
              print('turn_on_hi_fi_sources: turn on for %s', global_source2)
            core.turn_on(global_hass, global_target)
        else:
            print('turn_on_hi_fi_sources: turn off')
            core.turn_off(global_hass, global_target)

    hass.states.track_change(global_source1, track_sources)
    hass.states.track_change(global_source2, track_sources)

    # Tells the bootstrapper that the component was successfully initialized
    return True
