
import time
import logging

from homeassistant.helpers import validate_config
import homeassistant.components as core
from homeassistant.helpers.event import track_state_change

# The domain of your component. Should be equal to the name of your component
DOMAIN = "turn_on_hi_fi_lights"

# List of component names (string) your component depends upon
# We depend on group because group will be loaded after all the components that
# initialize devices have been setup.
DEPENDENCIES = ['group', 'scene']

# Configuration key for the entity id we are targetting
CONF_SCENE_SOURCE = 'scene_source'
CONF_SCENE_POWER = 'scene_power'
CONF_SCENE_OFF = 'scene_off'

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


    if not validate_config(config, {DOMAIN: [CONF_SCENE_OFF]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_SOURCE]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_POWER]}, _LOGGER):
        return False

    scene_source = config[DOMAIN][CONF_SCENE_SOURCE]
    scene_power = config[DOMAIN][CONF_SCENE_POWER]
    scene_off = config[DOMAIN][CONF_SCENE_OFF]
    source = config[DOMAIN][CONF_SOURCE]
    power = config[DOMAIN][CONF_POWER]

    def track_sources(entity_id, old_state, new_state):
        """ Fired when one of the sources state updates unit """
        if not (hass.states.get(source) and hass.states.get(power)):
            _LOGGER.warning('Source components not initialised')
            return
        source_on = hass.states.get(source).state == 'on'
        power_on = hass.states.get(power).state == 'on'
        if power_on :
            core.turn_on(hass, scene_power)
        elif source_on :
            core.turn_on(hass, scene_source)
        else:
            core.turn_on(hass, scene_off)

    track_state_change(hass, source, track_sources)
    track_state_change(hass, power, track_sources)

    # Tells the bootstrapper that the component was successfully initialized
    return True
