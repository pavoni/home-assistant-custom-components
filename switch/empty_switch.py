from homeassistant.components.switch import SwitchDevice

class EmptySwitch(SwitchDevice):
    """ Wraps a wemo maker using the sensor as the switch state """

    def __init__(self, new_name, new_hass, init_state = 'off'):
        self._name = new_name
        self.hass = new_hass
        self.my_state = init_state

    @property
    def state(self):
        return self.my_state

    @property
    def should_poll(self):
        return False

    @property
    def name(self):
        """ Returns the name of the switch if any. """
        return self._name

    @property
    def is_on(self):
        """ True if switch is on. """
        return self.my_state != 'off'

    def turn_on(self, **kwargs):
        """ Turn the entity on. """
        self.my_state = 'on'
        self.hass.states.set(self.entity_id, self.my_state)

    def turn_off(self, **kwargs):
        """ Turn the entity off. """
        self.my_state = 'off'
        self.hass.states.set(self.entity_id, self.my_state)
