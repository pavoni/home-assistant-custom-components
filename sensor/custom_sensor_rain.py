from custom_components.sensor.custom_sensor_maker import CustomSensorMaker

import homeassistant.components as core

class CustomSensorRain(CustomSensorMaker):
    @property
    def get_target_state(self):
        # Default to off if something went wrong
        try:
            ret = self.hass.states.get(self.target).attributes.get('sensor_state', 'failed')
            if ret == 'on':
                return 'rain'
            elif ret =='off':
                return 'dry'
            else:
                ret
        except AttributeError:
            return 'failed'
