from __future__ import print_function
import time
import random
import secrets      
import can 
import cantools

import numpy as np
def send_message(name, data, bus):
    db = cantools.database.load_file('../src/workshop.dbc')
    try:
        m = list(filter(lambda x:x.name == name, db.messages))[0]
    except:
        print("Message name {} not found in the loaded dbc. No Message sent.".format(name))
        return
    try:
        data = m.encode(data)
    except:
        print("Error encoding data {}.\nValid signals are {}\nNo Message was sent".format(data, m.signals))
        return
    byte_arr = list(data)
    for sig in m.signals:
        for x in range(sig.offset+sig.length,len(byte_arr)):
            byte_arr[x] = int.from_bytes(secrets.token_bytes(1), byteorder="little")
        data = list(byte_arr)
        bus.send(can.Message(arbitration_id=m.frame_id, data=data, is_extended_id=False))
if __name__ == "__main__":
    bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=25000)
    while True:
        send_message('PhySensors', {'Vehicle_Speed':120, 'RPM':9, 'Service_Light':0},bus)
        time.sleep(0.1)