# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 20:33:59 2025

@author: oscar
"""

import numpy as np
import matplotlib.pyplot as plt

try:
    from .DISTANS import *
except ImportError:
    try: 
        from DISTANS import *
    except ModuleNotFoundError:
        from .DISTANS import *

"""
Detta programmet fukuserar på motstånd och krafter

Källa: JU Solar Team Strategi Rapport.pdf
"""

g = 9.798 #konstanten för Australien
# g har enheten m / s^2
# rho mäts i kg/m^3
# speed mäts i m/s
# drag_koeff är ett tal
# fron_area mäts i m^2
# drag 
# weight(vikt) mäts i kg
# rullmotstånd per hjul är en skalär

# Beräknar luftmotståndet under förutsättning att drag koefficienten och frontarean är kända
def aerodynamic_resistance(rho, speed, drag_koeff, front_area):
    #Ange speed i m/s
    #Använder drag formula
    # Rho mäts i kg/m^3
    # Speed mäts i m/s
    # drag_koeff är en skalär
    # fron_area mäts i m^2
    resistance = 1/2 * rho * speed**2 * drag_koeff * front_area 
    # resultatsenheten är kg*m/s^2
    # där kg är kilogram, m är meter och s är sekunder
    return resistance

# En förenklad modell om man bara vet total drag och inte drag koefficienten
def aero_resistance(speed, drag):
    #Ange speed i m/s
    #Använder enbart drag för att använda insamlade värden
    resistance = (speed**2) * drag
    # resultatsenheten är kg*m/s^2
    # där kg är kilogram, m är meter och s är sekunder
    return resistance

# Beräknar rullmotståndet
def rolling_resistance(total_weight, rolling_res_per_wheel, num_wheels = 3):
    sum_roll_res = 0
    # Antalet hjul är inte relevant eftersom vi antar att belastningen är samma på alla hjul
    normal_force = g*total_weight  
    # normal_force har enheten kg*m/s^2
    
    #res = roll_res_coeff * normal_force
    res = rolling_res_per_wheel * normal_force
    # resultatsenheten är kg*m/s^2
    # där kg är kilogram, m är meter och s är sekunder
    return res
    
# Beräknar gradientmotståndet
def gradient_resistance(alpha, mass):
    #alpha ska anges i radianer
    resistance = mass*g * m.sin(alpha) 
    # resultatsenheten är kg*m/s^2
    # där kg är kilogram, m är meter och s är sekunder
    return resistance

def power(rho, speed, drag, front_area, total_weight, rolling_res_per_wheel, alpha, efficiency):
    #alpha ska anges i radianer
    #Ange speed i m/s
    F_D = aerodynamic_resistance(rho, speed, drag, front_area)
    F_R = rolling_resistance(total_weight, rolling_res_per_wheel)
    F_Gr = gradient_resistance(alpha, total_weight)
    # Samtliga ovan har enheterna kg*m/s^2
    # där kg är kilogram, m är meter och s är sekunder
    
    #Gradientmotståndet har en oproportioneligt stor betydelse gentemot
    #de andra krafterna. Viktar man ned grad.-mot. blir kraften som total för liten
    #if F_Gr <= 0:
    #    F_Gr = 0
    v = speed  # m/s
    u = efficiency 
    consumption = (F_D + F_R + F_Gr)*v/u 
    # consumption mäts i 
    return consumption

#list_F_Gr = []
#list_F_D = []
#list_F_R = []

def adj_power(speed, drag, total_weight, rolling_res_per_wheel, alpha, efficiency):
    #Ange speed i m/s
    F_D = aero_resistance(speed, drag)
    F_R = rolling_resistance(total_weight, rolling_res_per_wheel)
    F_Gr = gradient_resistance(alpha, total_weight)
    # Samtliga ovan har enheterna kg*m/s^2
    # där kg är kilogram, m är meter och s är sekunder
    
    #print(F_Gr)
    #list_F_Gr.append(F_Gr)
    #list_F_D.append(F_D)
    #list_F_R.append(F_R)
    #F_D = 0
    #if F_Gr <= 0:
    #    F_Gr = 0
    v = speed # m/s
    u = efficiency 
    consumption = (F_D + F_R + F_Gr)*v/u # W = kg*m^2/s^3
    return consumption

def total_power(speed, solar_car, alpha, acc):
    #Ange speed i m/s
    
    #Hämtar värdena från solbilen
    total_weight = solar_car.weight #kg
    rolling_rest = rolling_resistance(solar_car.weight, solar_car.rolling_res_per_wheel)
    efficiency = solar_car.efficiency_my
    #alpha = angle
    rho = solar_car.rho
    drag = solar_car.drag
    front_area = solar_car.front_area
    
    
    F_D = aero_resistance(speed, drag)
    F_R = rolling_rest #rolling_resistance(total_weight, rolling_res_per_wheel)
    F_Gr = gradient_resistance(alpha, total_weight)
    F_A = total_weight * acc
    # Samtliga ovan har enheterna kg*m/s^2
    # där kg är kilogram, m är meter och s är sekunder
    
    v = speed # m/s
    u = efficiency 
    consumption = (F_D + F_R + F_Gr + F_A)*v/u # W = kg*m^2/s^3
    return consumption

# Vi delar upp komposanterna till den totala förbrukningen

def aero_power(speed, solar_car):
    drag = solar_car.drag
    efficiency = solar_car.efficiency_my
    
    F_D = aero_resistance(speed, drag)
    
    v = speed # m/s
    u = efficiency 
    
    consumption = F_D*v/u # W = kg*m^2/s^3
    return consumption

###

def gradient_power(speed, solar_car, alpha):
    total_weight = solar_car.weight #kg
    efficiency = solar_car.efficiency_my
    
    F_Gr = gradient_resistance(alpha, total_weight)
    
    v = speed # m/s
    u = efficiency 
    
    consumption = F_Gr*v/u # W = kg*m^2/s^3
    if consumption < 0:
        consumption = 0
    return consumption

###

def rolling_power(speed, solar_car):
    efficiency = solar_car.efficiency_my
    
    F_R = rolling_resistance(solar_car.weight, solar_car.rolling_res_per_wheel)
    
    v = speed # m/s
    u = efficiency 
    
    consumption = F_R*v/u # W = kg*m^2/s^3
    if consumption < 0:
        consumption = 0
    return consumption

###

def acc_power(speed, solar_car, acc):
    total_weight = solar_car.weight #kg
    efficiency = solar_car.efficiency_my
    
    F_A = total_weight * acc
    
    v = speed # m/s
    u = efficiency 
    
    consumption = F_A*v/u # W = kg*m^2/s^3
    if consumption < 0:
        consumption = 0
    return consumption

#####

def get_dist_power(speed, start, stop, solar_car): #Här ska man lägga till vilken bil som används
    #Ange speed i m/s
    try:
        height = stop[1] #m
        last_height = start[1] #m
        length = stop[0] - start[0] #km
        angle_dist = distances_and_angles([start, stop])
    except TypeError: # Om vi ska arbeta utan höjdskillnad
        height = last_height = 0
        length = stop - start
        angle_dist = [0]
        
    angle = m.atan((height-last_height)/(length*1000)) # radianer
    
    weight = solar_car.weight #kg
    rolling_rest = rolling_resistance(solar_car.weight, solar_car.rolling_res_per_wheel)
    efficiency = solar_car.efficiency_my
    alpha = angle
    
    rho = solar_car.rho
    drag = solar_car.drag
    front_area = solar_car.front_area
    # Rho mäts i kg/m^3
    # drag_koeff är en skalär
    # fron_area mäts i m^2
    
    #power = adj_power(speed, drag, weight, solar_car.rolling_res_per_wheel, alpha, efficiency)
    powern = power(rho, speed, drag, front_area, weight, solar_car.rolling_res_per_wheel, alpha, efficiency)
    
    #returnerar total förbrukningen i W
    return powern


# Funktionen lägger in förbrukningarna i en samlad lista
def power_list(distance_list, speed_list, solar_car):
    #Ange speed i m/s
    if type(speed_list) != list:
        speed_list = [speed_list]*len(distance_list)
    powers = []
    
    # Tar fram två punkter på streckan och räknar ut förbrukningen på streckan
    for i in range(1, len(distance_list)):
        start = distance_list[i-1]  
        stop = distance_list[i]
        #print(start)
        
        # power anges i W
        power = get_dist_power(speed_list[i], start, stop, solar_car)
        powers.append(power)
        
    # returnerar en lista med förbrukningarna i W
    return powers

# Räknar ut förbrukningen mellan två punkter
def get_consumption(speed, start, stop, solar_car):
    #Ange speed i m/s
    power = get_dist_power(speed, start, stop, solar_car) # Effekt i W
    
    try:
        length = stop[0] - start[0] #i km
    except TypeError: # Om vi ska arbeta utan höjdskillnad
        length = stop - start #i km
    
    time = 1000*length/speed # sekunder,  m/(m/s)
    #Svarar i Ws
    return time*power

# Lägger ihop förbrukningen för en solbil för alla distanser i en lista
def sum_consumption(distance_list, speed_list, solar_car, lista = False):
    #Ange speed i m/s
    if type(speed_list) != list:
        speed_list = [speed_list]*len(distance_list)
    total_consumption = 0
    consumpts = []
    
    #Lägger in förbrukningen längs vägen i en lista
    for i in range(1, len(distance_list)):
        start = distance_list[i-1]
        stop = distance_list[i]
        cons = get_consumption(speed_list[i], start, stop, solar_car)
        consumpts.append(cons)
        total_consumption += cons
    if not lista: # Om det inte ska returnaras en lista, returnera summan
        return total_consumption
    else: # Annars returnera listan
        return consumpts
    

def sectional_consumption(sections, speed_list, solar_car):
    if type(speed_list) != list:
        speed_list = [speed_list]*len(sections)
    cons = []
    for i in range(len(sections)):
        cons.append([sum_consumption(sections[i], speed_list[i], solar_car), sections[i][-1][0]])
    return cons

def even_consumption(all_distances, speed_list, num_secs, solar_car):
    sections = get_even_sections(all_distances, num_secs)
    consum = sectional_consumption(sections, speed_list, solar_car)
    return consum

def plot_powers(speed, distance_list, solar_car):
    powers = power_list(distance_list, speed, solar_car)
    X = np.array(distance_list)
    #print(len(X.transpose()[0]))
    Y = np.array(powers)
    plt.plot(X.transpose()[0][:-1], Y, "ro")
    plt.show()
    
def plot_consumption(speed, sections, solar_car, print_con = False):
    #Ange speed i m/s
    consumptions = []
    acc_cons = []

    cons_total = 0

    velocity = speed

    for item in sections:
        del_consum = sum_consumption(item, velocity, solar_car)
        consumptions.append(del_consum)
        cons_total += del_consum
        acc_cons.append(cons_total)
        
    if print_con:
        print("Total konsumption: "+str(round(cons_total/1000000)) + " "
              +str(round((cons_total%1000000)/1000))+ " "
                    +str(round(cons_total%1000, 1))+" mwh")
            
    b = []
    
    dists = []
    for sec in sections:
        dists.append(sec[-1][0])

    for item in dists:
        if item not in b and not m.isnan(item) and item != 0:
            b.append(item)
            
    A = np.array(consumptions)
    B = np.array(b)
    
    plt.plot(B, A, "b-")

    plt.show()
    
