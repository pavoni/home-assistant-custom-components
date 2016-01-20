from custom_components.switch.custom_wemo_maker import CustomWemoMaker

import homeassistant.components as core

import time

# Press open button twice to avoid partial open issue
REPRESS_AFTER = 20
REPRESS_GAP = 3

class CustomGate(CustomWemoMaker):
    """ Wraps an exising switch, changing behaviour. """

    def turn_on(self, **kwargs):
        """ Turns the switch on. """
        if self.is_on :
        	return
        core.turn_on(self.hass, self.target)
        time.sleep(REPRESS_AFTER)
        core.turn_on(self.hass, self.target)
        time.sleep(REPRESS_GAP)
        core.turn_on(self.hass, self.target)
        super(CustomGate, self).turn_on()

    def turn_off(self):
        """ Turns the switch off. """
        if not self.is_on :
        	return
        core.turn_on(self.hass, self.target)
        super(CustomGate, self).turn_off()
