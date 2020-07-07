#!/usr/bin/env python3

import os

from Alfred3 import Tools

# automatic blueutil installer
os.environ['PATH'] = os.popen('./_sharedresources "blueutil"').readline()

query = Tools.getArgv(1)
adr, switch = tuple(query.split(";"))

if switch == "disconnected":
    Tools.log(adr)
    os.popen(f'blueutil --connect {adr}')
else:
    os.popen(f'blueutil --disconnect {adr}')
