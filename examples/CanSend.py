from __future__ import print_function
from turtle import speed
import can 
import cantools
import secrets
import numpy as np
import random
import time
def send_one():
    bus = can.interface.Bus(bustype='socketcan', channel='vacn1', bitrate=250000)
    msg = can.Messages(arbitration_id=0x111,
                       data=[0x33, 0x6c, 0x14, 0x7B, 0xB2, 0xFF, 0xFF]
                       is_extended_id=False)
    speed = 140*256
    hex_num = hex(speed)
    hex_num = hex_num[2:6]
    byte_2 = hex_num[0:2]
    byte_3 = hex_num[2:4]
    while True:
        try:
            bus.send(msg)
            print("Message sent on {}".format(bus.channel_info))
        except:
            print("Message NOT sent")
        time.sleep(0)
if __name__ == '__main__':
    send_one()