import time
import logging
from datetime import timedelta

from homeassistant.const import STATE_HOME, STATE_NOT_HOME, STATE_ON, STATE_OFF
import homeassistant.loader as loader
from homeassistant.helpers import validate_config
import homeassistant.util.dt as dt_util
import homeassistant.components as core

# The domain of your component. Should be equal to the name of your component
DOMAIN = "blind_open_close"

# List of component names (string) your component depends upon
# We depend on group because group will be loaded after all the components that
# initialize devices have been setup.
DEPENDENCIES = ['group']

# Configuration key for the entity id we are targetting
CONF_SOURCE_RADIO = 'source_radio'
CONF_TARGET_BLIND = 'target_blind'
CONF_SNOOZE_DELAY = 'snooze'
CONF_SLEEP_DELAY = 'sleep'

SUN = 'sun.sun'
SET_TIME = 'next_setting'

# Shortcut for the logger
_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    """ Setup blind_open_close"""

    # Validate that all required config options are given

    if not validate_config(config, {DOMAIN: [CONF_SOURCE_RADIO]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_TARGET_BLIND]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_SNOOZE_DELAY]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_SLEEP_DELAY]}, _LOGGER):
        return False

    radio = config[DOMAIN][CONF_SOURCE_RADIO]
    blind = config[DOMAIN][CONF_TARGET_BLIND]
    snooze = int(config[DOMAIN][CONF_SNOOZE_DELAY])
    sleep = int(config[DOMAIN][CONF_SLEEP_DELAY])

    # Validate that the radio entity id exists
    if hass.states.get(radio) is None:
        _LOGGER.error("Radio entity id %s does not exist", radio)

        # Tell the bootstrapper that we failed to initialize
        return False

    if hass.states.get(blind) is None:
        _LOGGER.error("Blind entity id %s does not exist", blind)

        # Tell the bootstrapper that we failed to initialize
        return False

    def close_blind():
        core.turn_off(hass, blind)

    def open_blind_if_radio_on():
        if core.is_on(global_hass, global_target1):
            core.turn_on(hass, blind)

    def set_up_blind_sunset_timer(entity_id, old_state, new_state):
        sunset = hass.states.get(SUN).attributes.get(SET_TIME, 0)
        sunset_tm = dt_util.str_to_datetime(sunset)
        target_tm = sunset_tm + timedelta(minutes = sleep)
        hass.track_time_change(close_blind, hour=target_tm.hour, minute=target_tm.minute, second=0)

    set_up_blind_sunset_timer(None, None, None)
    hass.states.track_change(SUN, set_up_blind_sunset_timer)

    def radio_on(entity_id, old_state, new_state):
        now = dt_util.now()
        start_window = now.replace( hour=6, minute=45)
        end_window  = now.replace( hour=9, minute=45)
        target_tm = now + timedelta(minutes = snooze)
        if now > start_window and now < end_window :
            hass.track_time_change(open_blind_if_radio_on, hour=target_tm.hour, minute=target_tm.minute, second=0)

    hass.states.track_change(radio, radio_on)

    # Tells the bootstrapper that the component was successfully initialized
    return True
