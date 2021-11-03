from matplotlib import pyplot as plt
from collections import deque
from threading import Lock, Thread
import numpy as np
import serial
import csv
import re
import time
from datetime import datetime
import timeit

SERIAL_PORT_f = 'COM2'
SERIAL_RATE_f = 115200

SERIAL_PORT_p = 'COM5'
SERIAL_RATE_p = 2000000

def main():
    n = 2000
    d = np.zeros((n, 2))
    ser_p = serial.Serial(SERIAL_PORT_p, SERIAL_RATE_p)
    ser_f = serial.Serial(SERIAL_PORT_f, SERIAL_RATE_f)

## reading force and pressure data

    ser_f.write(b'CV 4\r') # command for the ATI force sensor to send Z-axis force data
    start = timeit.default_timer()  ## for printing time if the test if necessary 
    for i in range(n):
    	ser_f.write(b'QR\r') # command for receiving force data
    	e = ser_f.inWaiting()
    	time.sleep(0.004)
    	g = ser_f.read(e).decode('ascii')
    	f = re.sub(r'[-\n,QR, CV, >, , \r]', "", g) # omitting unnecessar characters that the force sensor sends with the data
    	a = ser_p.readline().decode('ascii') # reading the combined pressure data
    	if f != "" and a != "":
        	d[i,0] = float(f)
        	d[i,1] = float(a)
    stop = timeit.default_timer()   # for printing time if the test if necessary 

## converting the 9 digit number of pressures to individual pressures of fingers

    data = np.zeros((n, 4))
    for i in range(n):
        num = d[i,1]
        data[i,0] = num % 1000 ##pressure of index finger
        num1 = num // 1000
        data[i,1] = num1 % 1000  ##pressure of thumb
        num2 = num1 // 1000
        data[i,2] = num2 % 1000  ##pressure of middle
        data[i,3] = d[i,0]  ##force

## saving the data points as a csv file

    np.savetxt("FP_test1.csv", data, delimiter=",")    
                 
if __name__ == '__main__':
  main()

