from homeassistant.helpers.entity import Entity

import homeassistant.components as core
from homeassistant.helpers.event import track_state_change

class CustomSensor(Entity):
    """ Wraps a wemo maker using the sensor as the switch state """

    def __init__(self, new_name, new_target, new_hass):
        self._name = new_name
        self.target = new_target
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
    def get_target_state(self):
        try:
            return self.hass.states.get(self.target)
        except AttributeError:
            return 'failed'
