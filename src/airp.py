#!/usr/bin/python3

import json
import os
import plistlib
import sys

from Alfred3 import Items, Tools

AIRPD_PRODUCT_INDX = {
    8202: "airpodmax",
    8206: "airpodpro",
    8194: "airpod1",
    8207: "airpod2",
    8203: "powerbeatspro"
}


def paired_airpods() -> dict:
    """
    Get paired AirPods including info

    Returns:
        dict: dict with paired AirPod name including dict with info
    """
    jsn: dict = json.loads(os.popen('system_profiler SPBluetoothDataType -json').read())
    devices: dict = jsn['SPBluetoothDataType'][0]['devices_list']
    out_dict = {}
    for i in devices:
        for d_name, d_info in i.items():
            address: str = d_info.get('device_address')
            if 'device_productID' in d_info:  # check if device is a supported headset
                prod_id = int(d_info.get('device_productID', 0), 16)
                vendor_id: str = int(d_info.get('device_vendorID', 0), 16)
                prod_label = AIRPD_PRODUCT_INDX.get(prod_id)
                if vendor_id == 76 and prod_id in AIRPD_PRODUCT_INDX.keys():
                    out_dict.update(
                        {d_name:
                            {"address": address,
                             "connected": d_info.get('device_connected'),
                             "prod_label": prod_label
                             }
                         }
                    )
    return out_dict


def main():
    query = Tools.getArgv(1)
    wf = Items()
    for ap_name, status in paired_airpods().items():
        adr: str = status.get('address')
        ap_type: str = status.get('prod_label')
        is_connected: bool = True if status.get('connected') == 'Yes' else False
        con_str: str = "connected, Press \u23CE to disconnect..." if is_connected else "NOT connected, \u23CE to connect..."
        ico: str = f"{ap_type}.png" if is_connected else f"{ap_type}_case.png"
        con_switch: str = "connected" if is_connected else "disconnected"
        if query == "" or query.lower() in ap_name.lower():
            wf.setItem(
                title=ap_name,
                subtitle=f"{ap_name} are {con_str}",
                arg=f"{adr};{con_switch}",
                uid=adr
            )
            wf.setIcon(ico, "image")
            wf.addItem()
    wf.write()


if __name__ == "__main__":
    main()
