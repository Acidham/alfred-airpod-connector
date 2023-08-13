#!/usr/bin/python3

import os
import shutil
import sys
import re

from Alfred3 import Tools

query = Tools.getArgv(1)
name, switch, adr = tuple(query.split(";"))
adr_escaped = re.sub("\s", "\ ", adr)
name_escaped = re.sub("\s", "\ ", name)

blueutil = shutil.which('blueutil')
switch_audio = os.environ["SwitchAudioSource_path"]

# if blueutil doesn't exist, we can just quit right away
if not blueutil:
    sys.exit()

# current behaviour: when the APs are not connected, we connect them with blueutil and move audio to them. If they are connected, we just move audio to them
if switch == "disconnected":
    Tools.log(name_escaped)
    # this connects to the airpods
    os.popen(f'{blueutil} --connect {adr_escaped}')
    # this moves audio to the airpods
    os.popen(f'{switch_audio} -s {name_escaped}')
else:
    os.popen(f'{switch_audio} -s {name_escaped}')