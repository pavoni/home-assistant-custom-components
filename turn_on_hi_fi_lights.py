
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


def setup(hass, config):
    """ Setup example component. """
    # Validate that all required config options are given

    if not validate_config(config, {DOMAIN: [CONF_SCENE_SOURCE]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_SCENE_POWER]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_SOURCE]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_POWER]}, _LOGGER):
        return False

    scene_source = config[DOMAIN][CONF_SCENE_SOURCE]
    scene_power = config[DOMAIN][CONF_SCENE_POWER]

    # Validate that the target entity id exists
    if hass.states.get(scene_power) is None:
        _LOGGER.error("Target entity id %s does not exist", scene_power)

        # Tell the bootstrapper that we failed to initialize
        return False

    if hass.states.get(scene_source) is None:
        _LOGGER.error("Target entity id %s does not exist", scene_source)

        # Tell the bootstrapper that we failed to initialize
        return False

    source = config[DOMAIN][CONF_SOURCE]

    # Validate that the source entity ids exist
    if hass.states.get(source) is None:
        _LOGGER.error("Source entity id %s does not exist", source)

        # Tell the bootstrapper that we failed to initialize
        return False

    power = config[DOMAIN][CONF_POWER]

    if hass.states.get(power) is None:
        _LOGGER.error("Source entity id %s does not exist", power)

        # Tell the bootstrapper that we failed to initialize
        return False

    def track_sources(entity_id, old_state, new_state):
        """ Fired when one of the sources state updates unit """

        source_on = hass.states.get(source).state == 'on'
        power_on = hass.states.get(power).state == 'on'
        if power_on :
            core.turn_on(hass, scene_power)
        elif source_on :
            core.turn_on(hass, scene_source)
        else:
            # core.turn_off(hass, scene_source)
            # core.turn_off(hass, scene_power)
            # Hack until scenes work properly
            core.turn_off(hass, 'group.special')

    hass.states.track_change(source, track_sources)
    hass.states.track_change(power, track_sources)

    # Tells the bootstrapper that the component was successfully initialized
    return True
