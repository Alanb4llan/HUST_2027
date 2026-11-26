# -*- coding: utf-8 -*-
"""
Created on Sat May 16 13:12:28 2026

@author: oscar
"""

import serial
import time

ser = serial.Serial('COM4', 9600)

while True:
    ser.write(b'Hello from virtual port\n')
    time.sleep(1)
    
