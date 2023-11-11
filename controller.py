#!/usr/bin/env python

from evdev import InputDevice, categorize, ecodes


#creates object 'gamepad' to store the data
gamepad = InputDevice('/dev/input/event1')



#loop and filter by event code and print the mapped label

encodermax = 65536.0
for event in gamepad.read_loop():

    if event.type == 3:
        if event.code == 0:
            if(abs(encodermax/2 - event.value) > 0.6):
                print("X ", event.value / encodermax )
