# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 17:21:07 2026

@author: Oscar Osbeck
"""


from RESA import *

"""
För att simulera datan som finns från LORA ska man kolla på 
de första 48972.15 meterna 
"""

sven = solar_car("Sven", 349.5, 0.867, 1.2, 0.2, 0.003, 3, 0.9, 3055, 0.23, 6)

#Nuna13 includerar de värden som laget påstår och i övrigt värden från sven samt vissa gissningar
nuna13 = solar_car("Nuna 13", 240, 0.87, 1.2, 0.17, 0.003, 3, 0.97, 3055, 0.27, 6)

sven_jr = solar_car("Sven jr", 269.5, 0.867, 1.2, 0.2, 0.003, 3, 0.9, 3055, 0.23*0.92, 6)

sven_jr2 = solar_car("Sven jr2", 249.5, 0.867, 1.2, 0.2*0.94, 0.003, 3, 0.95, 3055, 0.23, 6)


all_distances = cs_distances(allt_i_ett=True)

res_dist = sum_distance(all_distances)

vel = 63 /3.6 # 63km/h omvandlat till m/s

q_vel = 63 /3.6

vel2 = 61 /3.6

velocity = [q_vel]*2+ [vel]*5

standard_date = "2025-08-09T08:00:00"

sven_jr_trip = trip(res_dist, velocity, standard_date, sven_jr)
#sven_trip = trip(res_dist, vel, standard_date, sven)

#sven_jr_trip.plot_positions(7)



sven_jr_trip.plot_positions(7)
sven_jr_trip.plot_positions(1)
#sven_jr_trip.plot_positions(2)
sven_jr_trip.plot_positions(3)
sven_jr_trip.plot_positions(4)
sven_jr_trip.plot_positions(5)


sven_jr_trip.plot_time()
sven_jr_trip.plot_time("d", 8, 100)
sven_jr_trip.plot_time("da", 9)
sven_jr_trip.plot_time("da", 4)


# ============================
# MAIN – AUTOMATISKA PLOTTAR
# ============================

print("OPT.py körs – genererar plottar")

# --- 1. Batteri mot distans ---
sven_jr_trip.plot_positions(7)

# --- 2. Nettoenergi mot distans ---
sven_jr_trip.plot_positions(6)

#sven_jr_trip.plot_positions(1)

# --- 3. Batteri mot tid (dag-upplöst) ---
#sven_jr_trip.plot_time("day", 7)

# --- 4. Total förbrukning och produktion mot tid ---
#sven_jr_trip.plot_time("day", 4)   # Förbrukning
#sven_jr_trip.plot_time("day", 5)   # Produktion

# --- 5. Förbrukning och produktion per timme ---
sven_jr_trip.plot_hours()

# --- 6. Effektbehov längs banan ---
#plot_powers(vel, res_dist, sven_jr)

# --- 7. Solproduktion längs banan (jämna sektioner) ---
#plot_even_production(res_dist, vel, 50, sven_jr)

# --- 8. Produktion vs förbrukning vs netto ---
#plot_even_net(res_dist, 50, vel, sven_jr)



print("Alla plottar genererade")

# -------- Totalsummor --------
cons_mWh = sven_jr_trip.total_consumption/3.6
prod_mWh = sven_jr_trip.total_production/3.6
net_mWh  = (prod_mWh - cons_mWh)/3.6

print("\n===== ENERGISAMMANFATTNING =====")
print(f"Bil: {sven_jr_trip.solar_car.name}")
print(f"Total förbrukning kWh:      {cons_mWh/1e6:.2f}   ({cons_mWh:,.0f} )")
print(f"Total insamlad energi kWh:  {prod_mWh/1e6:.2f}   ({prod_mWh:,.0f} )")
print(f"Netto (prod-cons) kWh:      {net_mWh/1e6:.2f}   ({net_mWh:,.0f} )")
#print(f"Total förbrukning: {cons_mWh/3.6e6:.3f} kWh")

if sven_jr_trip.breakdown:
    print("Status: BREAKDOWN (batteriet tog slut innan mål)")
else:
    print("Status: KLARADE HELA STRÄCKAN")
print("================================\n")
print("Total tid: "+sven_jr_trip.total_time)

if sven_jr_trip.pass_control and not sven_jr_trip.breakdown:
    print("Målgång skedde i tid\n")
elif not sven_jr_trip.breakdown:
    print("Målgång skedde inte i tid\n")
else:
    print("Breakdown")


v = 63/3.6
rho = sven_jr.rho
Cd  = sven_jr.drag
A   = sven_jr.front_area

F_aero = 0.5*rho*Cd*A*v**2
P_aero = F_aero*v

print("F_aero (N):", F_aero)
print("P_aero (W):", P_aero)


"""
Följande är optimeringsfunktioner
De tar mycket tid att köra, detta bör optimeras i framtiden
"""

def vel_opt(solar_car, resolution = 0.5, start = 100):
    vel = start #Vel är km/h
    while trip(res_dist, vel/3.6, standard_date, solar_car).breakdown:# omvandlar från km/h till m/s
        vel-= resolution
    return vel

def weight_opt(solar_car, velocity, resolution = 1): #Velocity anges i km/h
    while trip(res_dist, velocity/3.6, standard_date, solar_car).breakdown:# omvandlar från km/h till m/s
        solar_car.weight -= resolution
    return solar_car.weight

def weight_diff(sol_car, velocity = 20, difference = 10):
    trip1 = trip(res_dist, velocity, standard_date, sol_car)
    solar_heavy = solar_car("heavy", sol_car.weight + difference, sol_car.front_area, sol_car.rho, sol_car.drag,
                            sol_car.rolling_res_per_wheel, sol_car.num_wheels, sol_car.efficiency_my, sol_car.battery_capacity, 
                            sol_car.eff_factor, sol_car.solar_area)
    solar_light = solar_car("light", sol_car.weight - difference, sol_car.front_area, sol_car.rho, sol_car.drag,
                            sol_car.rolling_res_per_wheel, sol_car.num_wheels, sol_car.efficiency_my, sol_car.battery_capacity, 
                            sol_car.eff_factor, sol_car.solar_area)
    heavy_trip = trip(res_dist, velocity, standard_date, solar_heavy)
    light_trip = trip(res_dist, velocity, standard_date, solar_light)
    cons = trip1.total_consumption
    l_cons = light_trip.total_consumption
    h_cons = heavy_trip.total_consumption
    print("Vanlig resa drar "+str(round(cons/1000000, 2)) + "kWh")
    print("Med "+str(difference)+" kg mindre sparar man "+str(round((cons-l_cons)/1000000, 3)) +"kWh")
    print("Med "+str(difference)+" kg mer drar man "+str(round((h_cons-cons)/1000000, 3)) +"kWh mer")
    print("Vikt "+str(sol_car.weight))
    print("Tung vikt "+str(solar_heavy.weight))




"""
vel = 86.6 / 3.6
#vel = 72 / 3.6

nuna_trip = trip(res_dist, vel, 8, nuna13)

nuna_trip.plot_time("day", 7)

nuna_trip.plot_time("da", 7)

nuna_trip.plot_positions(7)


vel = 63.5/3.6

henry_trip = trip(res_dist, vel, 8, henry)

henry_trip.plot_time("da", 7)

print(henry_trip.days_descriptions)

#henry_trip.plot_time("da", 8)
#henry_trip.plot_time("da", 9)
"""




