# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 09:41:33 2025

@author: oscar
"""

import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

date = datetime.datetime.today()

def add_session(title):
    date = datetime.datetime.today()
    year = str(date.year)
    month = str(date.month)
    day = str(date.day)
    hour = str(date.hour)
    minute = str(date.minute)
    second = str(date.second)
    session = [str(date.strftime("%Y-%m-%d")), hour +":"+ minute +":"+ second, title]#year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second]
    with open('Sessions.csv', 'a', newline = '') as file:
        spamwriter = csv.writer(file, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(session)
        
def time_to_float(time_delta):
    hours = float(time_delta.seconds/3600)
    return hours
    
class session_stats:
    def __init__(self):
        all_sessions = []
        with open('Sessions.csv', 'r', newline = '') as file:
            spamreader = csv.reader(file, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            last = 0
            sess_len = datetime.timedelta(seconds = 0)
            sessions = []
            all_items = []
            for item in spamreader:
                all_items.append(item)
                try:
                    idate = datetime.datetime.strptime(item[0]+"/"+item[1]+":"+item[2]+":"+item[3], "%Y-%m-%d/%H:%M:%S")
                except (ValueError, IndexError):
                    try:
                        idate = datetime.datetime.strptime(item[0]+"/"+item[1], "%Y-%m-%d/%H:%M:%S")
                    except ValueError:
                        pass
                if last == 0:
                    last = idate
                else:
                    diff = idate-last
                    if diff < datetime.timedelta(minutes = 15) and idate.date() == last.date():
                        sess_len += diff
                    else:
                        sessions.append([last.date(), sess_len])
                        sess_len = datetime.timedelta(seconds = 0)
                    last = idate
                
            sessions.append([last.date(), sess_len])
              
            
            self.all_sessions = sessions
            self.all_items = all_items
            
        days = []
        #tot_day = datetime.timedelta(seconds = 0)
        day = []
        for s in sessions:
            if day == []:
                day = s
            else:
                if s[0] == day[0]:
                    day[1] += s[1]
                else:
                    days.append(day)
                    day = s
            if s == sessions[-1]:
                days.append(day)
        
        self.days = days
        
    def plot_days(self, acc = False, value = False, price_per_hour = 500):
        x = []
        y = []
        summa = 0
        for d in self.days:
            x.append(d[0])
            if acc:
                summa += time_to_float(d[1])
                if value:
                    y.append(summa*price_per_hour)
                else:
                    y.append(summa)
            else:
                if value:
                    y.append(time_to_float(d[1])*price_per_hour)
                else:
                    y.append(time_to_float(d[1]))
        if acc:
            plt.plot(x, np.array(y), color = "r")
        else:
            plt.bar(x, np.array(y), color = "r")
        plt.gcf().autofmt_xdate()
        plt.xlabel("Datum")
        if value and acc:
            plt.ylabel("Est värde i kr")
            plt.suptitle("Beräknat värde på programmet", fontsize = 13)
            plt.title("Värde per timme: "+str(price_per_hour)+"kr", fontsize = 10)
        elif value:
            plt.ylabel("Est värde i kr")
            plt.suptitle("Beräknad värdeökning på programmet", fontsize = 13)
            plt.title("Värde per timme: "+str(price_per_hour)+"kr", fontsize = 10)
        else:
            plt.ylabel("Timmar")
            plt.title("Tid på programmet")
        plt.show()
        





ss = session_stats()



