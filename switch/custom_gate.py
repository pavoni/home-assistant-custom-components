from custom_components.switch.custom_wemo_maker import CustomWemoMaker

import homeassistant.components as core

class CustomGate(CustomWemoMaker):
    """ Wraps an exising switch, changing behavious. """


    def turn_on(self, **kwargs):
        """ Turns the switch on. """
        print('CustomGate turn on;')
        core.turn_on(self.hass, self.target)
        super(CustomGate, self).turn_on()


    def turn_off(self):
        """ Turns the switch off. """
        print('CustomGate turn off;')
        core.turn_off(self.hass, self.target)
        super(CustomGate, self).turn_off()
