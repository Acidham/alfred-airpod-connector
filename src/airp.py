#!/usr/bin/env python3

import json
import os
import plistlib
import sys

from Alfred3 import Items, Tools

AIRPD_PRODUCT_INDX = {
    8206: "airpodpro",
    8194: "airpod1",
    8207: "airpod2"

}


def get_airpods(device_id: str) -> tuple:
    """
    Get device status with a given address (MAC)

    Args:
        device_id (str): MAC address of the Device to search

    Returns:
        tuble: Left/Right/Case battery status
    """
    with open("/Library/Preferences/com.apple.Bluetooth.plist", "rb") as f:
        pl = plistlib.load(f)
    devices: dict = pl.get("DeviceCache")
    ret: tuple = tuple()
    for d, v in devices.items():
        if device_id in d:
            product_id: str = v.get("ProductID") if v.get("ProductID") else None
            product_label: str = AIRPD_PRODUCT_INDX.get(product_id)
            vendor_id: str = v.get("VendorID") if v.get("VendorID") else None
            ret: tuple = (product_label, product_id, vendor_id)
            break
    return ret


def get_avail_airpods() -> dict:
    jsn = json.loads(os.popen('/usr/local/bin/blueutil --paired --format json').read())
    out_dict = {}
    for i in jsn:
        address = i.get('address')
        prod_label, prod_id, vendor_id = get_airpods(address)
        if vendor_id == 76 and prod_id in AIRPD_PRODUCT_INDX.keys():
            out_dict.update(
                {i.get('name'):
                    {"address": i.get('address'),
                     "connected": i.get('connected'),
                     "prod_label": prod_label
                     }
                 }
            )
    return out_dict


def is_blueutil() -> bool:
    if os.path.exists("/usr/local/bin/blueutil"):
        return True
    else:
        return False


wf = Items()
if is_blueutil():
    avail_airpods = get_avail_airpods()
    for ap_name, status in avail_airpods.items():
        adr = status.get('address')
        ap_type = status.get('prod_label')
        is_connected = status.get('connected')
        con_str = "connected, Press \u23CE to disconnect..." if is_connected else "NOT connected, \u23CE to connect..."
        ico = f"{ap_type}.png" if is_connected else f"{ap_type}_case.png"
        con_switch = "connected" if is_connected else "disconnected"
        wf.setItem(
            title=ap_name,
            subtitle=f"{ap_name} is {con_str}",
            arg=f"{adr}|{con_switch}",
            uid=adr
        )
        wf.setIcon(ico, "image")
        wf.addItem()
else:
    wf.setItem(
        title="BLUEUTIL required!",
        subtitle='Please install with "brew install blueutil" first',
        valid=False
    )
    wf.addItem()
wf.write()
