# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 13:32:36 2026

@author: oscar
"""

from Strategi.INDATA import *
from Strategi.FORB import *
from Strategi.SOLBIL import *

"""
Första raden är första kolumnen i “LORA” programmen.

0 = LoRa.print(velocity); LoRa.print(" "); 
1 = LoRa.print(distance_travelled); LoRa.print(" "); 
2 = LoRa.print(battery_volt); LoRa.print(" ");
3 = LoRa.print(battery_current); LoRa.print(" ");
4 = LoRa.print(battery_cell_LOW_volt); LoRa.print(" "); LoRa.print(battery_cell_HIGH_volt); LoRa.print(" "); LoRa.print(battery_cell_AVG_volt); LoRa.print(" "); LoRa.print(battery_cell_LOW_temp); LoRa.print(" "); LoRa.print(battery_cell_HIGH_temp); LoRa.print(" "); LoRa.print(battery_cell_AVG_temp); LoRa.print(" "); LoRa.print(battery_cell_ID_HIGH_volt); LoRa.print(" "); LoRa.print(battery_cell_ID_LOW_volt); LoRa.print(" "); 
5 = LoRa.print(BMS_temp); LoRa.print(" "); LoRa.print(BATTERY_WATTHOURS_SINCE_START); LoRa.print(" "); LoRa.print(motor_current); LoRa.print(" "); 
6 = LoRa.print(motor_temp); LoRa.print(" ");
7 = LoRa.print(motor_controller_temp); LoRa.print(" "); 
8 = LoRa.print(MPPTInputPower1); LoRa.print(" "); 
9 = LoRa.print(MPPTInputPower2); LoRa.print(" "); 
10 = LoRa.print(MPPTInputPower3); LoRa.print(" "); 
11 = LoRa.print(MPPTInputPower4); LoRa.print(" ");
12 = LoRa.print(MPPTOutputPower1); LoRa.print(" "); 
13 = LoRa.print(MPPTOutputPower2); LoRa.print(" ");
14 = LoRa.print(MPPTOutputPower3); LoRa.print(" "); 
15 = LoRa.print(MPPTOutputPower4); LoRa.print(" "); 
16 = LoRa.print(MPPT_total_watt_out);
"""

"""
För att simulera datan som finns från LORA ska man kolla på 
de första 48972.15 meterna 
"""
# Jämför med det som står i MATLAB-filen "DataRace20250824..."
# Om det står 1 där är det 0 här (n blir n-1)

# 0 är hastighet
# 1 är distans
# 2 är Batteri spänning
# 3 är Batteri Ström

# 4 - 6 är okända

# 7 - 9 är troligtvis temperaturer

# 10 & 11 är okända

# 12 är troligtvis en temperatur

# 13 är Batteri konsumption
# 14 är Motor-ström

# 17 är MPPT1in
# 18 är MPPT2in
# 19 är MPPT3in
# 20 är MPPT4in
# 21 är MPPT1ut
# 22 är MPPT2ut
# 23 är MPPT3ut
# 24 är MPPT4ut
# 25 är MPPT_tot

"""
Skippa avläsningen från lorafilerna, använd de från SD-korten istället
"""

#lora13 = open_loras("58+57")

#lora_namn = get_loras("58+57")

#SD_n = open_SD(get_SDs("84")[0])

# I Falkenberg 2026-02-25 är log filerna 120 - 124
#SD_n = open_SD(get_SDs(124, "DataFalkenberg")[0], "DataFalkenberg")
#print(SD_n)

SD_n = []

def plot_from_list(lista = SD_n, index = 0):
    vals = []
    for item in lista:
        try:
            vals.append(float(item[index]))
        except IndexError:
            pass
    plt.figure(figsize=(11, 5), dpi=100)
    plt.plot(vals)
    plt.show()
    
    
def plot_list_w_time(lista = SD_n, index = 0):
    vals = []
    times = []
    curr_time = dt.datetime(2025,8,24,8,27,0)
    for item in lista:
        try:
            vals.append(float(item[index]))
            times.append(curr_time)
        except IndexError:
            pass
        curr_time += dt.timedelta(seconds = 1)
    plt.figure(figsize=(11, 5), dpi=100)
    plt.plot(times, vals, "b")
    plt.show()
    
def plot_sd_x_y(lista = SD_n, index1 = 0, index2 = 1):
    vals1 = []
    vals2 = []
    for item in lista:
        try:
            vals1.append(float(item[index1]))
            vals2.append(float(item[index2]))
        except IndexError:
            pass
    plt.figure(figsize=(11, 5), dpi=100)
    plt.plot(vals1, vals2, "b")
    plt.show()
    return sum(vals2)/len(vals2)
    
def plot_mult_sd(lista = SD_n, ix = 0, iy1 = 1, iy2 = 2):
    s = 0
    xals = []
    yals = []
    for item in lista:
        try:
            y = float(item[iy1])*float(item[iy2])
            xals.append(float(item[ix]))
            yals.append(y)
            s += y
        except IndexError:
            pass
    plt.figure(figsize=(11, 5), dpi=100)
    plt.plot(xals, yals, "b")
    plt.show()
    return s/len(xals)


with open('LORAdata.csv', 'w', newline = '\n') as file:
    spamwrite = csv.writer(file, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for item in SD_n:
        spamwrite.writerow(item)

n = 0
alla = []
values = []

with open('LORAdata.csv', 'r', newline = '\n') as file:
    spamreader = csv.reader(file, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for item in spamreader:
        alla.append(item)
        try:
            values.append(float(item[n]))
        except (ValueError, IndexError):
            pass
            #print(item)
        

"""     
time = np.linspace(1, len(values), len(values))

plt.figure(figsize=(11, 5), dpi=100)
plt.plot(time, values, "r")

plt.show()
"""

#plot_total_power(henry)

#add_session("LoRa")

