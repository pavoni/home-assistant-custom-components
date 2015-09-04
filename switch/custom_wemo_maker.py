from homeassistant.components.switch import SwitchDevice

class CustomWemoMaker(SwitchDevice):
    """ Wraps a wemo maker using the sensor as the switch state """

    def __init__(self, new_name, maker, new_hass):
        self._name = new_name
        self.target = maker
        self.hass = new_hass

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

