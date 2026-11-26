# -*- coding: utf-8 -*-
"""
Created on Thu May 21 12:39:42 2026

@author: oscar
"""

from ReceiverPack import *

import datetime as dt
import matplotlib.dates as mdates

fig_size = (8,5)

def read_lora_data(number):
    data = []
    with open("dataLora"+str(number)+".txt", "r") as file:  
        #print(now)
        lines = file.readlines()
        for item in lines:
            if len(string_to_vec(item)) >= 15:
                data.append(string_to_vec(item))
    return data

def read_data_file(file_name):
    data = []
    with open(file_name, "r") as file:  
        #print(now)
        lines = file.readlines()
        for item in lines:
            if len(string_to_vec(item)) >= 1:
                data.append(string_to_vec(item))
    return data

def read_mapp_data(mapp_namn = "DatafilerFalkenberg0519kör1"):
    lines = get_lines(mapp_namn)
    mapp_data = []
    for l in lines:
        data = read_data_file(mapp_namn+"/"+l)
        for d in data:
            mapp_data.append(d)
    return mapp_data

# Sätter ihop all data i .txt-filer som innehåller namnet "Lora"
def concatenate_lora_data():
    datafiles = get_lines_string("Lora")
    #print(datafiles)
    datafiles.remove("allLoraData.txt")
    ex_data = read_mapp_data()
    all_data = []
    for file in datafiles:
        all_data += read_data_file(file)
    all_data += ex_data
    #all_data = sorted(all_data, key = lambda x: x[1]) 
    return all_data

# Sätter ihop all data i .txt-filer som innehåller namnet "Lora"
def concatenate_SD_data(mapp = "txt_filer"):
    #datafiles = get_lines_string("log_")
    ex_data = read_mapp_data(mapp)
    all_data = []
    """
    for file in datafiles:
        all_data += read_data_file(file)
    """
    all_data += ex_data
    all_data = sorted(all_data, key = lambda x: x[1]) 
    return all_data
    
# Tar all data i en list och gör en txt fil med datan
def write_data_to_file(data, new_file_name = "newdata", full = False, append = False):
    wra = "w"
    if append:
        wra = "a"
    else:
        wra = "w"
    with open(new_file_name + ".txt", wra) as file:  
        for d in data:
            if not full:
                file.writelines(str(d).replace("'","")[1:-1]+"\n")
            else:
                file.writelines(str(d).replace("'","")+"\n")

# plottar data från en fil "dataLoraX" 
def plot_lora_data(number, numbers = [0,1], bort_minus = True):
    # Numbers avser nummrena från MATLAB scriptet
    data = read_lora_data(number)
    plot_data = []
    #print(plot_data[0])
    dates = []
    for item in data:
        #print(item)
        data_w_time = item[0] +" "+item[1]
        #print(data_w_time)
        date = dt.datetime.strptime(data_w_time[:-7], "%Y-%m-%d %H:%M:%S")
        #print(date)
        dates.append(date)
    plot_data.append(dates)
    for n in numbers:
        vec = []
        last = 0
        for item in data:
            try:
                last = float(item[n+4])
                if last < 0 and bort_minus:
                    last = 0
                vec.append(last) #+4 för att positionera
            except (ValueError, IndexError):
                vec.append(last)
        plot_data.append(vec)
        
    plt.figure(figsize = fig_size)
    for i in range(len(numbers)):
        # Vi skriver bara ut tiden eftersom att datumet(oftast) inte är relevant
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
        plt.plot(plot_data[0], plot_data[i+1], "b")
    plt.show()

# plottar datan från en txtfil, eller angiven data
# Genom att ange flera värden i "numbers" kan man plotta och gämföra flera värden från samma fil
def plot_txt_data(txtfile, numbers = [0,1], step = 4, minus_bort = True, 
                  datum = True, mapp = False, interval = False, start = True, end = True, 
                  distans = False, savename = False, data = False):
    # Numbers avser nummrena från MATLAB scriptet
    if type(data) == bool:
        data = read_data_file(txtfile)
    data = sorted(data, key = lambda x: x[1])
    data_titlar = ManuellSD
    if type(start) == str:
        start = dt.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    elif type(start != int) and datum:
        start = dt.datetime.strptime("2020-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    if type(end) == str:
        end = dt.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    elif type(end) != int and datum:
        end = dt.datetime.strptime("2050-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    """
    SD_data_titlar
    MATLAB_titlar
    Lora_data_titlar
    """
    if "SD" in txtfile:
        data_titlar = ManuellSD
        step = 0
        data = get_motor_and_battery(data, Lora = False, step = step)
    else:
        data_titlar = ManuellLora
        step = 4
        data = get_motor_and_battery(data, Lora = True, step = step)
    plot_data = []
    legends = []
    #print(plot_data[0])
    dates = []
    
    ### Testa om det går att ta bort denna for-loopen
    i = 0
    for item in data:
        if datum:
            try:
                # Hämtar datum och tid som string
                data_w_time = str(item[0]).replace(",","")+" "+str(item[1]).replace(",","")
                
                # Omvandlat till datetime
                date = dt.datetime.strptime(data_w_time[:-7], "%Y-%m-%d %H:%M:%S")
                if start < date < end:
                    dates.append(date)
            except ValueError:
                #dates.append(i)
                i+=1
            except TypeError:
                print(item)
        else:
            dates.append(i)
            i+=1
    plot_data.append(dates)
    ### !!Fram till hit!!
    #print(dates)
    if distans:
        numbers.append(1)
        
    for n in numbers:
        vec = []
        last = 0
        summa = 0 # För att kontrollera extremvärden
        antal = 0
        for item in data:
            try:
                process = False
                if datum:
                    # Hämtar datum och tid som string
                    data_w_time = str(item[0]).replace(",","")+" "+str(item[1]).replace(",","")
                    
                    # Omvandlat till datetime
                    date = dt.datetime.strptime(data_w_time[:-7], "%Y-%m-%d %H:%M:%S")
                    if start < date < end:
                        process = True
                else:
                    process = True
                if process:
                    #print(float(item[n+4].replace(",","")))
                    curr = float(item[n+step].replace(",","")) #+step(4) för att positionera
                    
                    # Justerar från m/s till km/h
                    if n == 0:
                        curr = float(curr)*3.6
                    
                    summa += last
                    antal += 1
                    if curr < 0 and minus_bort:
                        curr = 0
                    if type(interval) == list:
                        if curr < interval[0] or curr > interval[1]:
                            curr = last
                    avg = summa/antal
                    
                    
                    last = curr
                    vec.append(last) 
            except (ValueError, IndexError):
                if datum:
                    # Hämtar datum och tid som string
                    data_w_time = str(item[0]).replace(",","")+" "+str(item[1]).replace(",","")
                    
                    # Omvandlat till datetime
                    date = dt.datetime.strptime(data_w_time[:-7], "%Y-%m-%d %H:%M:%S")
                    if start < date < end:
                        vec.append(last)
                else:
                    vec.append(last)
                #print("Error")
        plot_data.append(vec)
        legends.append(data_titlar[n])
        
    colors = ["b", "g", "r", "k"]
    
    short = 0
    if distans:
        short = 1
        last = 0
        i = 1
        while i < len(plot_data[-1]):
            if abs(plot_data[-1][i] - last) > 500: # Sollar bort vissa orimliga värden
                new_data = []
                #print(str(plot_data[-1][i]) +" : "+ str(last))
                for item in plot_data:
                    new_data.append(item[:i] + item[i+1:])
                plot_data = new_data
            else:
                last = plot_data[-1][i]
                i+=1
            #print(last)
    
    plt.figure(figsize = fig_size)
    for i in range(len(numbers)-short):
        # Vi skriver bara ut tiden eftersom att datumet(oftast) inte är relevant
        if datum and not distans:
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
        c = colors[i]
        if distans:
            plt.plot(plot_data[-1], plot_data[i+1], c)
        else:
            plt.plot(plot_data[0], plot_data[i+1], c)
        plt.title("Data från "+txtfile)
        if datum and not distans:
            plt.xlabel("Klockslag")
        elif distans:
            plt.xlabel("Distans(m)")
        else:
            plt.xlabel("Radnummer")
        
        val = EnheterLora[numbers[i]]
        plt.ylabel(val)
    plt.legend(legends)
    
    if type(savename) == str:
        plt.savefig(savename)
        return dates
    else:
        plt.show()
    
def read_drivers():
    data = read_data_file("forardata.txt")
    for item in data:
        item[3] = item[3].replace("\n","")
        item[0] = item[0].replace(",","")
        item[1] = item[1].replace(",","")
        item[2]+=" "+item[3]
        item.remove(item[3])
    return data

def plot_lora_driver(driver, index = [0], distans = False, savename = False, data = False):
    drivers = sorted(read_drivers(), key = lambda x: x[0] + x[1])
    end = ""
    end_exist = False
    for d in drivers:
        """
        if type(driver) == list and not end_exist:
            end = d[0] +" "+d[1][:-7]
            end_exist = True
        print(d)
        """
        if type(driver) == str:
            if driver in d[-1]:
                driver = d
    start = driver[0] +" "+driver[1][:-7]
    
    # Räknar ut sista tidsvärdet
    if type(data) == bool:
        data = read_data_file("allLoraData.txt")
    data = sorted(data, key = lambda x: x[1])
    dates = []
    for item in data:
        # Hämtar datum och tid som string
        data_w_time = str(item[0]).replace(",","")+" "+str(item[1]).replace(",","")
        
        # Omvandlat till datetime
        date = dt.datetime.strptime(data_w_time[:-7], "%Y-%m-%d %H:%M:%S")
        if dt.datetime.strptime(start, "%Y-%m-%d %H:%M:%S") < date:
            if len(dates) >= 1:
                if date < dates[-1] + dt.timedelta(seconds = 50):
                    dates.append(date)
            else:
                dates.append(date)
    end = str(dates[-1])
    print(start)
    print(end)
    if type(savename) == str:
        dates = plot_txt_data("allLoraData.txt", index, datum = True, start= start, end = end,
                             distans = distans, savename = savename, data=data)
        return savename+".PNG", dates
    else:
        plot_txt_data("allLoraData.txt", index, datum = True, start= start, end = end, distans = distans)



drivers = ["2026-05-19, 09:27:07.546487, Oscar Pålsson",
           "2026-05-19, 11:52:11.048411, Sponsorer mm",
           "2026-05-19, 12:50:15.396355, Jennie Fagerberg",
           "2026-05-19, 14:23:15.378599, Toni Jausevac",
           "2026-05-19, 15:11:24.144324, Albin Gill"]



"""
all_data = concatenate_lora_data()

write_data_to_file(all_data, "allLoraData")

plot_txt_data("allLoraData.txt", [0], datum = True)


sd_data = concatenate_SD_data()

write_data_to_file(sd_data, "allSDData")

plot_txt_data("allSDData.txt", [0], step = 0, datum = False)
"""




