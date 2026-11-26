# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 20:40:55 2025

@author: Oscar Osbeck
"""

from SOLPLAN import *
#from INDATA import *
from SOLBIL import *
from FORB import *


"""
Den genomsnittliga hastigheten måste vara minst 63 km/h för att komma i tid till alla stop
"""

"""
För att simulera datan som finns från LORA ska man kolla på 
de första 48972.15 meterna 
"""

class trip:
    def __init__(self, distance_list, speed, date, solar_car, start_dist = 0, start_load = 1, stop_dist = None):
        
        # Hitta datum och klockslag
        date = dt.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        clock = date.hour + date.minute/60 + date.second/3600
        #print(clock)
        
        # Definiera lister och variabler
        whole_trip = []
        day = []
        positions = []
        self.distance_list = distance_list
        num_day = 0
        sum_cons = 0
        sum_prod = 0
        section = 0
        total_time = 0
        first = distance_list[0]
        s = 0
        while start_dist > first[0]:
            first = distance_list[s]
            s+=1
        break_bool = False
        
        # Gör variabler baserade på existerande funktioner
        ghi = ghi_list()
        file_names = coord_to_name()
        
        # Kontrollerar om hastigheterna är en lista, justerar
        speed_l = []
        if type(speed) == int or type(speed) == float:
            speed_l = [speed]*len(file_names)
        else:
            speed_l = speed
            
        #print(file_names)
        
        #Hämtar instrålningen för de första 2 stoppen
        ghi1, ghi2, pos1, pos2 = get_ghis(file_names, 0)
        print("positioner "+str(pos1)+" "+str(pos2))
        
        # Sätter startvärden
        adj_time = date
        start_idx = 1
        
        # Justerar hur stor andel av batteriet som är kvar baserat på om batteriet är laddat
        solar_car.battery_left = solar_car.battery_capacity * start_load 
        
        # Kör hela racet
        for i in range(s+1, len(distance_list)):
            #Hämtar hastigheten
            speed = 0
            if section >= len(speed_l):
                speed = speed_l[-1]
            else:
                speed = speed_l[section]
                
            #Tar fram nuvarande position och tid
            curr = distance_list[i]
            position = curr[0]
            #time och total_time är räknade i sekunder
            time = 1000*abs(position - first[0])/speed #i sekunder (m/(m/s))
            total_time += time 
            
            # Kollar om bilen har en maxstrecka samt denna är körd
            if stop_dist != None:
                if position >= stop_dist:
                    break_bool = True
            
            # Cons nedan är i Ws dvs Joule
            cons = get_consumption(speed, first, curr, solar_car)
            
            #prod = production_data(position, time, clock, solar_car, ghi)/3.6
            adj_date = date - dt.timedelta(hours = 9, minutes = 30) #Justering för tidszon ACST mot UTC
            #print(adj_date)
            
            # Sätter index
            end_idx = start_idx
            #print(date)
            #prod nedan anges i Ws dvs Joule
            
            # Räknar ut produktionen och aktuellt index för soldata
            prod, end_idx = production_data_est(position, time, solar_car, adj_date, 
                                                  file_names, ghi1, ghi2, pos1, pos2, start_idx) 
            #prod = production_data(curr[0], time, clock, solar_car, ghi)
            # Justerar index
            start_idx = end_idx
            
            # Kollar om positionen är mellan aktuella stopp
            if position >= pos2 and position < float(file_names[-1][1]):
                ghi1, ghi2, pos1, pos2 = get_ghis(file_names, position)
                start_idx = 1
                section += 1
                print("positioner "+str(pos1)+" "+str(pos2))
                
            # Räknar ut konsumption, produktion och netto per timme
            cons_per_h = cons / time #(J / s = W)
            prod_per_h = prod / time #(J / s = W)
            sum_cons += cons #(J)
            sum_prod += prod #(J)
            net = prod - cons # Netto i Joule dvs Ws
            
            # Fixar batteriet
            solar_car.battery_left += net/3.6 # mWh += Ws/3.6
            if solar_car.battery_left >= solar_car.battery_capacity:
                solar_car.battery_left = solar_car.battery_capacity
            elif solar_car.battery_left <= 0:
                solar_car.battery_left = 0
                break_bool = True
            
            # Kollar och justerar klockan
            if clock >= 17:
                for i in range(20):
                    min5 = 5/60/24
                    prod = production_data(curr[0], min5, clock + i*min5, solar_car, ghi)
                    sum_prod+=prod
                for i in range(24):
                    min5 = 5/60/24
                    prod = production_data(curr[0], min5, 6 + i*min5, solar_car, ghi)
                    sum_prod+=prod
                    
                #gör en lista med intressanta värden
                t_list = [curr, clock, cons, prod, sum_cons, sum_prod, sum_prod-sum_cons, solar_car.battery_left, cons_per_h, prod_per_h]
                #if type(t_list[-1]) != float:
                    #print(t_list[-1])
                #print(t_list[-1])
                
                # Lägger in värden i en positionslista
                positions.append([curr[0], clock, cons, prod, sum_cons, sum_prod, sum_prod-sum_cons, solar_car.battery_left, cons_per_h, prod_per_h])
                
                # Lägger in värden i lista för dagsbaserade värden
                day.append(t_list)
                whole_trip.append([num_day, day])
                
                # Återställer värden
                first = curr
                day = []
                clock = 8
                date += dt.timedelta(days = 1)
                date = date.replace(hour=clock, minute=0, second=0, microsecond=0)
                num_day += 1
                #print("Dag: " +str(num_day))
            else:
                #gör en lista med intressanta värden
                t_list = [curr, clock, cons, prod, sum_cons, sum_prod, sum_prod-sum_cons, solar_car.battery_left, cons_per_h, prod_per_h]
                #if type(t_list[-1]) != float:
                    #print(t_list[-1])
                #print(t_list[-1])
                
                # Lägger in värden i en positionslista
                positions.append([curr[0], clock, cons, prod, sum_cons, sum_prod, sum_prod-sum_cons, solar_car.battery_left, cons_per_h, prod_per_h])
                day.append(t_list)
                first = curr
                date += dt.timedelta(seconds = time)
                clock += time/3600 #klocka i timmar, omvandlar från sekunder
            #print(time)
            if break_bool:
                print("Total stecka: "+str(round(curr[0],2)) +"km")
                break;
        num_day += 1
        whole_trip.append([num_day, day])
        descs = ["Position", "Klockslag", "Aktuell förbrukning", "Aktuell produktion",
                                  "Summa konsumption", "Summa produktion", "Summa netto", "Återstående Batteri", "Aktuell förbrukning W", "Aktuell produktion W"]
        for d in range(len(descs)):
            descs[d] = str(d) + ": "+descs[d]
        
        # Sätter lokala värden
        self.days_descriptions = descs
        self.days = whole_trip
        self.stops = []
        for stop in file_names:
            self.stops.append([stop[0], stop[1]])
            
        # Förbereder värden för varje timme
        hours = []
        hour = 0
        h_cons = 0
        h_prod = 0
        day = 0
        
        # Går igenom alla positioner och sätter värdena timme för timme
        for pos in positions:
            if int(pos[1]) == hour:
                h_cons += pos[2]/1000
                h_prod += pos[3]/1000
            elif h_cons > 0:
                hours.append([day, hour, h_cons, h_prod])
                if hour == 16:
                    day += 1
                hour = int(pos[1])
                h_cons = 0
                h_prod = 0
            else:
                hour = int(pos[1])
                h_cons = 0
                h_prod = 0
                
        # Sätter värdena på self variablerna
        self.hours = hours
        self.hour_descriptions = ["Dag", "Klocktimme", "Konsumtion/h", "Produktion/h"]
        self.poss_descriptions = descs
        self.positions = positions
        self.solar_car = solar_car
        self.breakdown = break_bool
        self.total_consumption = sum_cons
        self.total_production = sum_prod
        self.total_seconds = total_time
        self.pass_control = False
        if total_time < 174168 and not self.breakdown: #antalet sekunder som man måste komma under
            self.pass_control = True
        hours = int(total_time/3600)
        minutes = int(total_time/60)-hours*60
        seconds = int(total_time - minutes*60 - hours*3600)
        self.total_time = str(hours)+"h "+str(minutes)+"min "+str(seconds)+"sek"
        
    # Plottar värden med avseende på tiden
    # Vad du vill plotta väljer du genom att sätta värdet på plot_val
    """
    0 till 3: ["Position", "Klockslag", "Aktuell förbrukning", "Aktuell produktion",
    4 till 6:  "Summa konsumption", "Summa produktion", "Summa netto",
    7 till 9:  "Återstående Batteri", "Aktuell förbrukning W", "Aktuell produktion W"]
    """
    def plot_time(self, resolution = "day", plot_val = 2, points = 1000000000, start = 0):
        Y = []
        X = []
        d_n = 0
        n_points = 0
        finish_time = 0
        for d in self.days:
            if resolution == "day":
                for item in d[1][start:]:
                    if n_points < points:
                        X.append(item[1]+d_n*24)
                        Y.append(item[plot_val])
                        n_points += 1
                if n_points < points:
                    X.append(d[1][-1][1]+d_n*24)
                    Y.append(d[1][-1][plot_val])
                    n_points += 1
            else:
                for item in d[1][start:]:
                    if n_points < points:
                        X.append(item[1]+d_n*9-8)
                        finish_time = item[1]+d_n*9-8
                        Y.append(item[plot_val])
                        n_points += 1
            d_n += 1
        x = np.array(X)
        y = np.array(Y)
        name = self.solar_car.name
        if resolution != "day" and not self.breakdown:
            print("Målgången för "+name+" skedde efter "+str(round(finish_time,2))+" timmar")
        elif resolution != "day":
            print("Breakdown för "+name+" skedde efter "+str(round(finish_time,2))+" timmar")
        plt.plot(x, y, "r-")
        plt.title(self.days_descriptions[plot_val] + " mot Tid för "+name)
        if resolution == "day" or resolution == "days":
            plt.xlabel("Clocktimmar från start")
        else:
            plt.xlabel("Timmar från start")
            
        plt.ylabel(self.days_descriptions[plot_val])
        plt.grid()
        plt.show()
        
    # Plottar med avseende på position från start i km
    # Vad du vill plotta väljer du genom att sätta värdet på plot_val
    """
    0 till 3: ["Position", "Klockslag", "Aktuell förbrukning", "Aktuell produktion",
    4 till 6:  "Summa konsumption", "Summa produktion", "Summa netto",
    7 till 9:  "Återstående Batteri", "Aktuell förbrukning W", "Aktuell produktion W"]
    """
    def plot_positions(self, plot_val = 1, ret = False):
        Y = []
        X = []
        d_n = 0
        for p in self.positions:
            X.append(p[0])
            Y.append(p[plot_val])
        x = np.array(X)
        y = np.array(Y)
        plt.title(self.days_descriptions[plot_val] + " mot Distans för "+self.solar_car.name)
        plt.xlabel("Kilometer från start")
        plt.ylabel(self.poss_descriptions[plot_val])
        plt.plot(x, y, "r-")
        plt.grid()
        if ret:
            plt.savefig("image"+str(plot_val)+".png")
            plt.close()
        else:
            plt.show()
        
    # Plottar värdena för varje timme, kan bara välja produktion och konsumption
    def plot_hours(self,  cons = True, prod = True):
        X = []
        Y = []
        Z = []
        for h in self.hours:
            X.append(h[0]*9 + h[1]-8)
            Y.append(h[2]/3.6)
            Z.append(h[3]/3.6)
        x = np.array(X)
        y = np.array(Y)
        z = np.array(Z)
        leg = []
        if cons:
            plt.plot(x, y, "b-")
            leg.append("Förbrukning per timme")
        if prod:
            plt.plot(x, z, "r-")
            leg.append("Produktion per timme")
        plt.xlabel("Timmar från start")
        plt.ylabel("Wh")
        plt.legend(leg)
        plt.show()
        
    # plottar bara altitudkurvan
    def plot_altitude(self, ret = True):
        X = []
        Y = []
        for h in self.distance_list:
            X.append(h[0])
            Y.append(h[1])
        x = np.array(X)
        y = np.array(Y)
        plt.plot(x, y, "b-")
        plt.title("Höjd över havet")
        plt.xlabel("Distans i km")
        plt.ylabel("Höjd över havet i meter")
        if ret:
            plt.savefig("altimage.png")
            plt.close()
        else:
            plt.show()
        



#add_session("RESA")







