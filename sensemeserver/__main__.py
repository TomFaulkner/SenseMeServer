#!/usr/bin/env python3
from typing import Union

import hug

from senseme import SenseMe

from load_devices import load_devices
"""
config loader / saver

/devicename/feature/setting/value

feature - fan/light
setting - brightness/power/whoosh/motion/etc
"""

# load the config
# for now though
config = {}

# load devices
device_db = load_devices()

# convert loaded devices list to senseme device object list
devices = []
for device in device_db:
    devices.append(SenseMe(**device))

def _device(device_id: Union[str, int], devices: list):
    if isinstance(device_id, str):
        try:
            return devices[int(device_id)]
        except ValueError:
            return devices[device_id]
    return devices[devices.keys()[device_id]]

@hug.get('/{device}/fan/speed')
def fan_speed(device: str):
    try:
        return _device(device, devices).speed 
    except:
        return devices

@hug.post('/{device}/fan/speed')
def fan_speed(device: str, speed: int):
    _device(device, devices).speed = speed 
    return _device(device, devices).speed

