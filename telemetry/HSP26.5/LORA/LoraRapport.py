# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 10:54:36 2026

@author: oscar
"""

from reportlab.lib.colors import *
from reportlab.lib.pagesizes import *
from reportlab.lib.units import *
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from ReadData import *

new_page_y = 275
author = "Oscar Osbeck"

"""
Det går att snabba på processtiden genom att bara läsa in datafilen en gång
"""

def drivers_to_pdf():
    # Storlek A4: 210 * 297 mm
    title = "Körrapport LoRa "+str(datetime.datetime.now().date()) #+"("+top_lista+")"
    #t_namn = "Listing via " + top_lista
    canvas = Canvas("Körrapport "+ str(datetime.datetime.now().date())+".pdf", pagesize=A4)
    canvas.setFont("Times-Roman", 24)
    canvas.drawString(45*mm, 265 * mm, title)
    canvas.setFont("Times-Roman", 15)
    
    # Hämtar överskridande data om körningen
    filename = "allLoraData.txt"
    data = read_data_file(filename)

    # Bör förbättras i framtidem
    plats = "Falkenbergs motorbana 2026-05-19"
    
    canvas.drawString(35*mm, 253 * mm, "Tagen från listan "+ filename)
    canvas.setFont("Times-Roman", 12)
    canvas.setFillColor(black)
    
    # Hämtar alla förare
    drivers = read_drivers()
    
    page = 0
    x_edge = 24
    y_pos = 242
    canvas.setFont("Times-Roman", 14)
    canvas.drawString(x_edge*mm, y_pos*mm, 'Rapporten avser körningen på '+ plats)
    y_pos -= 10
    canvas.setFont("Times-Roman", 16)
    canvas.drawString(x_edge*mm, y_pos*mm, "Körningarna genomfördes av:")
    y_pos -= 7
    x_edge = 28
    canvas.setFont("Times-Roman", 13)
    for driver in drivers:
        #if driver in item:
        canvas.drawString(x_edge*mm, y_pos*mm, str(driver[2]) + ": "+ str(driver[1])[:-7])
        y_pos -= 7
        if y_pos < 30:
            page += 1
            canvas.showPage()
            canvas.setFont("Times-Roman", 14)
            canvas.setFillColor(black)
            y_pos = new_page_y
    
    #Inledning
    Inledning = ["""Rapporten är från testkörningen på Falkenbergs Motorbana den 19 Maj 2026. 
                    Denna dagen var vi 3 team på plats, vi i HUST från Högskolan i Halmstad, JUST
                    från Högskolan i Jönköping och CST från Chalmers i Göteborg. 
                    Under dagen har vi i HUST kört 4 testkörningar och JUST har kört (2?) testkörningar.
                    CST hade av tekniska skäl inte möjlighet att genomföra någon testkörning.
                    Vi i HUST hade en körning på parkeringen där folk från både vårat team och
                    folk från våra sponsorer deltog.
                    
                    Denna rapporten täcker samtliga av våra körningar.
                    Det verkar som att vi saknar en del data från när sponsorerna körde samt
                    när Jennie körde.
                    
                    Förbättringar kommenteras i slutet."""]    
    
    y_pos -= 8
    x_edge = 24
    canvas.setFont("Times-Roman", 17)
    canvas.drawString(x_edge*mm, y_pos*mm, "Inledning")
    canvas.setFont("Times-Roman", 13)
    y_pos -= 8
    
    for inl in Inledning:
        
        text_obj = canvas.beginText(x_edge*mm, y_pos*mm)
        text_obj.textLines(inl)
        canvas.drawText(text_obj)
        
        num_lines = len(inl.splitlines())
        line_height = 13 * 0.42  # fontstorlek 13
        #new_y = start_y - num_lines * line_height
        y_pos -= num_lines*line_height
        
        if y_pos < 30:
            page += 1
            canvas.showPage()
            canvas.setFont("Times-Roman", 13)
            canvas.setFillColor(black)
            y_pos = new_page_y
    
    indicies = [[0], [27], [1], [27, 17, 18, 19], [17, 18, 19], [11, 15, 16], [10, 11], [7,8,9], [4,5,6]]
    
    """
    Kommentarerna kan enkelt förbättras genom att exempelvis visa en graf och prompta
    användaren att skriva en kommentar
    """
    graf_kommentarer = [["Hastigheten ser ut som den ska",
                    "Vi kan se att vi stundtals har en väldigt hög motoreffekt men värdena ser rimliga ut.",
                    "Distansen rapporterades korrekt men med vissa extremvärden.",
                    "Vi ser bara motoreffekter eftersom solplanet vara av.",
                    "Här har vi ingen data eftersom solplanet var av.",
                    "Om man jämför med värdena i rapport del 1 finns det tydliga avvikelser. Vi får kolla mer på detta",
                    "",
                    "Här har vi åter igen några uppstickare men på det stora hela ser det bra ut.",
                    "Här måste det göras en filtrering, annars ser det rimligt ut",
                    ""],
                   ["Körde de verkligen så snabbt? Körde de bara en gång?",
                   "",
                   "Några extremvärden som bör rättas till.",
                   "Solplanet var av.",
                   "Här måste vi fått ett datafel",
                   "",
                   "",
                   "Här har vi åter igen några uppstickare men på det stora hela ser det bra ut.",
                   "Här måste det göras en filtrering",
                   ""],
                   ["Hastigheten ser normal ut men vi verkar ha blivit av med signalen.",
                   "",
                   "Det var denna körningen som hade problem med distansen.",
                   "Motoreffekten är åtrigen ofta högre än MPPT:erna.",
                   "Vi får väldigt konstiga värden från MPPT 1 men annars ser allt normalt ut.",
                   "Här ser det ut som att något har blivit galet.",
                   "",
                   "Det ser ut som att temperaturmätningen inte fungerat här, de borde inte vara samma.",
                   "Det här ser iallafall bra ut.",
                   ""],
                   ["Hastigheten ser ut som den ska men några uppstickare.",
                   "Här behöver vi ha filtrering.",
                   "Några glapp i kurvan men annars bra.",
                   "I grafen ser vi att motoereffekten ofta överskrider MPPT:erna, filtrering behövs",
                   "Storlekn på värdena ser helt rimliga ut, vi har några avstickare som bör filtreras.",
                   "Här är det svårt att se vad temperaturen faktist är, vi får filtrera bort extremvärdena",
                   "",
                   "Här har vi åter igen några uppstickare men på det stora hela ser det bra ut.",
                   "Här måste det göras en filtrering",
                   ""],
                   ["Hastigheten ser ut som den ska",
                   "Vi kan se att vi stundtals har en väldigt hög motoreffekt men värdena ser rimliga ut.",
                   "Ser bra ut, lite filtrering behöver göras.",
                   "I grafen ser vi att motoereffekten ofta överskrider MPPT:erna",
                   "Storlekn på värdena ser helt rimliga ut, dock ser det ut som att värdena pendlar kraftigt.",
                   "Här är det svårt att se vad temperaturen faktist är, vi får filtrera bort extremvärdena",
                   "",
                   "Här har vi åter igen några uppstickare men på det stora hela ser det bra ut.",
                   "Här måste det göras en filtrering",
                   ""]]
    
    y_pos -= 10
    x_edge = 24
    canvas.drawString(x_edge*mm, y_pos*mm, "Vi tittar på all data i kronologisk ordning")
    y_pos -= 17
    canvas.drawString(x_edge*mm, y_pos*mm, "Skriven av "+author + " " +str(datetime.datetime.now().date()))
    canvas.setFont("Times-Roman", 15)
    y_pos -= 17
    
    page += 1
    canvas.showPage()
    canvas.setFont("Times-Roman", 12)
    canvas.setFillColor(black)
    y_pos = new_page_y
    
    
    d = 0 # Numrering av förarna
    for driver in drivers:
        i = 0
        
        #Skriver ut föraren och starttiden
        canvas.setFont("Times-Roman", 19)
        canvas.drawString(x_edge*mm, y_pos*mm, str(driver[2]) + ": "+ str(driver[1])[:-7])
        y_pos -= 12
        
        for item in indicies:
            
            namn, datum = plot_lora_driver(driver[2], item, savename = "first"+str(item)+str(driver[2]), data = data)
            canvas.setFont("Times-Roman", 15)
            rubrik = ""
            #if i == 0:
            #    rubrik = "Vi börjar med att kolla på "
            for t in item:
                rubrik += ManuellLora[t] +", "
            rubrik = rubrik[:-2]
            canvas.drawString(x_edge*mm, y_pos*mm, rubrik)
            try:
                y_pos -= 10
                canvas.setFont("Times-Roman", 12)
                canvas.drawString(x_edge*mm, y_pos*mm, graf_kommentarer[d][i])
            except IndexError:
                pass
                #y_pos += 130
            bild_hojd = 100
            #print(text.getY())
            if i == 0:
                canvas.drawImage(namn, x_edge*mm, (y_pos-bild_hojd-5)*mm, width = (8/5*bild_hojd)*mm, height = bild_hojd*mm)
            else:
                canvas.drawImage(namn, x_edge*mm, (y_pos-bild_hojd-5)*mm, width = (8/5*bild_hojd)*mm, height = bild_hojd*mm)
            os.remove(namn)
            y_pos -= (bild_hojd + 30)
            i += 1
            
            if y_pos < bild_hojd:
                page += 1
                canvas.showPage()
                canvas.setFont("Times-Roman", 12)
                canvas.setFillColor(black)
                y_pos = new_page_y
        d += 1
        
    # Skriver förbättringsområden i slutet av rapporten 
    forbattringar = ["""- Tydligara dokumentation för vilket index som avser vilket värde!
                     - Måste vara tydligt om det avser LoRa eller SD-kort!
                     - Denna rapporten saknar data för återstående batterimängd samt värden mot distans.
                     - Det finns tydliga behov att fixa filtrering av extrema värden.
                     - Vi ser inte ut att ha fått med hela körningarna, iallafall inte från Jennie.
                     - Dubbelkolla att datan avser det som står angivet.
                     - Gämföra data med SD-kortet, det som ska kollas i denna jämförelse är om tiden
                       ser lika dan ut i de båda fallen. LoRa-datan stämmer eftersom varje datavärde 
                       har fått sin tid noterad live från klockan på min dator. Det kan vara så att
                       datan på SD-kortet inte läses in med exakt en sekunds intevall.
                     - Samt förbättringar som har nämnts i del 1."""]    
    
    """
    page += 1
    canvas.showPage()
    canvas.setFont("Times-Roman", 12)
    canvas.setFillColor(black)
    y_pos = new_page_y
    """
    
    y_pos -= 20
    x_edge = 24
    canvas.setFont("Times-Roman", 17)
    canvas.drawString(x_edge*mm, y_pos*mm, "Förbättringsområden")
    canvas.setFont("Times-Roman", 13)
    y_pos -= 8
    
    for forb in forbattringar:
        
        text_obj = canvas.beginText(x_edge*mm, y_pos*mm)
        text_obj.textLines(forb)
        canvas.drawText(text_obj)
        
        num_lines = len(forb.splitlines())
        line_height = 13 * 0.4  # fontstorlek 13
        #new_y = start_y - num_lines * line_height
        y_pos -= num_lines*line_height
        
        y_pos -= 12
        if y_pos < bild_hojd:
            page += 1
            canvas.showPage()
            canvas.setFont("Times-Roman", 13)
            canvas.setFillColor(black)
            y_pos = new_page_y
        
    canvas.save()
    


drivers_to_pdf()


