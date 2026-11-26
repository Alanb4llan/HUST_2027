# -*- coding: utf-8 -*-
"""
Created on Sat May 16 13:16:09 2026

@author: oscar
"""

#import serial
import time
import datetime as dt


from .ReceiverPack import *

from .LORA import *

"""
# Detta stycket ska användas för en faktisk körning
ser = serial.Serial('COM4', 115200)

def add_point(string):
    lines = get_lines("data")
    # Ta bort str(len(lines)) för att skriva allt i filen "data.txt"
    with open("dataLora7.txt", "a") as file:  
        #print(now)
        file.writelines(string+"\n")
        time.sleep(0) # sätt till noll för 1 sekunds fördröjning
"""




"""
0, 1, 2 tid och title

Numrering från MATLAB
1 = hastighet
2 = distans
3 = batteri spänning
4 = batteri ström
5 = batteri_cell låg
6 = batteri cell hög spänninf
7 = batteri cell snitt volt
8 = batteri cell låg temp
9 = batteri cell hög temp
10 =  batteri cell snitt temp
12 = batteri cell id låg
13 = BMS temp
14 = motor ström
15 = motor temp
16 = motor controller temp
17 = MPPT input power 1
18 = MPPT input power 2
19 = MPPT input power 3
20 = MPPT input power tot

"""

datalist = []

"""
OBS! Programmet nedan fungerar inte för testkörningar eftersom serieporten är avaktiverad
"""

class read_lora:
    def __init__(self, serial_on = True, read = True):
        if serial_on:
            self.ser = serial.Serial('COM4', 115200) # Läser in data från serieporten
        self.read = read
        self.serial_on = serial_on
        self.points = []
        self.write = False
        self.SD_n = open_SD(get_SDs(124, "DataFalkenberg")[0], "DataFalkenberg")
        self.i = 770
        
        
    def add_point(self, i = 0):
        """ Denna funktionen hämtar värden från en testkörnig för att exprimentera med UI"""
        
        LORA = self.SD_n
        
        try:
            string = str(LORA[i])
        except TypeError:
            string = ""
        
        if self.write:
            with open("dataLora25.txt", "a") as file:  
                file.writelines(string+"\n")
                time.sleep(0) # sätt till noll för 1 sekunds fördröjning
        
        self.points.append(LORA[i])
        
        return string
    
    
    def read_data(self):
        if self.read:
            string = self.add_point(i=self.i)
            #print(i)
            self.i+=1
            time.sleep(0)
            now = str(dt.datetime.now())
            #string = now+" "+str(ser.readline())
            info_vec = string_to_vec(string)
            # Tid är 0, 1 och 2 är "lora data"
            """
            try:
                print("Hastighet: "+ str(float(info_vec[4])*3.6)+"km/h")
                print("Temperatur batteri: " + info_vec[19]+" grader C")
                print("Spänning batteri: " + info_vec[6] +"V") # nr 3
                print("Ström batteri: " + info_vec[7] + "A") # nr 4
                print("Batterieffekt: "+ str(round(float(info_vec[7])*float(info_vec[6]))) + "W")
                
                print("Spänning Motor: " + info_vec[6] +"V") # nr 3
                print("Ström Motor: " + info_vec[17] + "A") # nr 14
                print("Motoreffekt: "+ str(round(float(info_vec[17])*float(info_vec[6]))) + "W")
                
                print("MPPT output power 1: " + info_vec[21] +"V") # nr 17
                print("MPPT output power 2: " + info_vec[22] +"V") # nr 18
                print("MPPT output power 3: " + info_vec[23] +"V") # nr 19
                print("MPPT output power tot: " + info_vec[25] +"V") # nr 20
                
                datalist.append(info_vec)
                
                plotvals(datalist, 5)
                
            except (IndexError, ValueError):
                print("IndexError")
            """
            #print(string)
            #self.add_point(string)
            #print(len(self.points))


    
