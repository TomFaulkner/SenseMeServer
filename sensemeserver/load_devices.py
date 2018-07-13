import json
import os

from constants import DEVICE_DB_NAME, ENV_VAR_PREFIX, ENV_DEVICE_NAME


def _load_device_data(fn: str) -> list:
    try:
        with open(fn) as f:
            return json.load(f)['devices']
    except OSError:
        return []


def _load_device_data_env() -> list:
    devices = []
    for x in range(1, 100):
        device = os.environ.get(f'{ENV_VAR_PREFIX}_{ENV_DEVICE_NAME}_{x}')
        if device:
            try:
                ip, name = device.split(',')
                devices.append({'ip': ip, 'name': name})
            except ValueError:
                devices.append({'ip': ip, 'name': ''})
        else:
            break
    return devices


def load_devices() -> list:
    """Load devices from device file and environment variables."""
    devices = []
    devices.extend(_load_device_data(DEVICE_DB_NAME))
    devices.extend(_load_device_data_env())
    return devices


def write_devices(devices: list, fn: str) -> None:
    """Write device data to file"""
    with open(fn, 'w') as f:
        json.dump({'devices': f})

