import logging

from homeassistant.components.switch import SwitchDevice

import homeassistant.components as core
from homeassistant.helpers.event import track_state_change

# Shortcut for the logger
_LOGGER = logging.getLogger(__name__)

class CustomSkylight(SwitchDevice):
    """ Wraps two wemo makers with momentary switches """

    def __init__(self, new_name, maker_on, maker_off, maker_rain_sensor, new_hass):
        self._name = new_name
        self.target_on = maker_on
        self.target_off = maker_off
        self.target_rain_sensor = maker_rain_sensor
        self.hass = new_hass
        # Keep state private to avoid anything else changing it!
        # Default to off - no sensor - but probably closed
        self._state = 'off'

        def close_skylight_if_raining(entity_id, old_state, new_state):
            """ Called when the target device changes state. """
            if self.raining:
                _LOGGER.warning('CustomSkylight close because of rain!')
                self.turn_off()

        track_state_change(self.hass, self.target_rain_sensor, close_skylight_if_raining)

    @property
    def state(self):
        """ Returns the state of the switch if any. """
        return self._state

    @property
    def name(self):
        """ Returns the name of the switch if any. """
        return self._name

    @property
    def raining(self):
        """ Returns whether the rain sensor think it's raining. Default to True if there is a problem!"""
        try:
            sensor_state = self.hass.states.get(self.target_rain_sensor).attributes.get('sensor_state', 'failed')
        except AttributeError:
            sensor_state = 'failed'
            _LOGGER.warning('CustomSkylight could not comminucate with rain sensor!')
        return not (sensor_state == 'off')


    def turn_on(self, **kwargs):
        """ Opens the Skylight - toggles the momentary switch. """
        if not self.raining:
            core.turn_on(self.hass, self.target_on)
            self._state = 'on'
        else:
            _LOGGER.warning('CustomSkylight open - refused because of rain!')


    def turn_off(self):
        """ Closes the Skylight - toggles the momentary switch. """
        core.turn_on(self.hass, self.target_off)
        self._state = 'off'
