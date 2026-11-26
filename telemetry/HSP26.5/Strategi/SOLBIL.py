# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 20:40:00 2025

@author: oscar
"""

"""
specs för sven

front_area = 0.867 #m^2
H5 front_area = 0.827 m^2
H6 front_area = 0.706 m^2
rho = 1.2 #luftdensitet kg/m^3
drag = 0.0551 #estimat, denna ska vara 0.2
drag = 0.0157 eller 0.02 ej bekräftad
total_weight = 349.5 #kg inklusive förare
rolling_res_per_wheel = 0.003
efficiency_my = 0.9

Battery_capacity = 3055 #Wh
"""

#from .FORB import *

#from sessions import *

#16 = 1/2 * rho * drag_koeff * front_area * (60/3.6)**2

drag_koeff = 23.2/(1/2 * 1.2 * 0.867 * (60/3.6)**2)

class solar_car:
    def __init__(self, name, weight, front_area, rho, drag, rolling_res_per_wheel,
                 num_wheels, efficiency_my, battery_capacity, eff_factor, solar_area):
        self.name = name
        self.weight = weight
        self.front_area = front_area
        self.rho = rho
        self.drag = drag
        self.rolling_res_per_wheel = rolling_res_per_wheel
        self.num_wheels = num_wheels
        self.efficiency_my = efficiency_my
        self.battery_capacity = battery_capacity*1000 #omvandlar från wh till mwh
        self.battery_left = battery_capacity*1000
        self.eff_factor = eff_factor
        self.solar_area = solar_area
        
        
henry = solar_car("Henry", 349.5, 0.867, 1.2, 0.2, 0.003, 3, 0.9, 3055, 0.23, 6)

#Nuna13 includerar de värden som laget påstår och i övrigt värden från sven samt vissa gissningar
nuna13 = solar_car("Nuna 13", 240, 0.87, 1.2, 0.2, 0.003, 3, 0.97, 3055, 0.27, 6)





#add_session("SOLBIL")
