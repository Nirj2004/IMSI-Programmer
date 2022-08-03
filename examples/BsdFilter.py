from __future__ import print_function
from multiprocessing import current_process
from reprlib import recursive_repr
import marplotlib.pyplot as plt 
import matplotlib.animation as animation
from matplotlib import style
import can 
import numpy as np
bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)
bus.set_filters([{"can_id": 0x11, "can_mask": 0x7FF, "extended":False}])
recorder = can.BufferedReader()
notifier = can.Notifier(bus,[recorder])
data = np.array([])
data_point = 0
max_data_points = 1000
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
plt.ylabel('y')
plt.xlabel('x')
plt.grid(True)
x = []
y = []
def animate(u,x,y):
    recv_msg=recorder.get_message()
    if recv_msg !=None:
        speed = recv_msg.data[1]*256+recv_msg.data[2]
        speed = float(speed)/256
        if len(x) > 1000:
            x.pop(0)
            y.pop(0)
            global data_point
            current_point = data_point
            x.append(current_point)
            y.append(speed)
            data_point = data_point +1
    print(y)
    ax1.plot(x,y)
    ax1.clear()
    plt.xlabel('Sample')
    plt.ylabel('Speed [km/hr]')
    plt.grid(True)
    plt.xticks(rotation=45, ha='right')
ani = animation.FuncAnimation(fig, animate, fargs=(x,y), interval=1)
plt.show()