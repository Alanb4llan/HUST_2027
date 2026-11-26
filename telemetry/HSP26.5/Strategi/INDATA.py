# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 20:23:12 2025

@author: Oscar Osbeck
"""

import csv
import os
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#from sessions import *

#Detta är en klass för alla stop längs vägen
class road_stops():
    def __init__(self, places, total_distance, time_arrived, time_leave, control_open, control_close, time_at_stop):
        self.places = places
        self.total_distance = total_distance
        self.time_arrived = time_arrived
        self.time_leave = time_leave
        self.control_open = control_open
        self.control_close = control_close
        self.time_at_stop = time_at_stop
        self.velocities = []
        self.drive_times = []

#Detta är en (inaktuell) funktion som läser in solstrålningen i Darwin
def ghi_list():
    ghi = []
    with open('radiation_and_weather_forecast_Darwin.csv', 'r', newline = '') as file:
        spamreader = csv.reader(file, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for item in spamreader:
            #print(item)
            if item[0] == 'ghi':
                ghi.append(item[6:8])
            else:
                date = dt.datetime.strptime(item[6][:10], '%Y-%m-%d')
                hour = int(item[6][11:13])
                minute = int(item[6][14:])
                #print(minute)
                n_date = date.replace(hour = hour, minute = minute)
                #print(n_date)
                app_item = [n_date, item[7]]
                ghi.append(app_item)
            
        file.close()
    return ghi

#Denna funktion hämtar namnen på alla filer i en mapp
def get_lines(mapp_namn = "solkoordinater"):
    current = os.getcwd()
    path = current + '\\' + mapp_namn
    path = os.path.realpath(path)
    lines = os.listdir(path)
    return list(dict.fromkeys(lines))

# Följande funktion hämtar namnen på alla filer "LORA00XX.TXT"
def get_loras(fil = 13, mapp_namn = "Rawdata_20250824"):
    Loras = get_lines(mapp_namn)
    rets = []
    for fil_namn in Loras:
        if str(fil) in fil_namn:
            rets.append(fil_namn)
    return rets

def get_SDs(fil = 13, mapp_namn = "DataSD"):
    SDs = get_lines(mapp_namn)
    rets = []
    for fil_namn in SDs:
        if str(fil) in fil_namn:
            rets.append(fil_namn)
    return rets

# Denna funktion öppnar filerna från funktionen ovan
# och lägger in alla värden i en lista
def open_loras(fil = 13, mapp_namn = "Rawdata_20250824"):
    loras = get_loras(fil, mapp_namn)
    info = []
    for item in loras:
        print(item)
        with open(mapp_namn +'\\'+ item, 'r', encoding='utf-8', newline = "\n") as file:
            line = None
            try:
                line = file.readline()
            except UnicodeDecodeError:
                pass
            size = os.path.getsize(mapp_namn +'\\'+ item)
            i = 0
            print(size)
            while line != None and i <= size:
                i+= 1
                info.append(line.split())
                try:
                    line = file.readline()
                    #print(line)
                except UnicodeDecodeError:
                    continue
    return info

def open_SD(fil = 84, mapp_namn = "DataSD"):
    SD = get_SDs(str(fil), mapp_namn)
    print(SD)
    info = []
    for item in SD:
        print(item)
        with open(mapp_namn +'\\'+ item, 'r', encoding='utf-8', newline = "\n") as file:
            line = None
            try:
                line = file.readline()
            except UnicodeDecodeError:
                pass
            size = os.path.getsize(mapp_namn +'\\'+ item)
            i = 0
            print(size)
            while line != None and i <= size:
                i+= 1
                info.append(line.split())
                try:
                    line = file.readline()
                    #print(line)
                except UnicodeDecodeError:
                    continue
    return info

# Hämtar alla väderdata för en viss koordinat
def ghi_line_list(line):
    ghi = []
    with open('solkoordinater/'+line, 'r', newline = '') as file:
        spamreader = csv.reader(file, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for item in spamreader:
            #print(item)
            ghi.append(item)
        file.close()
    return ghi

# Gör en pandas.DataFrame för alla kontrollstopp
def control_stop():
    lista_kalkylark = []
    namn_kalkylark = []
    lines = ['Control stop 2025.xlsx']
    for i in range(len(lines)):
        if namn_kalkylark.count(lines[i][1:-5]) < 1:
            Ex_Ark = pd.ExcelFile(lines[i])
            temp_ark = [Ex_Ark.parse(item) for item in Ex_Ark.sheet_names]
            lista_kalkylark.append([lines[i][:-5],temp_ark])
            namn_kalkylark.append(lines[i][0:-5])
    return lista_kalkylark[0][1][0]

#Räknar ut koordinaterna för alla kontrollstopp
# Har alternativ för att plotta koordinaterna
def control_stop_coordinates(plot = False):
    lista = []
    with open('Positioner_stop.csv', 'r', newline = '') as file:
        spamreader = csv.reader(file, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for item in spamreader:
            lista.append(item)
    if plot:
        X = []
        Y = []
        for l in lista[1:]:
            X.append(float(l[1]))
            Y.append(float(l[2]))
        x = np.array(X)
        y = np.array(Y)
        plt.plot(x, y, "r*-")
        plt.show()
    return lista

# Hämtar namn på stopp samt aktuell väderdatafil
def coord_to_name():
    lines = get_lines() # Hämtar alla namn på väderfiler
    #print(len(lines))
    cs = control_stop_coordinates() # Hämtar koordinater för stoppen
    #print(len(cs))
    names = []
    i = 0
    for line in lines:
        l = False
        for c in cs:
            # Kollar om koordinaterna finns i namnet på värderfilen
            if c[1] in line and c[2] in line: 
                names.append([c[0], c[3], line])
                l = True
        #if not l:
            #print(line)
    return names

"""
Följande funktion läser in txt filer med koordinater och höjder
"""

file_name_1 = "Elevation_Stuart_Highway.txt"

# Läser in höjddata från hela streckan
# OBS!!! Använder en förenklad version för identifiering, bör uppgraderas framåt
def read_txt(file_name):
    read = []
    with open(file_name, 'r') as file:
        i = 0
        for line in file:
            content = line.strip()
            #print(content)
            if(i >= 1):
                items = []
                items.append(float(content[2:13]))
                items.append(float(content[16:27]))
                items.append(float(content[30:35]))
                read.append(items)
            i += 1
    return read


"""
#Funktion för följande finns i "DISTANS"

CS = control_stop()

lista = []

for item in CS:
    lista.append(CS[item])

RS = road_stops(lista[0], lista[1], lista[5], lista[6], 
                lista[7], lista[9], lista[11])

        
speed_list = [60]*len(RS.places)
"""

#d = date_time_converter(RS.control_close[3])

#add_session("INDATA")

