#!/usr/bin/env python3
from typing import Union

import hug
from senseme import SenseMe

from load_devices import load_devices
"""
/devicename/feature/setting/value

feature - fan/light
setting - brightness/power/whoosh/motion/etc
"""


def _device(device_id: str, devices: list) -> SenseMe:
    """helper to support {device} being either index or name"""
    try:
        idx = int(device_id)
        return devices[tuple(devices.keys())[idx]]
    except ValueError:
        return devices[device_id]


# @hug.cli(name='speed_get')
@hug.get('/{device}/fan/speed')
def fan_speed_get(device: str):
    try:
        return _device(device, devices).speed 
    except:
        return devices

# @hug.cli(name='speed')
@hug.post('/{device}/fan/speed')
def fan_speed(device: str, speed: int):
    _device(device, devices).speed = speed 
    return _device(device, devices).speed



API = hug.API('brightness')

@hug.object(name='brightness', api=API)
class Light:
    @hug.post('/{device}/light/brightness')
    @hug.object.cli
    def set_brightness(self, device: str, brightness: int) -> int:
        _device(device, devices).brightness = brightness
        return _device(device, devices).brightness

    @hug.get('/{device}/light/brightness')
    @hug.object.cli
    def get_brightness(self, device: str) -> int:
        return _device(device, devices).brightness



device_db = load_devices()

# convert loaded devices list to senseme device object list
devices = {}
for idx, device in enumerate(device_db):
    # devices.append(SenseMe(**device))
    name = device['name'] if device['name'] else idx    
    devices[name] = SenseMe(**device) 
    
# fan_speed.interface.cli() 
# fan_speed_get.interface.cli()
if __name__ == '__main__':
    API.cli()


