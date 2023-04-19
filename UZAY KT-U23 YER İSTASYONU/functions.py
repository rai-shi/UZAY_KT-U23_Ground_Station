import time

import serial

from tkinter import *
from tkinter import ttk 
from tkinter import filedialog

#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
#from mpl_toolkits.mplot3d import Axes3D
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

import os

import csv 

import ftplib

from pygrabber.dshow_graph import FilterGraph

import cv2 

import tkintermapview 

from PIL import ImageTk
import PIL.Image 

import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.freeglut import *
#import numpy as np
from pyopengltk import OpenGLFrame
#import math

import re 
import threading



ktu_blue= "#1f5ba1"
light_grey = "#C6C7CA"
dark_grey= "#282A3A"

class threadFactory():
    def __init__(self,target_, args_:tuple=None, daemon_:bool=False ):
        self.target = target_ 
        self.justargs = args_ 
        self.daemon = daemon_
        self.stop_event = threading.Event()

    def create(self):
        if self.justargs != None:
            self.args = (self.stop_event, ) + self.justargs              
        else:
            self.args = (self.stop_event, )           
        self.thread = threading.Thread(target = self.target, args=self.args, daemon=self.daemon) 

    def start(self):
        self.thread.start() 

    def finish(self):
        self.stop_event.set()
        self.thread.join()  
        print("function close")

def clock(label:Label):
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    day= time.strftime("%d")
    month= time.strftime("%m")
    year= time.strftime("%Y")
    
    label.config(text= hour+":"+minute+":"+second+"   "+day+"/"+month+"/"+year)
    label.after(1000, clock, label)

class HandleLine:
    def __init__(self):
        self.datas = [] 
        self.result = b''

    def setDatas(self,data):
        self.datas.append(data)

    def getDatas(self):
        try:
            result = self.datas[-1]
            #self.datas.pop(0)
            return result
        except:
            print("henüz veri yok")

class PacketReader:
    def __init__(self, ser_, handler_:HandleLine, timeout=1, eol=b'\r\n'):
        self.ser = ser_
        self.eol = eol
        self.buffer = b''
        self.lock = threading.Lock()
        self.handler = handler_
        
    def read_packet(self):
        with self.lock:
            packet = None
            if self.eol in self.buffer:
                packet, self.buffer = self.buffer.split(self.eol, 1)
            if packet != None:
                print(packet)
                self.handler.setDatas(packet)
    
    def read_thread(self):
        while True:
            with self.lock:
                try:
                    self.buffer += self.ser.read(self.ser.in_waiting or 1)   
                except:
                    pass
            time.sleep(0.5) # 0.05
            
    def start(self):
        threading.Thread(target=self.read_thread, daemon=True).start()


global port 
port = str()
global speed
speed = int()

def getConnectInfo( port_:ttk.Combobox, speed_:ttk.Combobox):
    global port 
    global speed 

    port=port_.get()
    speed = int(speed_.get())

def PortConnect(event:threading.Event, ser: serial.Serial, handler:HandleLine, text:Label):
    if event.is_set():
        return
    try:
        global port 
        global speed

        ser.port=port
        ser.baudrate = speed

        ser.setDTR(True)
        ser.setRTS(True)  

        ser.open()

        if ser.isOpen():

            text['background'] = 'green'
            text.configure(text="BAĞLANTI KURULDU")

            reader = PacketReader(ser_ = ser, handler_=handler )
            reader.start() 
            while True:
                reader.read_packet()
                time.sleep(0.5) 

    except:
            text['background'] = "red"
            text.configure(text="Yanlış Bilgi Girildi")



def isStatusWord(statusWord:str)->bool:
    statusWords = ["1","2", "3",
                  "4","5", 
                  "6", "7", "8", "GELİŞTİRME"]
    if statusWord in statusWords:
        return True
    else :
        return False

def ProperAras(arasCode:str)->str:  # yanlış kodu -1 yollar
    aras1 = str 
    aras2 = str 
    aras3 = str 
    aras4 = str 
    aras5 = str 
    
    if arasCode[0] == '1' or arasCode[0] == '0':
        aras1 = arasCode[0]
    else:
        aras1="-1"

    if arasCode[1] == '1' or arasCode[1] == '0':
        aras2 = arasCode[1]
    else:
        aras2="-1"

    if arasCode[2] == '1' or arasCode[2] == '0':
        aras3 = arasCode[2]
    else:
        aras3 = "-1"

    if arasCode[3] == '1' or arasCode[3] == '0':
        aras4 = arasCode[3]
    else:
        aras4="-1"

    if arasCode[4] == '1' or arasCode[4] == '0':
        aras5 = arasCode[4]
    else:
        aras5="-1"

    return aras1+aras2+aras3+aras4+aras5

# saat düzeltilecek
def ProperHour(hour:str)->str:
    
    pattern = "[0-9]+/[0-9]+/[0-9]+,[0-9]+/[0-9]+/[0-9]+"
    if re.fullmatch(pattern,hour):
        return hour 
    else:
        return "00/00/2023,00/00/00"
    
    #hourPart1 = str
    #hourPart2 = str
    #MinutePart1 = str
    #MinutePart2 = str

    #if (hour[0].isdigit()) and (hour[1].isdigit()) and (hour[3].isdigit()) and (hour[4].isdigit()):
    #    hourPart1 = hour[0]
    #    hourPart2 = hour[1]
    #    MinutePart1 = hour[3]
    #    MinutePart2 = hour[4]
        
    #    return hourPart1 + hourPart2 +":" + MinutePart1 + MinutePart2
    #else:
    #    return "00:00"

def isHeight(height_param:str)->bool:

    height = height_param.replace('.','',1)
    height = height.replace('-','',1)

    if height.isdigit():  #yükseklik1
        return True
    else:
        return False

def isVelocity(velocity_param:str)->bool:

    velocity = velocity_param.replace('.','',1)
    velocity = velocity.replace('-','',1)

    if velocity.isdigit():  
        return True
    else:
        return False

def isPositionData(position_param:str)->bool:
    position = position_param.replace('.','',1)
    position = position.replace('-','',1)

    if position.isdigit():  
        return True
    else:
        return False
      
    

def ConvertDatas(datas:list)->list:
    # önce veri istenilen türde mi kontrol et sonra istenilene dönüştür
    # değilse 0.0 ya da null_str ata
    #'3.14'.replace('.','',1).isdigit()
    
    properDatas = list()

    if datas[0].isdigit(): # counter
        properDatas.append(int(datas[0]))
    else:
        properDatas.append(int("0"))
    if isStatusWord(datas[1]): #statu
        properDatas.append(str(datas[1]))
    else:
        properDatas.append(str("hatalı_durum_kelimesi"))


    properDatas.append(ProperAras(datas[2])) # aras

    properDatas.append(ProperHour(datas[3])) # saat 
 
    if datas[4].replace('.','',1).isdigit():  #basınç1
        properDatas.append(float(datas[4]))
    else:
        properDatas.append(float("0.0"))

    if datas[5].replace('.','',1).isdigit():  #basınç2
        properDatas.append(float(datas[5]))
    else:
        properDatas.append(float("0.0"))

    if isHeight(datas[6]):  #yükseklik1
        properDatas.append(float(datas[6]))
    else:
        properDatas.append(float("0.0"))

    if isHeight(datas[7]):  #yükseklik2
        properDatas.append(float(datas[7]))
    else:
        properDatas.append(float("0.0"))

    if datas[8].replace('.','',1).isdigit():  #irtifa
        properDatas.append(float(datas[8]))
    else:
        properDatas.append(float("0.0"))

    if isVelocity(datas[9]):  #hız
        properDatas.append(float(datas[9]))
    else:
        properDatas.append(float("0.0"))

    if datas[10].replace('.','',1).isdigit():  #sicaklık
        properDatas.append(float(datas[10]))
    else:
        properDatas.append(float("0.0"))

    if datas[11].replace('.','',1).isdigit():  #pil
        properDatas.append(float(datas[11]))
    else:
        properDatas.append(float("0.0"))

    if datas[12].replace('.','',1).isdigit():  #lat1
        properDatas.append(float(datas[12]))
    else:
        properDatas.append(float("0.0"))

    if datas[13].replace('.','',1).isdigit():  #long1
        properDatas.append(float(datas[13]))
    else:
        properDatas.append(float("0.0"))

    if datas[14].replace('.','',1).isdigit():  #alt1
        properDatas.append(float(datas[14]))
    else:
        properDatas.append(float("0.0"))

    if isPositionData( datas[15]):  #pitch
        properDatas.append(float(datas[15]))
    else:
        properDatas.append(float("0.0"))

    if isPositionData( datas[16]):  #roll
        properDatas.append(float(datas[16]))
    else:
        properDatas.append(float("0.0"))

    if isPositionData( datas[17]):  #yaw
        properDatas.append(float(datas[17]))
    else:
        properDatas.append(float("0.0"))

    properDatas.append("145812")  # takım no kontrolü 18 
            
    properDatas.append(" ") # 19 yani 1-20'ye


    return properDatas
          

def GetData(ser:serial.Serial, handler:HandleLine, text:Label, pureTeleLabel:Label)->tuple :

    pureData = b'' # serialden alınan veri
    properDatas = list() # her şeyi düzgünleştirilmiş veri


    if ser.isOpen():

        pureData = handler.getDatas()

        if pureData != None:

            if pureData != b'':

                # buraya dikkat 
                #pureTeleLabel.configure(text=pureData)
                try: 
                    strDatas = pureData.decode('UTF-8') # byte->str dönüşüm
                    lessThanSignCount = strDatas.count("<") # 19
                    greaterThanSignCount = strDatas.count(">") # 19
                    commaCount = strDatas.count(",") # 18

                    if (lessThanSignCount==19) and ( greaterThanSignCount==19) and ( commaCount==18 ):
                        # veri düzgün "< > ," lar silinecek tek tek veriler kontrol edilecek
                
                        strDatas = strDatas.replace("<"," ")
                        strDatas = strDatas.replace(">"," ")
                        datasList = strDatas.split(",")

                        for item in range(0,19): # boşlukları silme
                            datasList[item] = datasList[item].lstrip()
                            datasList[item] = datasList[item].rstrip()

                        lastElementOfDatasList = datasList[-1]
                        lastElementOfDatasList = lastElementOfDatasList.replace(" \r\n"," ")
                        datasList[-1] = lastElementOfDatasList
 

                        properDatas = ConvertDatas(datasList)
                        text['background'] = "green"
                        text.configure(text="Başarılı Veri")
                        return_tuple = (True, properDatas)
                        return return_tuple

                    else:
                        # < > , tam değil
                        text['background'] = "red"
                        text.configure(text="Hatalı Veri Bütünü")
                        returnFautl_tuple = (False,pureData)
                        return returnFautl_tuple
                except:
                    # decode'lanamayan veri
                    text['background'] = "red"
                    text.configure(text="decode edilemedi!")
                    returnFautl_tuple = (False,pureData)
                    return returnFautl_tuple

            else:
                # boş veri
                text['background'] = "red"
                text.configure(text="Boş Veri")
                EmptyData = []
                returnFautl_tuple = (False,EmptyData)
                return returnFautl_tuple
                
        else: 
            # boş veri
            text['background'] = "red"
            text.configure(text="Boş Veri")
            EmptyData = []
            returnFautl_tuple = (False,EmptyData)
            return returnFautl_tuple
    else:
        # port açık değil
        text['background'] = "red"
        text.configure(text="Port Açık Değil")
        EmptyData = []
        returnFautl_tuple = (False,EmptyData)
        return returnFautl_tuple



def WriteAllOfIt(datas:list, tabFrame:Frame):

    teleTitle = ["Paket no: ","Durum: ","ARAS: ", "Saat: ",
            "G.Y. Basıncı: ","T. Basıncı: ",
            "G.Y. Yüksekliği: ","T. Yüksekliği: ",
            "İrtifa Farkı: ","İniş Hızı: ",
            "Sıcaklık: ",
            "Pil Gerilimi: ",
            "G.Y. Latitude: ","G.Y. Longitude: ","G.Y. Altitude: ",
            "Pitch: ","Roll: ","Yaw: ",
            "Takım No: ", " "]

    units = [ 
        " ", " ", " ", " ", 
        " hPa", " hPa", " m", " m",
        " m", " m/s", " °C", " V",
        " ", " ", " ",
        " °", " °", " °", " ", " "]

    dataIndex = 0
    for col in range(4):
        for rw in range(5):
            textData = Label(tabFrame, anchor = "w",width= 32, font=("Helvetica",9), text= (teleTitle[dataIndex]+ str(datas[dataIndex])+ units[dataIndex]), bg=light_grey)
            textData.grid(row=rw, column=col, padx=4, pady=10)
            dataIndex = dataIndex +1 

global packet
packet = 1
def TeleTableListing(datas:list, tabFrame:Frame):

    global packet 
    packetNum = Label(tabFrame, text = packet,bg= light_grey, anchor="w",width=6)
    packetNum.grid(row=packet, column=0,padx=2.5, pady=0.5)

    for item in range(1,20):
        takenData = Label(tabFrame,text= datas[item-1],font=("Helvetica",8),bg= light_grey, anchor='w', width=6, borderwidth=2, relief="groove")  # 23
        takenData.grid(row=packet, column=item, padx=2.5, pady=0.5)

    packet += 1

#def GraphIt(myplot:Figure ,xindex:int, yindex:int, canvas:Canvas, datas:list, old_datas:list):

#    x1 = int(xindex)
#    y1 = float(datas[yindex])
    
#    if old_datas:
#        x0 = int(x1-1)
#        y0 = float(old_datas[yindex])
#        myplot.plot( [x0,x1],[y0,y1], color='#0059aa', linestyle= '-') 

#    canvas.draw()

def GraphIt(dict_items:list ,xindex:int, datas:list, old_datas:list):
    for dict_item in dict_items:
        x1 = int(xindex)
        y1 = float(datas[dict_item['yindex']]) 

        if old_datas:
            x0 = int(x1-1) 
            y0 = float(old_datas[dict_item['yindex']])
            dict_item['plot'].plot( [x0,x1], [y0,y1], color='#0059aa', linestyle= '-' )
            #dict_item['plot'].autoscale()
            #dict_item['plot'].ticklabel_format(useOffset=False)
        dict_item['canvas'].draw()

def Aras(frames:list,values:str):
    for index in range(5):
    
        if(int(values[index])):
            frames[index]['background'] = "red"      
        else:
   
            frames[index]['background'] = "green"

def StatuChange(statu_data:str, labels:list[Label] ):
    if statu_data != None:
        if statu_data == "1":
            labels[0]['background'] = "green"

        if statu_data == "2":
            labels[0]['background'] = "green"
            labels[1]['background'] = "green"
            labels[2]['background'] = light_grey
            labels[3]['background'] = light_grey
            labels[4]['background'] = light_grey
            labels[5]['background'] = light_grey
            labels[6]['background'] = light_grey
            labels[7]['background'] = light_grey

        if statu_data == "3":
            labels[0]['background'] = "green"
            labels[1]['background'] = "green"
            labels[2]['background'] = "green"
            labels[3]['background'] = light_grey
            labels[4]['background'] = light_grey
            labels[5]['background'] = light_grey
            labels[6]['background'] = light_grey
            labels[7]['background'] = light_grey

        if statu_data == "4":
            labels[0]['background'] = "green"
            labels[1]['background'] = "green"
            labels[2]['background'] = "green"
            labels[3]['background'] = "green"
            labels[4]['background'] = light_grey
            labels[5]['background'] = light_grey
            labels[6]['background'] = light_grey
            labels[7]['background'] = light_grey

        if statu_data == "5":
            labels[0]['background'] = "green"
            labels[1]['background'] = "green"
            labels[2]['background'] = "green"
            labels[3]['background'] = "green"
            labels[4]['background'] = "green"
            labels[5]['background'] = light_grey
            labels[6]['background'] = light_grey
            labels[7]['background'] = light_grey

        if statu_data == "6":
            labels[0]['background'] = "green"
            labels[1]['background'] = "green"
            labels[2]['background'] = "green"
            labels[3]['background'] = "green"
            labels[4]['background'] = "green"
            labels[5]['background'] = "green"
            labels[6]['background'] = light_grey
            labels[7]['background'] = light_grey

        if statu_data == "7":
            labels[0]['background'] = "green"
            labels[1]['background'] = "green"
            labels[2]['background'] = "green"
            labels[3]['background'] = "green"
            labels[4]['background'] = "green"
            labels[5]['background'] = "green"
            labels[6]['background'] = "green"
            labels[7]['background'] = light_grey

        if statu_data == "8":
            labels[0]['background'] = "green"
            labels[1]['background'] = "green"
            labels[2]['background'] = "green"
            labels[3]['background'] = "green"
            labels[4]['background'] = "green"
            labels[5]['background'] = "green"
            labels[6]['background'] = "green"
            labels[7]['background'] = "green"

        if statu_data == "GELİŞTİRME":
            labels[0]['background'] = "blue"
            labels[1]['background'] = "blue"
            labels[2]['background'] = "blue"
            labels[3]['background'] = "blue"
            labels[4]['background'] = "blue"
            labels[5]['background'] = "blue"
            labels[6]['background'] = "blue"
            labels[7]['background'] = "blue"
       
def Mapping(map_:tkintermapview.TkinterMapView, locationDatasList:list): 

    x_locationYuk = locationDatasList[0]
    y_locationYuk = locationDatasList[1]

    yukMap = map_
   
    yukMap.delete_all_marker()

    yukMap.set_position(x_locationYuk,y_locationYuk, marker=True)          

def hexagone(z:float, colorTop:tuple, colorSide:tuple):
    tophexagone= [
        ((0,2,z+.5), (0,0,z+.5), (1,2,z+.5) ),
        ((1,2,z+.5), (0,0,z+.5), (2,1,z+.5)),
        ((2,1,z+.5), (0,0,z+.5), (2,0,z+.5)),
        ((2,0,z+.5), (0,0,z+.5), (2,-1,z+.5)),
        ((2,-1,z+.5), (0,0,z+.5), (1,-2,z+.5)),
        ((1,-2,z+.5), (0,0,z+.5), (0,-2,z+.5)),
        ((0,-2,z+.5), (0,0,z+.5), (-1,-2,z+.5)),
        ((-1,-2,z+.5), (0,0,z+.5), (-2,-1,z+.5)),
        ((-2,-1,z+.5), (0,0,z+.5), (-2,0,z+.5)),
        ((-2,0,z+.5), (0,0,z+.5), (-2,1,z+.5)),
        ((-2,1,z+.5), (0,0,z+.5), (-1,2,z+.5)),
        ((-1,2,z+.5), (0,0,z+.5), (0,2,z+.5))
        ]
    # .102, .178, .255
    glColor3f(*colorTop)
    glBegin(GL_TRIANGLES)  
    for triangles in tophexagone:
        for vertex in triangles:
            glVertex3fv(vertex)
    glEnd()


    quads = [((-1,2,z+.5), (1,2,z+.5), (1,2,z), (-1,2,z) ),
             ((1,2,z+.5), (2,1,z+.5) , (2,1,z), (1,2,z) ),
             ((2,1,z+.5), (2,-1,z+.5), (2,-1,z), (2,1,z) ),
             ((2,-1,z+.5), (1,-2,z+.5), (1,-2,z), (2,-1,z) ),
             ((1,-2,z+.5), (-1,-2,z+.5), (-1,-2,z), (1,-2,z) ),
             ( (-1,-2,z+.5), (-2,-1,z+.5), (-2,-1,z), (-1,-2,z) ),
             ( (-2,-1,z+.5), (-2,1,z+.5), (-2,1,z), (-2,-1,z) ),
             ( (-2,1,z+.5), (-1,2,z+.5), (-1,2,z), (-2,1,z) ),
        ]
    glColor3f(*colorSide)
    glBegin(GL_QUADS) 
    for quad in quads:
        for vertex in quad:
            glVertex3fv(vertex)
    glEnd()


    bottomhexagone= [
        ((0,2,z), (0,0,z), (1,2,z) ),
        ((1,2,z), (0,0,z), (2,1,z) ),
        ((2,1,z), (0,0,z), (2,0,z) ),
        ((2,0,z), (0,0,z), (2,-1,z) ),
        ((2,-1,z), (0,0,z), (1,-2,z) ),
        ((1,-2,z), (0,0,z), (0,-2,z) ),
        ((0,-2,z), (0,0,z), (-1,-2,z) ),
        ((-1,-2,z), (0,0,z), (-2,-1,z) ),
        ((-2,-1,z), (0,0,z), (-2,0,z) ),
        ((-2,0,z), (0,0,z), (-2,1,z) ),
        ((-2,1,z), (0,0,z), (-1,2,z) ),
        ((-1,2,z), (0,0,z), (0,2,z) )
        ]
    glColor3f(*colorTop)
    glBegin(GL_TRIANGLES)  
    for triangles in bottomhexagone:
        for vertex in triangles:
            glVertex3fv(vertex)
    glEnd()
#üst
def flaments_one(z:float, height:float):

    flaments = [
        ( (-.125,1.5,z), (.125,1.5,z), (.125,1.25,z), (-.125,1.25,z) ),

        ( (.125,1.5,z), (.125,1.5,z+height), (.125,1.25,z+height), (.125,1.25,z) ),
        ( (-.125,1.5,z), (-.125,1.5,z+height), (.125,1.5,z+height), (.125,1.5,z) ),
        ( (-.125,1.5,z), (-.125,1.5,z+height), (-.125,1.25,z+height), (-.125,1.25,z) ),
        ( (-.125,1.25,z), (-.125,1.25,z+height), (.125,1.25,z+height), (.125,1.25,z) ), 

        ( (-.125,1.5,z+height), (.125,1.5,z+height), (.125,1.25,z+height), (-.125,1.25,z+height) ),
        ]
    colors = [
        (0,0.5,0.5),
       (0,0.5,0.5),(0,0.5,0.5),(0,0.5,0.5),(0,0.5,0.5), 
       (0,0.5,0.5)
    ]
    glBegin(GL_QUADS)  
    for quads, color in zip(flaments, colors):
        glColor3fv(color)
        for vertex in quads:
            glVertex3fv(vertex)
    glEnd()
#sol
def flaments_two(z:float, height:float):

    flaments = [
        ( (-1.5,.125,z), (-1.25,.125,z), (-1.25,-.125,z), (-1.5,-.125,z) ),

        ( (-1.25,.125,z), (-1.25,.125,z+height), (-1.25,-.125,z+height), (-1.25,-.125,z) ),
        ( (-1.5,.125,z), (-1.5,.125,z+height), (-1.25,.125,z+height), (-1.25,.125,z) ),
        ( (-1.5,.125,z), (-1.5,.125,z+height), (-1.5,-.125,z+height), (-1.5,-.125,z) ),
        ( (-1.5,-.125,z), (-1.5,-.125,z+height), (-1.25,-.125,z+height), (-1.25,-.125,z) ),

        ( (-1.5,.125,z+height), (-1.25,.125,z+height), (-1.25,-.125,z+height), (-1.5,-.125,z+height) ),
        ]
    colors = [
        (0,0.5,0.5),
       (0,0.5,0.5),(0,0.5,0.5),(0,0.5,0.5),(0,0.5,0.5), 
       (0,0.5,0.5)
    ]
    glBegin(GL_QUADS)  
    for quads, color in zip(flaments, colors):
        glColor3fv(color)
        for vertex in quads:
            glVertex3fv(vertex)
    glEnd()
#sağ
def flaments_three(z:float, height:float):
    flaments = [
        ( (1.25,.125,z), (1.5,.125,z), (1.5,-.125,z), (1.25,-.125,z) ),

        ( (1.5,.125,z), (1.5,.125,z+height), (1.5,-.125,z+height), (1.5,-.125,z) ),
        ( (1.25,.125,z), (1.25,.125,z+height), (1.5,.125,z+height), (1.5,.125,z) ),
        ( (1.25,.125,z), (1.25,.125,z+height), (1.25,-.125,z+height), (1.25,-.125,z) ),
        ( (1.25,-.125,z), (1.25,-.125,z+height), (1.5,-.125,z+height), (1.5,-.125,z) ),

        ( (1.25,.125,z+height), (1.5,.125,z+height), (1.5,-.125,z+height), (1.25,-.125,z+height) ),
        ]
    colors = [
        (0,0.5,0.5),
       (0,0.5,0.5),(0,0.5,0.5),(0,0.5,0.5),(0,0.5,0.5), 
       (0,0.5,0.5)
    ]
    glBegin(GL_QUADS)  
    for quads, color in zip(flaments, colors):
        glColor3fv(color)
        for vertex in quads:
            glVertex3fv(vertex)
    glEnd()
#alt
def flaments_four(z:float, height:float):

    flaments = [
        ( (-.125,-1.25,z), (.125,-1.25,z), (.125,-1.5,z), (-.125,-1.5,z) ),

        ( (.125,-1.25,z), (.125,-1.25,z+height), (.125,-1.5,z+height), (.125,-1.5,z) ),
        ( (-.125,-1.25,z), (-.125,-1.25,z+height), (.125,-1.25,z+height), (.125,-1.25,z) ),
        ( (-.125,-1.25,z), (-.125,-1.25,z+height), (-.125,-1.5,z+height), (-.125,-1.5,z) ),
        ( (-.125,-1.5,z), (-.125,-1.5,z+height), (.125,-1.5,z+height), (.125,-1.5,z) ),

        ( (-.125,-1.25,z+height), (.125,-1.25,z+height), (.125,-1.5,z+height), (-.125,-1.5,z+height) ),
        ]
    colors = [
        (0,0.5,0.5),
       (0,0.5,0.5),(0,0.5,0.5),(0,0.5,0.5),(0,0.5,0.5), 
       (0,0.5,0.5)
    ]
    glBegin(GL_QUADS)  
    for quads, color in zip(flaments, colors):
        glColor3fv(color)
        for vertex in quads:
            glVertex3fv(vertex)
    glEnd()

def rectangle(z:float):
    flaments = [
        ((-1.5,1.5,z),(1.5,1.5,z),(1.5,-1.5,z),(-1.5,-1.5,z)), 

        ((-1.5,1.5,z),(-1.5,-1.5,z),(-1.5,-1.5,z+.5),(-1.5,1.5,z+.5)),

        ((-1.5,1.5,z),(1.5,1.5,z),(+1.5,1.5,z+.5),(-1.5,1.5,z+.5)),
        ((1.5,1.5,z),(1.5,-1.5,z),(1.5,-1.5,z+.5),(1.5,1.5,z+.5)),
        ((1.5,-1.5,z),(-1.5,-1.5,z),(-1.5,-1.5,z+.5),(1.5,-1.5,z+.5)),

        ((-1.5,1.5,z+.5),(1.5,1.5,z+.5),(1.5,-1.5,z+.5),(-1.5,-1.5,z+.5)),
        ]
    colors = [
        (0,0.7,0.7), 
        (0,0.5,0.7), (0,0.5,0.7), (0,0.5,0.7), (0,0.5,0.7), 
        (0,0.7,0.7)
    ]
    glBegin(GL_QUADS)  
    for quads, color in zip(flaments, colors):
        glColor3fv(color)
        for vertex in quads:
            glVertex3fv(vertex)
    glEnd()

def drawAxes():
        # eksenler
        glBegin(GL_LINES)

        glColor3f(1,0,0)
        glVertex3f(100,0,0)
        glVertex3f(-100,0,0)

        glColor3f(0,1,0)
        glVertex3f(0,100,0)
        glVertex3f(0,-100,0)

        glColor3f(0,0,1)
        glVertex3f(0,0,100)
        glVertex3f(0,0,-100)

        glEnd()

class App3D(OpenGLFrame):
    def initgl(self):
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)
        glClearColor(1,1,1,0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.width/self.height, 1, 100)
        glMatrixMode(GL_MODELVIEW)

        self.rotate = False
        self.x = 360
        self.y = 360 
        self.z = 360

    def rotate_X(self, x_degree:float):
        self.x = x_degree
        self.rotate = True

    def rotate_Y(self, y_degree:float):
        self.y = y_degree 
        self.rotate = True

    def rotate_Z(self, z_degree:float):
        self.z = z_degree
        self.rotate = True

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        glTranslate(0.0,0.0,-1.0);

        glScale(.25,.25,.25)

        boardTopCol = (0.8, 0.8, 0.8)
        boardsideCol = (0.4, 0.4, 0.4)
        
        HexTopCol = (0,0.7,0.7)
        HexSideCol = (0,0.5,0.7)

        if self.rotate:
            glRotatef(self.x,1,0,0)
            glRotatef(self.y,0,1,0)
            glRotatef(self.z,0,0,1)
        else:
            glRotatef(90,1,0,0)

        drawAxes()

        hexagone(-5,HexTopCol,HexSideCol)
        flaments_one(-4.5,2)
        flaments_two(-4.5,2)
        flaments_three(-4.5,2)
        flaments_four(-4.5,2)

        rectangle(-2.5) 
        flaments_one(-2,3)
        flaments_two(-2,3)
        flaments_three(-2,3)
        flaments_four(-2,3)

        hexagone(1,boardTopCol, boardsideCol)

        flaments_one(1.5,2)
        flaments_two(1.5,2)
        flaments_three(1.5,2)
        flaments_four(1.5,2)

        hexagone(3.5,HexTopCol,HexSideCol)

        glFlush()

def packetNumUpdate(packetText:Label, paketno:int):
    packetText.configure(text="GELEN PAKET ADEDİ: "+ str(paketno)) 

def timeLabelConfigure(timeLabel:Label, time:str):
    timeLabel.configure(text=time)


# SIRALAMA KONTROL EDİLECEK !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def storeCSV(datas:list):  
    headers = ["PAKETNUMARASI","UYDUSTATÜSÜ","HATAKODU", "GÖNDERMESAATİ", "BASINÇ1", "BASINÇ2", 
                   "YÜKSEKLİK1", "YÜKSEKLİK2", "İRTİFAFARKI", "İNİŞHIZI", "SICAKLIK", "PİLGERİLİMİ", 
                   "GPS1 LATITUDE", "GPS1 LONGITUDE", "GPS1 ALTITUDE",
                   "PITCH", "ROLL", "YAW","TAKIMNO"]


    # veriler için klasör oluştur
    if not  (os.path.exists("TELEMETRI VERILERI")): 
        dirName = "TELEMETRI VERILERI"
        os.makedirs(dirName)


    # veriler için csv oluştur
    if not (os.path.exists("TELEMETRI VERILERI/telemetri.csv")):
        datafile_csv = open("TELEMETRI VERILERI/telemetri.csv","x")
        datafile_csv.close()


    # verileri .csv içine yaz
    if (os.path.exists("TELEMETRI VERILERI/telemetri.csv")):
        w_datafile_csv = open("TELEMETRI VERILERI/telemetri.csv", "a", newline='')
        writer = csv.DictWriter(w_datafile_csv, fieldnames= headers )

        for data_packet in datas:
            csv_datas = {}
            i=0 
            for head in headers:
                csv_datas[head] = data_packet[i] 
                i += 1
            writer.writerow(csv_datas)

        w_datafile_csv.close()


old_datas = list()
all_datas = []
#all_datas.append([ 0 , 'GELISTIRME', '00000', '12/12/23,12/30', 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 145812])
x:int = 1
def StartListing( event:threading.Event, ser: serial.Serial, handler:HandleLine, text:Label, dottabFrame:Frame, alltabFrame:Frame, pureTeleLabel:Label, packetText:Label, graphes:list, aras_frames:list, statu_labels:list, map_:tkintermapview.TkinterMapView, timeLabel:Label, app:App3D  ):
    
    if event.is_set():
            return

    global x
    global old_datas
    global all_datas

    return_GetData = list()
    isData_Okey = bool()

    isData_Okey, return_GetData = GetData(ser, handler, text,pureTeleLabel)

    if isData_Okey:          
        datas = return_GetData.copy()
        # storeCSV(datas)
        
        WriteAllOfIt(datas, dottabFrame)
        #TeleTableListing(datas, alltabFrame) 
        StatuChange(datas[1], statu_labels)
        locationDataList = list[float] 
        locationDataList = [datas[12], datas[13]]
        Mapping(map_,  locationDataList )
        paketno = datas[0]
        packetNumUpdate(packetText, paketno)
        aras_values = datas[2]
        Aras(aras_frames, aras_values)
        GraphIt(graphes, x, datas, old_datas)
        x = x+1
        old_datas = datas.copy()
        timeLabelConfigure(timeLabel,  datas[3])
        app.rotate_X(datas[15]+90)
        app.rotate_Y(datas[16]) 
        app.rotate_Z(datas[17])

        all_datas.append(datas)
        datas = []

    else:
        if 0 != len(all_datas):
            datas = all_datas[-1].copy()

    text.after(700,StartListing,event, ser, handler, text, dottabFrame,alltabFrame,pureTeleLabel, packetText, graphes, aras_frames, statu_labels, map_, timeLabel, app)

def OpenCSV():
    path = os.getcwd()+ "/TELEMETRI VERILERI"
    os.startfile(path)




def leave(ser: serial.Serial):
    leavetext= b's'
    if (ser.isOpen() ):
        ser.write(leavetext)

def buzzer(ser: serial.Serial): 
    buzzertext= b'b'
    if (ser.isOpen() ):
        ser.write(buzzertext)

def kalibration(ser: serial.Serial): 
    buzzertext= b't'
    if (ser.isOpen() ):
        ser.write(buzzertext)



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import requests

global IP
IP = str()

def getIP(IPtext:Text):
     IPvalue = IPtext.get("1.0",END)
     global IP 
     IP = IPvalue

def videoTransConnect(event:threading.Event, label:Label): 

    if event.is_set():
            return

    global driver
    try:
        s = Service(r'C:/Users/Pc/Desktop/edgedriver_win64/msedgedriver')

        options_ = webdriver.EdgeOptions() 
        options_.add_argument("headless") 

        driver = webdriver.Edge(service=s, options=options_)

        global IP
        address = IP+"/upload"
        driver.get(address)

        label.configure(text="Bağlantı Kuruldu", bg="green")
        print("kuruldu")

    except:
        label.configure(text="Bağlantı Kurulamadı", bg="red")
        print("olmadı")

from tkinter import filedialog
global file_path
file_path:str
def videoTransPickFile(label:Label):
    global file_path
    file_path = filedialog.askopenfilename(initialdir= "C:/Users/Pc/Downloads",
                                            title= "Select File",
                                            filetypes= ( ("video files","*.mp4"),
                                                        ("all files","*.*") ) )  
     
    if file_path != None: 
        label["background"] = "green"
        label["foreground"] = "white"
        label.configure(text="Dosya Seçildi")

def videoTransSend(event:threading.Event, label:Label):
    if event.is_set():
            return
    global driver 
    global file_path
    try:
        # Dosya yükleme etiketine dosya yolu gönderme
        file_input =  driver.find_element(by=By.NAME, value="fupload")
        file_input.send_keys(file_path)

        # Yükleme düğmesine tıklama
        upload_button = driver.find_element(by=By.XPATH, value="/html/body/form/button")  
        upload_button.click()

        # Web sürücüsü kapatma
        driver.quit()
        print("video aktarımı başarılı")
        label.configure(text="Aktarım Başarılı", bg="green")
    except:
        label.configure(text="Aktarım Başarısız", bg="red")
    




global video_name 
video_name = str()

def openVideoFile(): 
    os.startfile(os.getcwd())

def openAsenkronWin():

    secondroot = Tk()
    secondroot.title(u"2.YER İSTASYONU-DOSYA İNDİR")
    secondroot.geometry("500x400")
    secondroot.configure(bg= dark_grey)

    frame = Frame(secondroot, bg= light_grey, width=450, height=350) 
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)


    conStatu_label = Label(frame, text=u"Bağlantı Durumu", width=30, font=("Helvetica",10))
    conStatu_label.grid(row=0, column=0, padx=10, pady=15 )

    fileName_text = Text(frame, width=25,height=1)
    fileName_text.insert(END, "dosya adını giriniz...")
    fileName_text.grid(row=1,column=0, padx=10, pady=20)

    okey_button = Button(frame, text="Tamam", width=30, command=lambda:GetFileName(fileName_text) )
    okey_button.grid(row=2, column=0, padx=(15,8), pady=10)


    t_video = threading.Thread(target= ConnectServer, args = (conStatu_label,))
    ConButton = Button(frame,text=u"Dosyayı İndir", width=30, command=lambda :t_video.start() )
    ConButton.grid(row=3, column=0, padx=8, pady=5)

    openButton = Button(frame,text=u"Dosya Konumunu Aç", width=30, command =openVideoFile )
    openButton.grid(row=4, column=0, padx=8, pady=5)
    
    secondroot.focus()
    secondroot.mainloop()
    # window.after(1, lambda: window.focus_force())

def GetFileName(name:Text):
     dosya = name.get("1.0",END)
     global video_name 
     video_name = dosya

def ConnectServer(label:Label):
    try:
        s = Service(r'C:/Users/Pc/Desktop/edgedriver_win64/msedgedriver')

        options_ = webdriver.EdgeOptions() 
        options_.add_argument("headless") 

        driver = webdriver.Edge(service=s, options=options_)
        label.configure(text="bağlantı kuruldu", bg="green", fg="white" )

        global video_name 
        dosya = video_name 
        #label.configure(text=dosya)

        url = "http://192.168.4.5/download" 

        params = {
                "download": dosya
            }
        response = requests.post(url, params=params) # response = requests.post(url, data=form_data)

        label.configure(text="response döndü", bg="green", fg="white"  )
        # Yanıtın içindeki dosyayı indir
        if 'Content-Disposition' in response.headers:
            file_name = response.headers['Content-Disposition'].split('filename=')[-1].strip('"')
            save_path= os.getcwd()+ "/asenkron" 
            completeName = os.path.join(save_path, file_name)
            with open(completeName, 'wb') as f:              
                label.configure(text="dosya alınıyor", bg="green", fg="white"  )
                f.write(response.content[response.content.find(b'\r\n\r\n')+4:]) # f.write(response.content)
                f.close()
                label.configure(text="dosya alındı", bg="green", fg="white"  )
    except:
        label.configure(text="işlem başarısız", bg="red", fg="white"  )






global cameraIndex
cameraIndex = int()
# bunu butona verip destroyu da ekleyebilirim
def getCameraID(camVariable:IntVar, camIndex:int):
    print( "get variable: " + str(camVariable.get()))   
    global cameraIndex
    if ( isinstance(cameraIndex, int) ):
        cameraIndex = camVariable.get() #camIndex-1
    

global capture_
global out_

global isStream
isStream = True

def startCamera(win:Tk, label:Label):

    win.destroy()

    global cameraIndex
    print("start: " + str(cameraIndex))
    capture = cv2.VideoCapture(1) 
    #capture = cv2.VideoCapture(cameraIndex) 
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('uzaykt-u23.mp4', fourcc, 20.0, (640, 480))
    global capture_
    global out_ 
    capture_ = capture
    out_ = out
    thread = threading.Thread(target=showFrames, args=(label, capture, out) )
    thread.start()

def SelectCamera(camera_label:Label):
    camSelectingWin = Tk()
    camSelectingWin.title("Kamera Cihazını Seç")
    camSelectingWin.geometry("300x300")
    camSelectingWin.configure(bg=dark_grey)
    
    camFrame = Frame( camSelectingWin, width=200, height=225, bg= light_grey )
    camFrame.pack(pady=10)
    camFrame.pack_propagate(False)

    graph = FilterGraph()
    
    camVariable = IntVar()
    camIndex=0
  
    for camera in graph.get_input_devices():
        Radiobutton(camFrame, text=camera, bg= light_grey, variable= camVariable, value=camIndex, 
                    command=lambda: getCameraID(camVariable, camIndex) ).pack(padx=10, pady=5)
        camIndex += 1

    closeButton = Button(camSelectingWin, text="Tamam", width=15, command=lambda: startCamera(camSelectingWin,camera_label ) )
    closeButton.pack(side=BOTTOM, pady=5)
    camSelectingWin.focus()

def showFrames(camera_label:Label, capture, out):
    global isStream
    if isStream:
        if capture.isOpened():
            # read the capture
            ret, frame = capture.read()

            # record
            out.write(frame)  

            # turned into image and display  
            cv2image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            img = PIL.Image.fromarray(cv2image)
            width, height = img.size 
            img = img.resize((int(width/2),int(height/2)))
            imgtk = ImageTk.PhotoImage(image = img) 
            camera_label.imgtk = imgtk
            camera_label.configure(image=imgtk,width=292,height=200)


    camera_label.after(10,showFrames, camera_label, capture, out)

def finishStream():
    global isStream
    global capture_
    global out_
    # quit
    #if not isStream: 
    isStream = False  
    capture_.release()
    out_.release()
    cv2.destroyAllWindows()
    return


def openCameraFile(): 
    os.startfile(os.getcwd())