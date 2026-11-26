# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 20:36:56 2025

@author: Oscar Osbeck
"""

"""
Detta programmet arbetar med strålning och solproduktion

Länk till Solcast video kommer från dokumentet "Annas anteckningar" i 
Google drive -> HUST -> HUST 2025 -> EL -> Strategi Australien 
länken är: https://www.youtube.com/watch?v=aYrd7EGNOlQ&t=192s 

"""

#from INDATA import *
from DISTANS import *


#Följande två funktioner är äldre gamla funktioner som berör beräkningen av strålningen

def radiation_est(pos, clock_time = 12):
    #Gör ett estimat på strålningen
    top_rad = (90 - 0.0066*pos)*10
    radiation = top_rad * 2.7182818**(-(clock_time - 12)**2/14)
    return radiation

def radiation_data(clock_time, ghi, num_day = 0):
    #Räknar ut strålningen utifrån data
    #ghi ska vara en lista
    for item in ghi[(1+num_day*288):]:
        #print(item[0])
        ghi_time = item[0].hour + item[0].minute/60
        if abs(ghi_time - clock_time) <= 1/11:
            return int(item[1])
    return 0

#Funktion för viktning av strålning givet position mellan två mätvärden
def radiation_weight(position, pos1, pos2, g1, g2):
    p = position
    x1 = position - pos1
    x2 = pos2 - position
    m = g1
    k = (g2-g1)/(pos2-pos1)
    y = k*x1+m
    if x1 < 0 or x2 < 0: # Kollar att positionen är mellan koordinaterna
        y = 0
    return y

def get_ghis(file_names, position):
    pos1 = 0
    pos2 = 0
    for f in range(1, len(file_names)):
        if float(file_names[f-1][1]) <= position <= float(file_names[f][1]):
            ghi1 = ghi_line_list(file_names[f-1][2])
            ghi2 = ghi_line_list(file_names[f][2])
            pos1= float(file_names[f-1][1])
            pos2= float(file_names[f][1])
            #print(file_names[f-1][2])
    
    return ghi1, ghi2, pos1, pos2

#Beräknar strålningen utifrån datan
def radiation_data_est(date, position, file_names, ghi1, ghi2, pos1, pos2, start_idx = 1, ghi_num = 5):
    g1 = 0
    g2 = 0
    #hours = int(clock_time)
    #minutes = int((clock_time-hours)*60) - int((clock_time-hours)*60)%5
    #print(date+" "+str(hours) +" "+str(minutes)+" "+str(seconds)) 
    #ndate = dt.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    #ndate += dt.timedelta(hours = hours, minutes = minutes)
    sub_min = date.minute%5
    ndate = date - dt.timedelta(minutes = sub_min, seconds = date.second, microseconds= date.microsecond)
    #print(ndate)
    end_idx = start_idx
    i = start_idx
    i1date = dt.datetime.strptime(ghi1[i][-2] , "%Y-%m-%dT%H:%M:%S+00:00")
    i2date = dt.datetime.strptime(ghi2[i][-2] , "%Y-%m-%dT%H:%M:%S+00:00")
    if ndate == i1date == i2date:
        g1 = float(ghi1[i][ghi_num])
        g2 = float(ghi2[i][ghi_num])
        #print("Position "+str(position))
    else:
        #print(i1date)
        #print(i2date)
        #print(clock_time)
        #print(ndate)
        while i < len(ghi1):
        #for i in range(start_idx, len(ghi1)):
            item = ghi1[i]
            idate = dt.datetime.strptime(item[-2], "%Y-%m-%dT%H:%M:%S+00:00")
            if idate == ndate:
                g1 = float(item[ghi_num])
                end_idx = i
                #print(end_idx)
                #print(start_idx)
            i+=1
        i = start_idx
        while i < len(ghi2):
        #for i in range(start_idx, len(ghi2)):
            item = ghi2[i]
            idate = dt.datetime.strptime(item[-2], "%Y-%m-%dT%H:%M:%S+00:00")
            if idate == ndate:
                g2 = float(item[ghi_num])
                end_idx = i
                i = len(ghi2)
            i+=1
        
    y = radiation_weight(position, pos1, pos2, g1, g2)
    
    # Kollar så att positionen är på banan, jag sätter 3200 så det finns lite marginal
    if position > 3200:
        y = 0
    
    #print("Position "+str(position)+" index: "+str(end_idx))
    return y, end_idx
    
#rde = radiation_data_est("2025-08-02", 5.332, 1900.23, coord_to_name())




#####

def production_data(pos, time, clock, solar_car, ghi, num_day = 0):
    #time ska anges i sekunder
    #prod = radiation_est(pos, clock) * solar_car.eff_factor * time
    prod = radiation_data(clock, ghi, num_day) * solar_car.eff_factor * time * solar_car.solar_area #/6
    return prod

def production_data_est(pos, time, solar_car, date, file_names, ghi1, ghi2, pos1, pos2, start_idx):
    #time ska anges i sekunder
    #stral är strålningen som mäts i W/m^2
    stral, idx = radiation_data_est(date, pos, file_names, ghi1, ghi2, pos1, pos2, start_idx)
    prod = stral * solar_car.eff_factor * time * solar_car.solar_area # du kan behöva dela med 3.6 för omvandlig mellan km/h och m/s
    #svaret är i Ws
    return prod, idx
    
def production_list(distance_list, speed, solar_car, clock = 12):
    prod_list = []
    num_day = 0
    first = distance_list[0]
    ghi = ghi_list()
    for i in range(1, len(distance_list)):
        curr = distance_list[i]
        time = 1000*abs(curr[0] - first[0])/(speed*3.6)
        prod_list.append(production_data(curr[0], time, clock, solar_car, ghi, num_day))
        first = curr
        clock += time/3600
        if clock >= 17:
            clock = 8
            num_day += 1
            #print("Dag: " +str(num_day))
        #print(time)
    return prod_list

def sum_production(distance_list, speed, solar_car, clock = 12):
    return sum(production_list(distance_list, speed, solar_car, clock))

def even_production(distance_list, speed, num_sections, solar_car):
    even_sec = get_even_sections(distance_list, num_sections)
    sec_len = distance_list[-1][0]/num_sections
    sec_time = sec_len/(speed*3.6) #Enheterna är km och m/s
    prod_list = []
    clock = 8
    #print(sec_time)
    num_day = 0
    for sec in even_sec:
        prod = sum_production(sec, speed, solar_car, clock)
        clock += sec_time
        if clock >= 17:
            clock = 8
            num_day += 1
            #print("Dag: " +str(num_day))
        prod_list.append([prod, sec[-1][0]])
    return prod_list

def section_production(distance_list, check_points, speed, solar_car):
    sections = get_sections(distance_list, check_points)
    prod_list = []
    for sec in sections:
        prod = sum_production(sec, speed, solar_car)
        prod_list.append([prod, sec[-1][0]])
    return prod_list

def sectional_production(sections, speed, solar_car):
    prod_list = []
    for sec in sections:
        prod = sum_production(sec, speed, solar_car)
        prod_list.append([prod, sec[-1][0]])
    return prod_list

def plot_production(distance_list, speed):
    plot_list = production_list(distance_list, speed, solar_car)
    X = np.array(distance_list[1:]).transpose()[0]
    Y = np.array(plot_list)
    plt.plot(X, Y, "b-")
    plt.show()
    
def plot_section_production(distance_list, check_points, speed, solar_car):
    plot_list = section_production(distance_list, check_points, speed, solar_car)
    X = np.array(plot_list).transpose()
    plt.plot(X[1], X[0], "b-")
    plt.show()
    return plot_list
    
def plot_even_production(distance_list, speed, num_secs, solar_car):
    plot_list = even_production(distance_list, speed, num_secs, solar_car)
    A = np.array(plot_list)
    X = A.transpose()[1]
    Y = A.transpose()[0]
    plt.plot(X, Y, "g-")
    plt.show()
    return A


#add_session("SOLPLAN")