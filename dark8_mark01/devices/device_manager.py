from dark8_mark01.devices.usb_scanner import scan_usb_devices
from dark8_mark01.devices.wifi_scanner import scan_wifi_networks


def get_all_devices():
    return {
        "usb": scan_usb_devices(),
        "wifi": scan_wifi_networks(),
    }
