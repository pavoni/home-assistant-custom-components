from homeassistant.components.switch import SwitchDevice

import homeassistant.components as core
from homeassistant.helpers.event import track_state_change

class CustomWemoMaker(SwitchDevice):
    """ Wraps a wemo maker using the sensor as the switch state """

    def __init__(self, new_name, maker, new_hass):
        self._name = new_name
        self.target = maker
        self.hass = new_hass

        def copy_target_state(entity_id, old_state, new_state):
            """ Called when the target device changes state. """
            self.hass.states.set(self.entity_id, self.get_target_state)

        track_state_change(self.hass, self.target, copy_target_state)

    @property
    def state(self):
        return self.get_target_state

    @property
    def should_poll(self):
        return True

    @property
    def name(self):
        """ Returns the name of the switch if any. """
        return self._name

    @property
    def is_on(self):
        """ True if switch is on. """
        return self.get_target_state != 'off'

    @property
    def get_target_state(self):
        # Default to off if something went wrong
        try:
            return self.hass.states.get(self.target).attributes.get('sensor_state', 'failed')
        except AttributeError:
            return 'failed'

