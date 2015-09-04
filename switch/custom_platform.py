"""
homeassistant.components.wemo_blind
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Custom platform to import custom switches.

"""
from custom_components.switch.custom_blind import CustomBlind
from custom_components.switch.custom_gate import CustomGate
from custom_components.switch.custom_skylight import CustomSkylight
import logging


# DEPENDENCIES = ['switch.blind', 'switch.gate', 'switch.skylight_open', 'switch.skylight_close', 'switch.rain_sensor']
DEPENDENCIES = []

DOMAIN = "custom_platform"

# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """ Find and return blind switches. """
    add_devices_callback([
        CustomBlind('Blind', 'switch.blind', hass),
        CustomGate('Gate', 'switch.gate', hass),
        CustomSkylight('Velux Skylight', 'switch.skylight_open', 'switch.skylight_close', 'switch.rain_sensor', hass)
    ])


