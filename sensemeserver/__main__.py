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

device_db = load_devices()

# convert loaded devices list to senseme device object list
devices = {}
for idx, device in enumerate(device_db):
    # devices.append(SenseMe(**device))
    name = device['name'] if device['name'] else idx    
    devices[name] = SenseMe(**device) 


def _device(device_id: str, devices: list) -> SenseMe:
    """helper to support {device} being either index or name"""
    try:
        idx = int(device_id)
        return devices[tuple(devices.keys())[idx]]
    except ValueError:
        return devices[device_id]


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

