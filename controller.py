#!/usr/bin/env python

from evdev import InputDevice, categorize, ecodes
import stepper
import threading

import time    
from enum import Enum

#creates object 'gamepad' to store the data
gamepad = InputDevice('/dev/input/event1')
stepper = stepper.stepper()
import queue


#loop and filter by event code and print the mapped label

encodermax = 65536.0
deadzone = .1

message_queue = queue.Queue()


    
class Message(Enum):
    POS = 1
    NEG = 2
    OFF = 3
    LAST = 4


def worker_function(mqueue):
    last_msg = Message.OFF
    rpos = 1
    while True:

        try:
            message = mqueue.get(False)
            print(f"Processing message: {message}")

        except queue.Empty:
            message = Message.LAST

        if message is None:
            break  # Exit the loop if a None message is received

        if(message == Message.POS):
            stepper.move(True, rpos)
            last_msg = message
        elif(message == Message.NEG):
            stepper.move(False, rpos)
            last_msg = message
        elif(message == Message.LAST):
            if(last_msg == Message.POS or last_msg == Message.NEG):
                stepper.move(last_msg == Message.POS, rpos)
        elif(message == Message.OFF):
            last_msg = Message.OFF
            stepper.off()


worker_thread = threading.Thread(target=worker_function, args=(message_queue,))
worker_thread.start()

for event in gamepad.read_loop():
    epoch_time = int(time.time())

    if(event.sec  < epoch_time): # + float(event.nsec) * 1e-9
        continue

    if event.type == 3:
        if event.code == 0:
            if(abs(event.value / encodermax - .5) >  deadzone):
                print("X ",  event.value / encodermax, event.sec )

                if event.value / encodermax > .5:
                    message_queue.put(Message.POS)
                else:
                    message_queue.put(Message.NEG)

            else:    
                message_queue.put(Message.OFF)



        




