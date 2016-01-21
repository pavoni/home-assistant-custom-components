"""
homeassistant.components.switch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Custom platform to import custom switches.

"""
from custom_components.switch.custom_blind import CustomBlind
from custom_components.switch.custom_gate import CustomGate
from custom_components.switch.custom_skylight import CustomSkylight
from custom_components.switch.empty_switch import EmptySwitch
import logging

DEPENDENCIES = []

DOMAIN = "custom_platform"

# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """ Find and return customised switches for gate, blind and skylight. """
    add_devices_callback([
        CustomBlind('Blind', 'switch.blind_toggle', hass),
        CustomGate('Gate', 'switch.gate_toggle', hass),
        CustomSkylight('Skylight', 'switch.skylight_open', 'switch.skylight_close', 'switch.rain_sensor', hass)
    ])


