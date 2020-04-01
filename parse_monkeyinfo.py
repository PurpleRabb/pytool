#!/usr/bin/env monkeyrunner
# Copyright 2010, The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys
import re

p = re.compile(r'[(](.*)[)]', re.S)
pos = re.findall(p, "0:(118.046295,223.92648)")
(x, y) = pos[0].split(',')
print(x, y)

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage

# The format of the file we are parsing is very carfeully constructed.
# Each line corresponds to a single command.  The line is split into 2
# parts with a | character.  Text to the left of the pipe denotes
# which command to run.  The text to the right of the pipe is a python
# dictionary (it can be evaled into existence) that specifies the
# arguments for the command.  In most cases, this directly maps to the
# keyword argument dictionary that could be passed to the underlying
# command.
# Lookup table to map command strings to functions that implement that
# command.
CMD_MAP = {
    'TOUCH': lambda dev, arg: dev.touch(**arg),
    'DRAG': lambda dev, arg: dev.drag(**arg),
    'PRESS': lambda dev, arg: dev.press(**arg),
    'TYPE': lambda dev, arg: dev.type(**arg),
    'WAIT': lambda dev, arg: MonkeyRunner.sleep(**arg)
}


# Process a single file for the specified device.
def process_file(fp, device):
    for line in fp:
        (cmd, rest) = line.split('|')
        try:
            # Parse the pydict
            rest = eval(rest)
        except:
            print('unable to parse options')
            continue
        if cmd not in CMD_MAP:
            print('unknown command: ' + cmd)
            continue
        CMD_MAP[cmd](device, rest)


p = re.compile(r'[(](.*)[)]', re.S)

actions =  {
'(ACTION_DOWN):' : MonkeyDevice.DOWN,
'(ACTION_UP):' : MonkeyDevice.UP
}
def parse_file(fp, device):
    for line in fp:
        val_list = line.replace('\n', '').split(' ')
        if val_list[1] == 'Key':
            keycode = val_list[-1]
            #if val_list[2] == '(ACTION_DOWN):':
                #print('Down keycode:', keycode)
                #device.press(keycode, MonkeyDevice.DOWN)
            #if val_list[2] == '(ACTION_UP):':
                #print('Up keycode:', keycode)
                #device.press(keycode, MonkeyDevice.UP)
            print(val_list[-1])
            device.press(keycode,actions[val_list[2]])
        if val_list[1] == 'Touch':
            (x, y) = re.findall(p, val_list[-1])[0].split(',')
            print(val_list[2], (x, y))
            device.touch(int(float(x)), int(float(y)),actions[val_list[2]])
        if val_list[0] == 'Sleeping':
            print('Sleep for 300ms')
            MonkeyRunner.sleep(0.3)


def main():
    file = sys.argv[1]
    fp = open(file, 'r')
    device = MonkeyRunner.waitForConnection()

    parse_file(fp, device)
    fp.close()


if __name__ == '__main__':
    main()
