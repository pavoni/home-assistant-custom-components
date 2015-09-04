from custom_components.switch.custom_wemo_maker import CustomWemoMaker

import homeassistant.components as core

class CustomGate(CustomWemoMaker):
    """ Wraps an exising switch, changing behavious. """


    def turn_on(self, **kwargs):
        """ Turns the switch on. """
        print('CustomGate turn on;')
        if (self.is_on):
            return
        core.turn_on(self.hass, self.target)

    def turn_off(self):
        """ Turns the switch off. """
        print('CustomGate turn off;')
        if not(self.is_on):
            return
        if core.is_on(self.hass, self.target):
            core.turn_off(self.hass, self.target)
        else:
            core.turn_on(self.hass, self.target)
