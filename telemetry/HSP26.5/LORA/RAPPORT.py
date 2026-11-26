# -*- coding: utf-8 -*-
"""
Created on Fri Feb  6 13:48:16 2026

@author: oscar
"""

from RESA import *

from reportlab.lib.colors import *
from reportlab.lib.pagesizes import *
from reportlab.lib.units import *
from reportlab.pdfgen.canvas import Canvas


sven_jr = solar_car("Sven jr", 269.5, 0.867, 1.2, 0.2, 0.003, 3, 0.9, 3055, 0.23, 6)



def check_new_page(y_pos, page, canvas):
    if y_pos < 30:
        page += 1
        canvas.showPage()
        canvas.setFont("Times-Roman", 12)
        canvas.setFillColor(black)
        y_pos = 265
    return y_pos, page

def report(solar_car = sven_jr):
    all_distances = cs_distances(allt_i_ett=True)

    res_dist = sum_distance(all_distances)

    standard_date = "2025-08-09T08:00:00"
    
    velocity = 63 /3.6
    
    r_trip = trip(res_dist, velocity, standard_date, solar_car)
    
    
    # Storlek A4: 210 * 297 mm
    title = "Rapport "+str(datetime.datetime.now().date())
    t_namn = ""
    canvas = Canvas("Rapport "+ str(datetime.datetime.now().date())+".pdf", pagesize=A4)
    canvas.setFont("Times-Roman", 24)
    canvas.drawString(60*mm, 265 * mm, title)
    canvas.setFont("Times-Roman", 12)
    canvas.setFillColor(black)
    
    page = 0
    x_edge = 24
    y_pos = 253
    canvas.setFont("Times-Roman", 14)
    canvas.drawString(x_edge*mm, y_pos*mm, 'Bilspecs')
    x_edge = 26
    x_right = 90
    y_pos -= 10
    canvas.setFont("Times-Roman", 12)
    canvas.drawString(x_edge*mm, y_pos*mm, 'Namn: ')
    canvas.drawString(x_right*mm, y_pos*mm, solar_car.name)
    y_pos -= 8
    canvas.drawString(x_edge*mm, y_pos*mm, 'Vikt: ')
    canvas.drawString(x_right*mm, y_pos*mm, str(solar_car.weight)+ " kg")
    y_pos -= 8
    canvas.drawString(x_edge*mm, y_pos*mm, 'Front Area: ')
    canvas.drawString(x_right*mm, y_pos*mm, str(solar_car.front_area) + "m^2")
    y_pos -= 8
    canvas.drawString(x_edge*mm, y_pos*mm, 'Luftdensitet: ')
    canvas.drawString(x_right*mm, y_pos*mm, str(solar_car.rho)+"kg/m^3")
    y_pos -= 8
    canvas.drawString(x_edge*mm, y_pos*mm, 'Drag koefficient: ')
    canvas.drawString(x_right*mm, y_pos*mm, str(solar_car.drag))
    y_pos -= 8
    canvas.drawString(x_edge*mm, y_pos*mm, 'Rullmotsånd per hjul: ')
    canvas.drawString(x_right*mm, y_pos*mm, str(solar_car.rolling_res_per_wheel))
    y_pos -= 8
    canvas.drawString(x_edge*mm, y_pos*mm, 'Antal hjul: ')
    canvas.drawString(x_right*mm, y_pos*mm, str(solar_car.num_wheels)+ " st")
    y_pos -= 8
    canvas.drawString(x_edge*mm, y_pos*mm, 'Drivlinans effektivitet: ')
    canvas.drawString(x_right*mm, y_pos*mm, str(solar_car.efficiency_my))
    y_pos -= 8
    canvas.drawString(x_edge*mm, y_pos*mm, 'Batterikapacitet: ')
    canvas.drawString(x_right*mm, y_pos*mm, str(int(solar_car.battery_capacity/1000)) +" Wh")
    y_pos -= 8
    canvas.drawString(x_edge*mm, y_pos*mm, 'Batteri vid start: ')
    canvas.drawString(x_right*mm, y_pos*mm, str(int(solar_car.battery_left/1000)) +" Wh")
    y_pos -= 8
    canvas.drawString(x_edge*mm, y_pos*mm, 'Solplanets effektivitet: ')
    canvas.drawString(x_right*mm, y_pos*mm, str(round(solar_car.eff_factor*100,1)) + "%")
    y_pos -= 8
    canvas.drawString(x_edge*mm, y_pos*mm, 'Solplanets area: ')
    canvas.drawString(x_right*mm, y_pos*mm, str(solar_car.solar_area)+ " m^2")
    y_pos -= 10
    
    canvas.setFont("Times-Roman", 16)
    canvas.drawString(x_edge*mm, y_pos*mm, "Resan")
    y_pos -= 7
    x_edge = 28
    canvas.setFont("Times-Roman", 12)
    canvas.drawString(x_edge*mm, y_pos*mm, 'Resan börjar i '+r_trip.stops[0][0]+" och slutar i "+r_trip.stops[-1][0])
    y_pos -= 7
    canvas.drawString(x_edge*mm, y_pos*mm, 'Resan är '+str(float(r_trip.stops[-1][1])-float(r_trip.stops[0][1]))+" km lång")
    y_pos -= 7
    if r_trip.breakdown:
        canvas.drawString(x_edge*mm, y_pos*mm, "Efter "+str(round(r_trip.positions[-1][0], 2))+"km tog resan slut pga tomt batteri")
    elif r_trip.pass_control:
        canvas.drawString(x_edge*mm, y_pos*mm, "Bilen klarade hela resan på "+r_trip.total_time)
        y_pos -= 6
        canvas.drawString(x_edge*mm, y_pos*mm, "Detta räckte för att komma i mål i tid")
    else:
        canvas.drawString(x_edge*mm, y_pos*mm, "Bilen klarade hela resan på "+r_trip.total_time)
        y_pos -= 6
        canvas.drawString(x_edge*mm, y_pos*mm, "Detta räckte inte för att komma i mål i tid")
    
    y_pos -= 9
    x_edge = 26
    canvas.setFont("Times-Roman", 14)
    canvas.drawString(x_edge*mm, y_pos*mm, 'Stop med distanser')
    y_pos -= 8
    x_edge = 28
    canvas.setFont("Times-Roman", 12)
    canvas.drawString(x_edge*mm, y_pos*mm, 'Programmet har identifierat följande stop. Stoppens distanser är också angivna.')
    y_pos -= 7
    canvas.drawString(x_edge*mm, y_pos*mm, 'Det kan förekomma stop som inte står med nedan, stoppen som identifierats under är även')
    y_pos -= 7
    canvas.drawString(x_edge*mm, y_pos*mm,'platserna som använts för väderdata.')
    
    y_pos -= 9
    x_right = 90
    canvas.drawString(x_edge*mm, y_pos*mm, "Stop")
    canvas.drawString(x_right*mm, y_pos*mm, "Strecka från start")
    y_pos -= 8
    for item in r_trip.stops:
        stop = item[0]
        distans = item[1]
        canvas.drawString(x_edge*mm, y_pos*mm, stop)
        canvas.drawString(x_right*mm, y_pos*mm, distans+"km")
        y_pos -= 8
        
        y_pos, page = check_new_page(y_pos, page, canvas)
        
    x_edge = 26
    canvas.setFont("Times-Roman", 15)
    canvas.drawString(x_edge*mm, y_pos*mm, "Altitud")
    y_pos -= 8
    x_edge = 28
    canvas.setFont("Times-Roman", 12)
    canvas.drawString(x_edge*mm, y_pos*mm, "Här kommer en graf med altituden under resan")
    y_pos -= 8
    r_trip.plot_altitude()
    im = "altimage.png"
    std_height = 190
    y_pos -= std_height/2.62
    canvas.drawImage(im, x_edge*mm, y_pos*mm, std_height*1.6, std_height)
    os.remove(im)
    y_pos -= 9
    x_edge = 24
    
    
    canvas.setFont("Times-Roman", 16)
    canvas.drawString(x_edge*mm, y_pos*mm, "Mätningar under resan")
    x_edge = 27
    y_pos -= 8
    canvas.setFont("Times-Roman", 13)
    for i in range(7, len(r_trip.poss_descriptions)):
        canvas.drawString(x_edge*mm, y_pos*mm, r_trip.poss_descriptions[i])
        r_trip.plot_positions(i, True)
        im = "image"+str(i)+".png"
        std_height = 180
        y_pos -= std_height/2.62
        y_pos, page = check_new_page(y_pos, page, canvas)
        if y_pos > 265 - std_height/2.62:
            y_pos = 265 - std_height/2.62
        canvas.drawImage(im, x_edge*mm, y_pos*mm, std_height*1.6, std_height)
        os.remove(im)
        
        y_pos -= 8
        
        y_pos, page = check_new_page(y_pos, page, canvas)
            
    
    
    canvas.save()
    
    return r_trip
    
report()


add_session("Report")
