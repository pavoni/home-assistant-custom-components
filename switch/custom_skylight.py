from homeassistant.components.switch import SwitchDevice

import homeassistant.components as core

class CustomSkylight(SwitchDevice):
    """ Wraps two wemo makers with momentary switches """

    def __init__(self, new_name, maker_on, maker_off, maker_rain_sensor, new_hass):
        self._name = new_name
        # No sensors - but usually closed - so assume this
        self._state = 'off'
        self.target_on = maker_on
        self.target_off = maker_off
        self.target_rain_sensor = maker_rain_sensor
        self.hass = new_hass

    @property
    def state(self):
        return self._state

    @property
    def should_poll(self):
        return True

    @property
    def name(self):
        """ Returns the name of the switch if any. """
        return self._name

    @property
    def raining(self):
        """ Returns whether the rain sensor think it's raining. Default to True if there is a problem!"""
        try:
            sensor_state = self.hass.states.get(self.target).attributes.get('sensor_state', 'failed')
        except AttributeError:
            return 'failed'
        return not (sensor_state == 'off')

    @property
    def is_on(self):
        """ True if switch is on. """
        return self._state != 'off'

    def turn_on(self, **kwargs):
        """ Opens the Skylight - toggles the momentary switch. """
        if not self.raining:
            print('CustomSkylight open;')
            core.turn_on(self.hass, self.target_on)
            self._state = 'on'
        else:
            print('CustomSkylight turn on - refused becaus of rain!')


    def turn_off(self):
        """ Closes the Skylight - toggles the momentary switch. """
        print('CustomSkylight close;')
        core.turn_on(self.hass, self.target_off)
        self._state = 'off'
