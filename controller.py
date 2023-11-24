#!/usr/bin/env python

from evdev import InputDevice, categorize, ecodes
import stepper
import threading
import logging
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
    CUR_UP = 5
    CUR_DOWN = 6


def worker_function(mqueue):
    last_msg = Message.OFF
    rpos = 10
    currents = [250, 500, 750, 1000, 1250, 1500, 1750, 2000]

    cur_current = 0

    while True:
        epoch_time = int(time.time())


        try:

            messaget = mqueue.get(False)
            (mtime, message) = messaget
            if messaget is None:
                break  # Exit the loop if a None message is received
            print(f"Processing message: {message}")

        except queue.Empty:
            message = Message.LAST
            mtime = epoch_time




        if(not(message == Message.OFF) and mtime  < epoch_time): # + float(event.nsec) * 1e-9
            continue


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
        elif(message == Message.CUR_UP):
            if(cur_current < len(currents)-1):
                cur_current = cur_current + 1
                stepper.set_current(currents[cur_current])
        elif(message == Message.CUR_DOWN):
            if(cur_current > 0):
                cur_current = cur_current - 1
                stepper.set_current(currents[cur_current])

worker_thread = threading.Thread(target=worker_function, args=(message_queue,))
worker_thread.start()

for event in gamepad.read_loop():
    epoch_time = int(time.time())

    if(event.sec  < epoch_time): # + float(event.nsec) * 1e-9
        continue
    # print("event.type " , event.type , "event.code", event.code ,"event.value", event.value)

    if event.type == 3:
        if event.code == 17:
            if event.value == -1: #raise current
                message_queue.put((event.sec, Message.CUR_UP))
            if event.value == 1: #lower current
                message_queue.put((event.sec, Message.CUR_DOWN))



        if event.code == 0:
            if(abs(event.value / encodermax - .5) >  deadzone):
                print("X ",  event.value / encodermax, event.sec )

                if event.value / encodermax > .5:
                    message_queue.put((event.sec, Message.POS))
                else:
                    message_queue.put((event.sec, Message.NEG))

            else:    
                message_queue.put((event.sec, Message.OFF))



        




