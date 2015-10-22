import time
import logging
from datetime import timedelta

from homeassistant.helpers import validate_config
import homeassistant.util.dt as dt_util
import homeassistant.components as core
from homeassistant.helpers.event import track_state_change, track_point_in_time


# The domain of your component. Should be equal to the name of your component
DOMAIN = "blind_open_close"

# List of component names (string) your component depends upon
# We depend on group because group will be loaded after all the components that
# initialize devices have been setup.
DEPENDENCIES = ['group']

# Configuration key for the entity id we are targetting
CONF_SOURCE_RADIO = 'source_radio'
CONF_TARGET_BLIND = 'target_blind'
CONF_TARGET_LIGHT = 'target_light'
CONF_SNOOZE_DELAY = 'snooze'
CONF_SLEEP_DELAY = 'sleep'

SUN = 'sun.sun'
SET_TIME = 'next_setting'
RISE_TIME = 'next_rising'

# Shortcut for the logger
_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    """ Setup blind_open_close"""

    # Validate that all required config options are given

    if not validate_config(config, {DOMAIN: [CONF_SOURCE_RADIO]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_TARGET_BLIND]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_TARGET_LIGHT]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_SNOOZE_DELAY]}, _LOGGER):
        return False

    if not validate_config(config, {DOMAIN: [CONF_SLEEP_DELAY]}, _LOGGER):
        return False

    radio = config[DOMAIN][CONF_SOURCE_RADIO]
    blind = config[DOMAIN][CONF_TARGET_BLIND]
    light = config[DOMAIN][CONF_TARGET_LIGHT]
    snooze = int(config[DOMAIN][CONF_SNOOZE_DELAY])
    sleep = int(config[DOMAIN][CONF_SLEEP_DELAY])

    def close_blind(now):
        core.turn_off(hass, blind)

    def turn_off_light(now):
        core.turn_off(hass, light)

    def open_blind_if_radio_on(now):
        radio_on = core.is_on(hass, radio)
        if radio_on:
            core.turn_on(hass, blind)
            time.sleep(20)
            sun_up = hass.states.get(SUN) == 'above_horizon'
            if not sun_up:
                core.turn_on(hass, light)
                set_up_blind_sunrise_timer(None, None, None)


    def set_up_blind_sunset_timer(entity_id, old_state, new_state):
        sunset = hass.states.get(SUN).attributes.get(SET_TIME, 0)
        sunset_tm = dt_util.str_to_datetime(sunset)
        target_tm = sunset_tm + timedelta(minutes = sleep)
        track_point_in_time(hass, close_blind, target_tm)

    def set_up_blind_sunrise_timer(entity_id, old_state, new_state):
        sunrise = hass.states.get(SUN).attributes.get(RISE_TIME, 0)
        sunrise_tm = dt_util.str_to_datetime(sunrise)
        target_tm = sunrise_tm + timedelta(minutes = sleep)
        track_point_in_time(hass, turn_off_light, target_tm)

    set_up_blind_sunset_timer(None, None, None)
    track_state_change(hass, SUN, set_up_blind_sunset_timer)

    def radio_on(entity_id, old_state, new_state):
        now = dt_util.now()
        start_window = now.replace( hour=6, minute=45)
        end_window  = now.replace( hour=9, minute=45)
        target_tm = now + timedelta(minutes = snooze)
        radio_on = core.is_on(hass, radio)
        blind_closed = not core.is_on(hass, blind)
        if blind_closed and radio_on and now > start_window and now < end_window :
            track_point_in_time(hass, open_blind_if_radio_on, target_tm)

    track_state_change(hass, radio, radio_on)

    # Tells the bootstrapper that the component was successfully initialized
    return True
