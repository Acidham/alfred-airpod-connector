#!/usr/bin/python3

import os

from Alfred3 import Tools

query = Tools.getArgv(1)
adr, switch = tuple(query.split(";"))

if switch == "disconnected":
    Tools.log(adr)
    os.popen(f'blueutil --connect {adr}')
else:
    os.popen(f'blueutil --disconnect {adr} --wait-disconnect {adr}')
