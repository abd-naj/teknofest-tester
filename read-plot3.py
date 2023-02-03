import serial
import time
import matplotlib.pyplot as plt
import numpy as np
from drawnow import *
import re
from wrtie_xlxs import wirteToXlxs
import random


cnt = 0
ld1Array = []
ld2Array = []

srRate = 9600
z1port = 'COM4'  # set the correct port before run it

z1serial = serial.Serial(port=z1port, baudrate=srRate)
z1serial.timeout = 2  # set read timeout
# print z1serial  # debug serial.
print(z1serial.is_open)  # True for opened

plt.ion()
filName = 'test' + str(random.randint(1, 5000)) + '.xlsx'
# filName = 'test1.xlsx'
def writeData(dataLd1, dataLd2, speed, time):
    print('writeData')
    print(filName)
    # wirteToXlxs(filName)
    wirteToXlxs(filName).write(dataLd1, dataLd2, speed, time)

def makeFig():
    # plt.ylim()
    plt.grid(True)
    plt.ylabel('ld1')
    plt.title('LD1 + LD2')
    plt.plot(ld1Array, 'r-')
    plt.legend(loc='upper left')
    plt2 = plt.twinx()
    plt2.plot(ld2Array)


if z1serial.is_open:
    while True:
        size = z1serial.inWaiting()
        if size:
            a = z1serial.readline(12)
            dataArray = [int(s) for s in re.findall(r'\b\d+\b', str(a))]
            print(dataArray)
            ld1 = float(dataArray[0])
            speed = 0
            if len(dataArray) < 2:
                break
            ld2 = float(dataArray[1])
            ld1Array.append(ld1)
            ld2Array.append(ld2)
            writeData(ld1, ld2, speed, time.time())
            drawnow(makeFig)
            plt.pause(0.1)
            cnt = cnt + 1
            if (cnt > 12):
                ld1Array.pop(0)
                ld2Array.pop(0)
else:
    print('z1serial not open')


# z1serial.close()  # close z1serial if z1serial is open.

# write excel file

