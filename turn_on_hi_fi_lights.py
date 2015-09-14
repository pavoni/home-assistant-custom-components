
import time
import logging

from homeassistant.const import STATE_HOME, STATE_NOT_HOME, STATE_ON, STATE_OFF
import homeassistant.loader as loader
from homeassistant.helpers import validate_config
import homeassistant.components as core

# The domain of your component. Should be equal to the name of your component
DOMAIN = "turn_on_hi_fi_lights"

# List of component names (string) your component depends upon
# We depend on group because group will be loaded after all the components that
# initialize devices have been setup.
DEPENDENCIES = ['group', 'scene']

# Configuration key for the entity id we are targetting
CONF_SCENE_SOURCE = 'scene_source'
CONF_SCENE_POWER = 'scene_power'

CONF_SOURCE = 'source'
CONF_POWER = 'power'

# Shortcut for the logger
_LOGGER = logging.getLogger(__name__)

global_scene_source = 0
global_scene_power = 0
global_source = 0
global_power = 0


def setup(hass, config):
    """ Setup example component. """
    global global_hass, global_target1, global_target2, global_source, global_maker
    global_hass = hass
    # Validate that all required config options are given

    if not validate_config(config, {DOMAIN: [CONF_SCENE_SOURCE]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_SCENE_POWER]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_SOURCE]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_POWER]}, _LOGGER):
        return False

    global_scene_source = config[DOMAIN][CONF_SCENE_SOURCE]
    global_scene_power = config[DOMAIN][CONF_SCENE_POWER]

    # Validate that the target entity id exists
    if hass.states.get(global_scene_power) is None:
        _LOGGER.error("Target entity id %s does not exist", global_scene_power)

        # Tell the bootstrapper that we failed to initialize
        return False

    if hass.states.get(global_scene_source) is None:
        _LOGGER.error("Target entity id %s does not exist", global_scene_source)

        # Tell the bootstrapper that we failed to initialize
        return False

    global_source = config[DOMAIN][CONF_SOURCE]

    # Validate that the source entity ids exist
    if hass.states.get(global_source) is None:
        _LOGGER.error("Source entity id %s does not exist", global_source)

        # Tell the bootstrapper that we failed to initialize
        return False

    global_power = config[DOMAIN][CONF_POWER]

    if hass.states.get(global_power) is None:
        _LOGGER.error("Source entity id %s does not exist", global_power)

        # Tell the bootstrapper that we failed to initialize
        return False

    def track_sources(entity_id, old_state, new_state):
        """ Fired when one of the sources state updates unit """

        source_on = global_hass.states.get(global_source).state == 'on'
        power_on = global_hass.states.get(global_power).state == 'on'
        if power_on :
            core.turn_on(global_hass, global_scene_power)
        elif source_on :
            core.turn_on(global_hass, global_scene_source)
        else:
            core.turn_off(global_hass, global_scene_source)
            core.turn_off(global_hass, global_scene_power)
            # Quick hack until scenes work for hue lights
            core.turn_off(global_hass, 'group.special')

    hass.states.track_change(global_source, track_sources)
    hass.states.track_change(global_power, track_sources)

    # Tells the bootstrapper that the component was successfully initialized
    return True
