# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 20:25:53 2025

@author: Oscar Osbeck
"""

"""
!!! Rutten har blivit fel kring Glandambo, detta bör åtgärdas snarast !!!
"""

import math as m
try:
    from INDATA import *
except ModuleNotFoundError:
    from .INDATA import *

"""
Koordinat, distans och vinkelbaserade funktioner
"""
earth_radius = 6371 #km
pi = 3.1415926

def convert_coordinates_to_distance(coordinates):
    earth_circumference = earth_radius * 2*pi
    distance = []
    latest_point = [0,0,0]
    for point in coordinates:
        if latest_point == [0,0,0]:
            latest_point = point
        else:
            dis_lat = point[0] - latest_point[0]
            dis_lon = point[1] - latest_point[1]
            dis_x = dis_lat/360 * earth_circumference
            dis_y = dis_lon/360 * earth_circumference
            m_dist = m.sqrt(dis_x**2 + dis_y**2)
            #if m_dist < 0.1:
            #    print(point)
            distance.append([m_dist, point[2]])
            latest_point = point
    return distance

def sum_distance(distance, ret_int = False):
    sum_dist = 0
    all_dist = []
    for item in distance:
        sum_dist += item[0]
        all_dist.append([sum_dist, item[1]])
    if ret_int:
        return sum_dist
    return all_dist

def smooth_sum_distance(sum_dist, length = 5):
    all_dist = []
    for i in range(length, len(sum_dist)):
        avg = 0
        for t in sum_dist[i-length:i]:
            avg += t[1]
        all_dist.append([sum_dist[i][0], avg/length])
    return all_dist

def distances_and_angles(distance, degrees = False, print_l = False):
    """
    returnerar distansen i km och vinkel i antingen radianer som standard
    degrees = true => vinkeln ges i grader
    """
    sum_dist = 0
    last_height = 0
    all_dist = []
    for item in distance:
        sum_dist += item[0]
        height = item[1]
        if print_l:
            print("Höjdskillnad: " + str(height-last_height)+"m")
            print("Distans: " +str(item[0]*1000)+"m")
        angle = m.atan((height-last_height)/(item[0]*1000))
        if degrees:
            angle = angle/(2*pi)*360
        all_dist.append([sum_dist, angle])
        last_height = height
    return all_dist

"""
Tidsbaserade funktioner
"""

def date_time_converter(date_string):
    #print(date_string)
    date = []
    if type(date_string) == str:
        i = 0
        curr_str = ""
        while(i < len(date_string)):
            obj = date_string[i]
            if obj == "/" or obj == " " or obj == ":" or obj == "-":
                date.append(curr_str) 
                curr_str = ""
            else:
                curr_str += str(obj)
            i+=1
        date.append(curr_str)
    else:
        date.append(date_string)
    return date

def total_time(speeds): #Ange speed i m/s
    if type(speeds) == int:
        speeds = [speeds]*len(RS.total_distance)
    total_time = []
    for i in range(1, len(RS.total_distance)):
        diff = RS.total_distance[i] - RS.total_distance[i-1]
        total_time.append(diff/speeds[i])
    return total_time

def time_at_stop(speeds):
    #Ange speed i m/s
    tt = total_time(speeds)
    dtc = date_time_converter(RS.time_arrived[0])
    ta = float(dtc[-1])/60 + float(dtc[-2])
    
    stop_time = []
    for i in range(len(tt)):
        ta += tt[i-1]
        if date_time_converter(RS.time_leave[i])[-2] == '08':
            ta = 8
        #print(ta)
        #print("ta = " +str(ta))
        stop_time.append(ta)
    return stop_time

"""
Controlstops baserad distansmätning

Gör en lista med alla distanser ungefär som convert_distances_to_coordinates.
Skillnaden är att vi kontrollerar och justerar distanserna.
"""

def cs_distances(file = file_name_1, plot = False, allt_i_ett = False):
    obj = read_txt(file)
    csc = control_stop_coordinates()
    i = 0
    last = obj[0][:2]
    first = 0
    f = 0
    dists = []
    for item in csc[1:]:
        stop = False
        while i < len(obj)-1 and not stop:
            current = obj[i][:2]
            cs = item[1:3]
            curr_l = [float(current[0]), float(current[1]), 0]
            cs_l = [float(cs[0]), float(cs[1]), 0]
            dist = convert_coordinates_to_distance([curr_l, cs_l])[0][0] # 1 -> en distans på 1 km
            if (float(current[0]) <= float(cs[0]) <= float(last[0])) or dist < 0.0001:
                distance = convert_coordinates_to_distance(obj[first: i])
                summa = sum_distance(distance, True)
                #print(dist)
                #print(item)
                #print(summa)
                if f >= 1:
                    diff = summa/(float(item[3]) - float(csc[f][3]))
                    #print(diff)
                    conv = convert_coordinates_to_distance(obj[first:i])
                    for c in conv:
                        c[0] /= diff
                        if allt_i_ett:
                            dists.append(c)
                    if not allt_i_ett:
                        dists.append(conv)
                #print(obj[i])
                i+=1
                stop = True
                #print(i)
                first = i
            else:
                #print(current)
                #print(cs)
                i+=1
                
            last = current
        f+=1
    if plot:
        cX = []
        cY = []
        for c in csc[1:]:
            cX.append(float(c[1]))
            cY.append(float(c[2]))
        oX = []
        oY = []
        for o in obj:
            oX.append(float(o[0]))
            oY.append(float(o[1]))
        cx = np.array(cX)
        cy = np.array(cY)
        ox = np.array(oX)
        oy = np.array(oY)
        plt.plot(cx, cy, "r*")
        plt.plot(ox, oy, "b-")
        plt.show()
    
    #all_distances = convert_coordinates_to_distance(obj)
    #res_dist = sum_distance(all_distances)
    
    return dists

def plot_altitude(distances):
    X = []
    Y = []
    for item in distances:
        X.append(item[0])
        Y.append(item[1])
    x = np.array(X)
    y = np.array(Y)
    plt.plot(x, y, "k-")
    plt.show()

def get_sections(all_distances, check_point_distances):
    streckor = []
    d = 1
    strecka = []
    for item in all_distances:
        if item[0] <= check_point_distances[d]:
            #print(check_point_distances[d])
            strecka.append(item)
        if item[0] >= check_point_distances[d]:
            if len(strecka) > 0:
                streckor.append(strecka)
                strecka = []
            if d < len(check_point_distances) - 1:
                d += 1
    return streckor

def get_even_sections(all_distances, num_sections):
    total_distance = all_distances[-1][0]
    delta = total_distance / num_sections
    #print(delta)
    dists = []
    for i in range(num_sections+1):
        dists.append(delta*(i))
    #print(dists)
    sections = get_sections(all_distances, dists)
    return sections

#CS = cs_distances(plot = True)

















