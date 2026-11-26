# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 16:37:53 2026

@author: oscar
"""

from LORA import *
from RESA import *

g = 9.798 #konstanten för Australien
# g har enheten m / s^2
# rho mäts i kg/m^3
# speed mäts i m/s
# drag_koeff är ett tal
# fron_area mäts i m^2
# drag 
# weight(vikt) mäts i kg
# rullmotstånd per hjul är en skalär

"""
aerodynamic_resistance(rho, speed, drag_koeff, front_area)
    resistance = 1/2 * rho * speed**2 * drag_koeff * front_area 

rolling_resistance(total_weight, rolling_res_per_wheel, num_wheels = 3):
    res = rolling_res_per_wheel * g*total_weight  

gradient_resistance(alpha, mass):
    resistance = mass*g * m.sin(alpha) 
    
adj_power(speed, drag, total_weight, rolling_res_per_wheel, alpha, efficiency):
    F_D = aero_resistance(speed, drag)
    F_R = rolling_resistance(total_weight, rolling_res_per_wheel)
    F_Gr = gradient_resistance(alpha, total_weight)
    v = speed # m/s
    u = efficiency 
    consumption = (F_D + F_R + F_Gr)*v/u     # W = kg*m^2/s^3
    
acc = acceleration
comsump = (1/2 * rho * speed**2 * drag_koeff * front_area + rolling_res_per_wheel * g*total_weight
           + mass*g * m.sin(alpha) + mass*acc)*v/u
"""


def plot_total_power(solar_car):
    vals = []
    times = []
    total_est = 0
    total_act = 0
    tot_error = 0
    
    resultat = [] # Fylls med resultatsförbrukningen
    estimat = []  # Fylls med estimat för alla delarna av förbrukningen
    
    weight = solar_car.weight #kg
    rolling_rest = rolling_resistance(solar_car.weight, solar_car.rolling_res_per_wheel)
    efficiency = solar_car.efficiency_my
    rho = solar_car.rho
    drag = solar_car.drag
    front_area = solar_car.front_area
    # Om man ändrar listan måste man kolla indexen
    lista = open_SD(get_SDs("84")[0]) 
    curr_time = dt.datetime(2025,8,24,8,27,0)
    i = 0
    
    forbs = []
    for item in lista:
        try:
            speed = float(item[0]) # i m/s
            acc = 0
            if i >= 1:
                acc = speed - float(lista[i-1][0]) # Tar den senaste hastigheten - den tidigare
            alpha = 0
            power = total_power(speed, solar_car, alpha, acc)
            
            # Räknar ut estimaten för komposanterna för förbrukningen
            P_Aero = aero_power(speed, solar_car)
            P_Gr = gradient_power(speed, solar_car, alpha)
            P_Rr = rolling_power(speed, solar_car)
            P_Acc = acc_power(speed, solar_car, acc)
            #estimat.append([P_Aero, P_Gr, P_Rr, P_Acc])
            estimat.append([P_Aero, P_Rr, P_Acc]) # Skippar gradientmotståndet för enkelhetens skull
            
            #vals.append(power)
            #vals.append(P_Aero*-0.334 + 7.67*P_Rr + 0.191*P_Acc) #Från MKM
            #power = P_Aero*0.6 + 0.9*P_Rr + 0.7*P_Acc # Manuell testning
            power = 0.75*power
            
            # Kontrollerar om förbrukningen är noll
            if power < 0:
                power = 0
            vals.append(power)
            total_est += power/3600 #Omvandla till Wh
            
            # motor_current(13) * battery_voltage(2) = förbrukning 
            forb = float(item[13])*float(item[2]) 
            total_act += forb/3600 #Omvandla till Wh
            forbs.append(forb)
            resultat.append(forb)
            
            tot_error += abs(forb-power)/3600 #Omvandlas till Wh
            
            
            times.append(curr_time)
        except IndexError:
            pass
        i += 1
        curr_time += dt.timedelta(seconds = 1)
        
    print("Total förväntad förbrukning: " + str(round(total_est,2)) +"Wh")
    print("Total faktisk förbrukning: " + str(round(total_act,2)) +"Wh")
    print("Total felberäkning i förbrukning: " + str(round(tot_error,2)) +"Wh")
    
    plt.figure(figsize=(11, 5), dpi=100)
    plt.plot(times, vals, "b")
    plt.plot(times, forbs, "r")
    plt.show()
    
    return estimat, resultat



E, R = plot_total_power(henry)

A = np.array(E)
At = A.transpose()
Y = np.array(R)

X = np.linalg.inv(At@A)@At@Y # Provar vi med denna metoden får vi helt orimliga resultat




