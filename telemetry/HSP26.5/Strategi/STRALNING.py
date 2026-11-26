# -*- coding: utf-8 -*-
"""
Created on Mon May 11 19:53:23 2026

@author: oscar
"""

from SOLPLAN import *
from SOLBIL import *

standard_date = "2025-08-09T12:00:00"



def get_radiation(date, position): # date ska vara datum och tid
    file_names = coord_to_name()

    ghi1, ghi2, pos1, pos2 = get_ghis(file_names, position)

    if type(date) != datetime.datetime:
        date = dt.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    adj_date = date - dt.timedelta(hours = 9, minutes = 30) #Justering för tidszon ACST mot UTC

    rad, idx = radiation_data_est(adj_date, position, file_names, ghi1, ghi2, pos1, pos2, start_idx = 1, ghi_num = 5)

    return rad

def get_radiations(dates, position):
    file_names = coord_to_name()

    ghi1, ghi2, pos1, pos2 = get_ghis(file_names, position)
    
    rads = []
    for date in dates:
        date = dt.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        adj_date = date - dt.timedelta(hours = 9, minutes = 30) #Justering för tidszon ACST mot UTC

        rad, idx = radiation_data_est(adj_date, position, file_names, ghi1, ghi2, pos1, pos2, start_idx = 1, ghi_num = 5)
        rads.append(rad)
    return rads

def plot_radiation_positions(n = 10, date = standard_date):
    x = []
    y = []
    for i in range(n):
        p = i*3020/n
        x.append(p)
        y.append(get_radiation(date, p))

    plt.plot(x, y)
    plt.title("")
    plt.show()
    
def plot_radiations_at_position(n = 10, dates = [standard_date]):
    x = []
    rads = []
    for i in range(n):
        p = i*3020/n
        x.append(p)
        rads.append(get_radiations(dates, p))

    cs = ["b", "r", "g", "k"]
    for d in range(len(dates)):
        y = []
        for r in rads:
            y.append(r[d])
        plt.plot(x,y,cs[d])
    plt.title("Strålning vid olika positioner")
    plt.legend(dates)
    plt.show()


# Estimerar strålning vid position givet viss hastighet
def plot_radiation_velocity(n = 20, date = standard_date, velocity = 60):
    x = []
    y = []
    for i in range(n):
        p = i*3020/n
        t = p / velocity # timmar
        deltat = 3020/n/velocity # tid mellan mätningar
        if type(date) != datetime.datetime:
            date = dt.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        date += dt.timedelta(hours = deltat)
        #print("tid: "+str(date.hour))
        #print("dag: "+str(date.day))
        if date.hour >= 17:
            date += dt.timedelta(days = 1)
            h = 8 + (int(deltat) + date.hour - 17)
            #print(h)
            date = date.replace(hour = h)
        x.append(p)
        y.append(get_radiation(date, p))

    plt.plot(x, y)
    plt.show()


add_session("Radiation")
















