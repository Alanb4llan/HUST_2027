# -*- coding: utf-8 -*-
"""
Created on Tue May 19 08:46:53 2026

@author: oscar
"""

"""
Denna modul innehåller funktioner för datainläsningen(Receiver.py)
"""

"""
Förbättring:
    Tydligare dokumentation vilka index som avser vilka värden,
    i dagsläget har jag fått lägga mycket tid på att lista ut vad värdena
    representerar.
    I dagsläget behöver man leta i olika filer(oklart vilka!) och gissa
    vilka värden som är vad. Det är även oklart vart i programmet värdena finns
    Detta bör lösas med tydlig dokumentation i form av en rapport där det
    tydligt framkommer vilka värden som innehåller vilken data.
    Måste vara tydligt om det avser LoRa eller SD-kortet
    Namnen som står i ex Arduino sketch_may5a, MATLAB: SDcard_data, 
        samtliga matcher inte datan som analyserats från SD-kortet
"""

import os
import matplotlib.pyplot as plt

from Strategi.INDATA import *

"""
Battery_cell_LOW_volt = M(:,5).';
Battery_cell_HIGH_volt = M(:,6).';
Battery_cell_AVG_volt = M(:,7).';

Battery_cell_LOW_temperature = M(:,8).';
Battery_cell_HIGH_temperature = M(:,9).';
Battery_cell_AVG_temperature = M(:,10).';

Battery_cell_HIGH_ID = M(:,11).';
Battery_cell_LOW_ID = M(:,12).';

% System temperatures, excluding battery cells
BMS_temperature = M(:,13).';
Motor_temperature = M(:,15).';
Motor_controller_temperature = M(:,16).';

% Solar power generation from each MPPT
MPPT1out = M(:,17).';
MPPT2out = M(:,18).';
MPPT3out = M(:,19).';
"""

# Kommentarerna avser numreringen i MATLAB, python kronologisk om inte annat står
SD_data_titlar = ["Hastighet", #1, 0
               "Distans",
               "Batteri Spänning",
               "Batteri Ström",
               
               "Battery_cell_LOW_volt", #5, 4
               "Battery_cell_HIGH_volt",
               "Battery_cell_AVG_volt",

               "Battery_cell_LOW_temperature", #8, 7
               "Battery_cell_HIGH_temperature",
               "Battery_cell_AVG_temperature",

               "Battery_cell_HIGH_ID", #11, 10
               "Battery_cell_LOW_ID",
               
               "BMS_temperature", #13, 12
               "Motor_temperature", #15, 13
               "Motor_controller_temperature", #16, 14
               
               "MPPT1out", #17, 15
               "MPPT2out", 
               "MPPT3out", #,17
               "Okänd",
               "Okänd",
               "Okänd",
               "Okänd",
               "Okänd",
               "Okänd",
               "Okänd",
               "Okänd",
               "Okänd",
               "Okänd",
               "Okänd"
               ]

Lora_data_titlar = ["VehicleVelocity",
                    "Distance",
                    "TotMPPT",
                    "PackVoltage",
                    "PackCurrent",
                    "InternalTempBMS",
                    "LowCellVoltage",
                    "HighCellVoltage",
                    "AverageCellVoltage",
                    "CellLowTemperature",
                    "CellLowTemperature_ID",
                    "CellHighTemperature",
                    "CellHighTemperature_ID",   
                    "CellAverageTemperature",
                    "MotorCurrent",
                    "MotorTemp",
                    "HeatSinkTemp",
                    "MPPTOutputPower1", 
                    "MPPTOutputPower2",
                    "MPPTOutputPower3",
                    "MPPTOutputPower4",
                   "Okänd",
                   "Okänd",
                   "Okänd",
                   "Okänd",
                   "Okänd",
                   "Okänd",
                   "Okänd",
                   "Okänd",
                   "Okänd",
                   "Okänd",
                   "Okänd"]

MATLAB_data_titlar = ["hastighet",
                 "distans",
                 "batteri spänning",
                 "batteri ström",
                 "batteri_cell låg",
                 "batteri cell hög spänninf",
                 "batteri cell snitt volt",
                 "batteri cell låg temp",
                 "batteri cell hög temp",
                 "batteri cell snitt temp",
                 "batteri cell id låg",
                 "BMS temp",
                 "motor ström",
                 "motor temp",
                 "motor controller temp",
                 "MPPT input power 1",
                 "MPPT input power 2",
                 "MPPT input power 3",
                 "MPPT input power tot",
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd"]

"""
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
print("MPPT output power tot: " + info_vec[25] +"V") # nr 290
"""

ManuellSD = ["Hastighet(Stämmer)", # 0
                 "Distans(Stämmer)", # 1
                 "Batteri spänning(Stämmer)", # 2
                 "Batteri ström(Stämmer)", # 3
                 "batteri_cell låg(Troligen)", # 4
                 "batteri cell hög spänninf(Troligen)", # 5
                 "batteri cell snitt volt(Troligen)", # 6
                 "batteri cell låg temp(Kanske)", # 7
                 "batteri cell hög temp(Kanske)", # 8
                 "batteri cell snitt temp(Kanske)", # 9
                 "batteri cell id låg(Kanske)", # 10
                 "BMS temp(??)", # 11
                 "Okänd", # 12, indexförskjutning
                 "Ström Motor(Stämmer)", # 13
                 "motor controller temp(Troligen)", # 14
                 "Temperatur Batteri(Troligen)", # 15
                 "MPPT input power 1(Stämmer)", # 16
                 "MPPT input power 2(Stämmer)", # 17
                 "MPPT input power 3(Stämmer)", # 18
                 "Okänd", # 19
                 "MPPT 1(??)", # 20
                 "MPPT 2(??)", # 21
                 "MPPT 3(??)", # 22
                 "Okänd",
                 "MPPT Tot(??)", # 24
                 "Okänd",
                 "Okänd",
                 "Batteri Effekt", #27
                 "Motor Effekt", # 28
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd"]


ManuellLora = ["Hastighet", # 0
                 "Distans", # 1
                 "Batteri spänning", # 2
                 "Batteri ström", # 3
                 "Batteri_cell låg", # 4
                 "Batteri cell hög spänninf", # 5
                 "Batteri cell snitt volt", # 6
                 "Batteri cell låg temp", # 7
                 "Batteri cell hög temp", # 8
                 "Batteri cell snitt temp", # 9
                 "Batteri cell id låg", # 10
                 "BMS temp", # 11
                 "Okänd", # 12
                 "Okänd", # 13, indexförskjutning gämfört med SD-kortet
                 "Ström Motor", # 14
                 "Motor controller temp", # 15
                 "Temperatur Batteri", # 16
                 "MPPT input power 1", # 17
                 "MPPT input power 2", # 18
                 "MPPT input power 3", # 19
                 "Okänd", # 20
                 "MPPT 1(??)", # 21
                 "MPPT 2(??)", # 22
                 "MPPT 3(??)", # 23
                 "Okänd",
                 "MPPT Tot(??)", # 25
                 "Batteri Effekt", #26
                 "Motor Effekt", #27
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd"]

EnheterLora = ["km/h", # 0
                 "meter", # 1
                 "Volt", # 2
                 "Ampere", # 3
                 "Volt", # 4
                 "Volt", # 5
                 "Volt", # 6
                 "Celcius", # 7
                 "Celcius", # 8
                 "Celcius", # 9
                 "Batteri cell id låg", # 10
                 "Celcius", # 11
                 "Okänd", # 12
                 "Okänd", # 13, indexförskjutning gämfört med SD-kortet
                 "Ampere", # 14
                 "Celsius", # 15
                 "Celsius", # 16
                 "Watt", # 17
                 "Watt", # 18
                 "Watt", # 19
                 "Okänd", # 20
                 "Watt", # 21
                 "Watt", # 22
                 "Watt", # 23
                 "Okänd",
                 "Watt", # 25
                 "Watt", #26
                 "Watt", #27
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd",
                 "Okänd"]

#Räknar ut konsumptionen i lista från txtfil
def get_battery_effekt(data_lista, step = 4):
    new_list = []
    for item in data_lista:
        val = item
        try:
            if len(item) >= 14:
                #print(item[2+step]+ " "+item[3+step])
                val.append(str(float(item[2+step][:-1])*float(item[3+step][:-1])))
                #print(val)
                new_list.append(val)
        except ValueError:
            new_list.append(item)
    return new_list


def get_motor_effekt(data_lista, Lora = False, step = 0):
    new_list = []
    for item in data_lista:
        val = item
        try:
            if len(item) >= 15+step and Lora:
                val.append(str(float(item[2+step][:-1])*float(item[14+step][:-1])))
                #print(val[-1])
                new_list.append(val)
            elif len(item) >= 14+step and not Lora:
                val.append(str(float(item[2+step][:-1])*float(item[13+step][:-1])))
                #print(val)
                new_list.append(val)
        except ValueError:
            pass
    return new_list

def get_motor_and_battery(data_lista, Lora = False, step = 0):
    lista = get_battery_effekt(data_lista, step)
    lista = get_motor_effekt(lista, Lora, step)
    #print(lista[-3:])
    return lista

def get_lines_string(string, ret_all = False):
    current = os.getcwd()
    path = current
    path = os.path.realpath(path)
    lines = os.listdir(path)
    rets = []
    for item in lines:
        if string in item and item[-4:] == ".txt":
            rets.append(item)
    if ret_all:
        return list(dict.fromkeys(lines))
    return rets


def string_to_vec(string):
    vec = []
    strs = ""
    for s in string:
        if s == " ":
            vec.append(strs)
            strs = ""
        else:
            strs += s
    vec.append(strs)
    return vec
    
# Modul för att läsa in data från falkenberg, första 2 provvarven
def read_datas(): 
    data = []
    for i in range(len(get_lines("data")) -1 ):
        with open("data"+str(i)+".txt", "r") as file:  
            #print(file)
            
            datan = file.readlines()
            for item in datan:
                data.append(item)
    dataret = []
    for item in data:
        dataret.append(string_to_vec(item))
    return data
    
def plot_vals(datalist, index = 0, title = ""):
    plotl = []
    for d in datalist:
        plotl.append(d[index])
    plt.title(title)
    plt.plot(plotl)
    plt.show()
        














