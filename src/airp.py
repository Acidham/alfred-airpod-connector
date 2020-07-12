#!/usr/bin/env python3

import json
import os
import plistlib
import sys

from Alfred3 import Items, Tools

AIRPD_PRODUCT_INDX = {
    8206: "airpodpro",
    8194: "airpod1",
    8207: "airpod2",
    8203: "powerbeatspro"

}

# automatic blueutil installer
os.environ['PATH'] = os.popen('./_sharedresources "blueutil"').readline()


def airpod_info(device_id: str) -> tuple:
    """
    Get airpod info with a given address (MAC)

    Args:
        device_id (str): MAC address of the AirPod to search

    Returns:
        tuble: productlabel, productid, vendorid
    """
    with open("/Library/Preferences/com.apple.Bluetooth.plist", "rb") as f:
        pl = plistlib.load(f)
    devices: dict = pl.get("DeviceCache")
    ret: tuple = tuple()
    for d, v in devices.items():
        if device_id in d:
            product_id: str = v.get("ProductID")
            product_label: str = AIRPD_PRODUCT_INDX.get(product_id)
            vendor_id: str = v.get("VendorID")
            ret: tuple = (product_label, product_id, vendor_id)
            break
    return ret


def paired_airpods() -> dict:
    """
    Get paired AirPods including info

    Returns:
        dict: dict with paired AirPod name including dict with info
    """
    jsn: dict = json.loads(os.popen('blueutil --paired --format json').read())
    out_dict = {}
    for i in jsn:
        address: str = i.get('address')
        prod_label, prod_id, vendor_id = airpod_info(address)
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
    """
    Checks if Blueutil was properly installed

    Returns:
        bool: True=available, False=not found
    """
    blueutil: str = os.popen("blueutil -v").readline()
    if blueutil == "":
        return False
    else:
        return True


def main():
    wf = Items()
    if is_blueutil():
        for ap_name, status in paired_airpods().items():
            adr: str = status.get('address')
            ap_type: str = status.get('prod_label')
            is_connected: bool = status.get('connected')
            con_str: str = "connected, Press \u23CE to disconnect..." if is_connected else "NOT connected, \u23CE to connect..."
            ico: str = f"{ap_type}.png" if is_connected else f"{ap_type}_case.png"
            con_switch: str = "connected" if is_connected else "disconnected"
            wf.setItem(
                title=ap_name,
                subtitle=f"{ap_name} are {con_str}",
                arg=f"{adr};{con_switch}",
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


if __name__ == "__main__":
    main()
