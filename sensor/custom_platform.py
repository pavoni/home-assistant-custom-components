"""
homeassistant.components.sensor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Custom platform to import custom switches.

"""
from custom_components.sensor.custom_sensor_maker import CustomSensorMaker
from custom_components.sensor.custom_sensor_insight import CustomSensorInsight
from custom_components.sensor.custom_sensor_rain import CustomSensorRain
import logging


DEPENDENCIES = []

DOMAIN = "custom_platform_sensor"

# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """ Find and return custom sensors for rain_sensor and hi_fi_systemline. """
    add_devices_callback([
        CustomSensorMaker('systemline', 'switch.hi_fi_systemline_sensor', hass),
        CustomSensorRain('rain', 'switch.rain_sensor', hass),
        CustomSensorInsight('preamp', 'switch.hi_fi_preamp', hass),
        CustomSensorInsight('kettle', 'switch.kettle', hass),
    ])


