from custom_components.switch.custom_wemo_maker import CustomWemoMaker

import homeassistant.components as core

class CustomGate(CustomWemoMaker):
    """ Wraps an exising switch, changing behaviour. """

    def turn_on(self, **kwargs):
        """ Turns the switch on. """
        core.turn_on(self.hass, self.target)
        super(CustomGate, self).turn_on()

    def turn_off(self):
        """ Turns the switch off. """
        core.turn_on(self.hass, self.target)
        super(CustomGate, self).turn_off()
