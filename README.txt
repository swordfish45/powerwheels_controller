# Connect xontroller to bt

sudo bluetoothctl
power on
agent on
default-agent
scan on
pair [id]

my controller id is  98:7A:14:62:4D:27

# Test controller
python3 .venv/lib/python3.9/site-packages/evdev/evtest.py


# get controller mapping

#!/usr/bin/env python


import evdev
from evdev import InputDevice, categorize, ecodes

#creates object 'gamepad' to store the data
#you can call it whatever you like
gamepad = InputDevice('/dev/input/event1')

#prints out device info at start
print(gamepad)

#evdev takes care of polling the controller in a loop
for event in gamepad.read_loop():
    print(categorize(event))


synchronization event at 1699737673.095146, SYN_REPORT
absolute axis event at 1699737673.132847, ABS_X
synchronization event at 1699737673.132847, SYN_REPORT