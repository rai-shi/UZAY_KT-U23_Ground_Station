# saat için
#import time
#import matplotlib.animation as animation
#from mpl_toolkits.mplot3d import Axes3D
#from tkinter import messagebox

from tkinter import *
# graph için
import matplotlib.axes._subplots
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
# resimler için
from PIL import ImageTk
import PIL.Image
# battery
import psutil 
# yeni özellikleri için
from tkinter import ttk 
from tkinter.font import Font
# kamera görüntüsü
import cv2 
# map
import tkintermapview 
import os
import csv 
import serial
import ftplib
import threading
from tkinter import filedialog

from functions import *



#color
ktu_blue= "#1f5ba1"
light_grey = "#C6C7CA"
dark_grey= "#282A3A"



#margin options
general_margin_options = {'padx':5, 'pady':5}

# plt style
plt.style.use('bmh') # bmh

root = Tk()
root.title("UZAY KT-U23 643953")
root.geometry("1920x1080")
root.state('zoomed')
root.configure(bg=dark_grey)

# font style
font_button = Font(family = "Helvetica", size = 8)
font_label = Font(family = "Helvetica", size = 9)
font_big = Font(family = "Helvetica", size = 16)

#root.option_add("*TCombobox*Listbox*Font", font)


#global değişkenler
ser = serial.Serial()
handler = HandleLine()


# iconbitmap
root.iconphoto(True, ImageTk.PhotoImage(PIL.Image.open("logo.png")))

#TOP

TopFrame = Frame(root, width=1920, height=50, padx=0, pady=0, bg=dark_grey)
TopFrame.grid(row=0,column=0)
TopFrame.grid_propagate(False)

topFrame_margings= {'padx':5, 'pady':10}

DateTimeLabel = Label(TopFrame, text="00/00/2023,00/00/00", width=18, font=font_big, bg= dark_grey ,fg="white")
DateTimeLabel.grid(row=0,column=0,padx=(2,5),pady=10)

TeamNoLabel = Label(TopFrame, text="TAKIM NO: 643953", font= font_big,bg=dark_grey, fg="white" )
TeamNoLabel.grid(row=0,column=1,**topFrame_margings)

PacketLabel = Label(TopFrame,text="GELEN PAKET ADEDİ: 1000", width=24, font=font_big,bg=dark_grey,fg="white")
PacketLabel.grid(row=0,column=2,**topFrame_margings)

ArasFrame = Frame(TopFrame,bg=light_grey)
ArasFrame.grid(row=0,column=3,padx=20,pady=10)

aras_margins= {'padx':1, 'pady':1}

Aras_svelocity = Frame(ArasFrame, width=45,height=45,bg="red") # genel olarak model uydu hızı olabilir
Aras_svelocity.grid(row=0,column=0,**aras_margins)

Aras_cvelocity = Frame(ArasFrame, width=45,height=45,bg="red")
Aras_cvelocity.grid(row=0,column=1,**aras_margins)

Aras_cpressure = Frame(ArasFrame, width=45,height=45,bg="red")
Aras_cpressure.grid(row=0,column=2,**aras_margins) 

Aras_slocation = Frame(ArasFrame, width=45,height=45,bg="red")
Aras_slocation.grid(row=0,column=3,**aras_margins)

Aras_leaving = Frame(ArasFrame, width=45,height=45,bg="red")
Aras_leaving.grid(row=0,column=4,**aras_margins)

aras_frames = [Aras_svelocity, Aras_cvelocity, Aras_cpressure, Aras_slocation, Aras_leaving]

top_button_margins = {'padx':8, 'pady':2}

def t_buzzer(ser:serial.Serial):
   threading.Thread(target=buzzer, args=ser ).start()

BuzzerButton = Button(TopFrame, text="BUZZER", font=font_button, width=15, command= lambda:buzzer(ser) )
BuzzerButton.grid(row=0, column=4, **top_button_margins)

def t_leave(ser:serial.Serial):
   threading.Thread(target=leave, args=ser ).start()

LeaveButton = Button(TopFrame, text="AYRIL", font=font_button, width=15, command= lambda: leave(ser) )
LeaveButton.grid(row=0, column=5, **top_button_margins)

def t_kalibration(ser:serial.Serial):
   threading.Thread(target=kalibration, args=ser ).start()

Calibbutton = Button(TopFrame, text="T.KALİBRASYON", font=font_button, width=15, command= lambda: kalibration(ser) )
Calibbutton.grid(row=0, column=6, **top_button_margins)


batteryFrame = Frame(TopFrame,bg=dark_grey)
batteryFrame.grid(row=0,column=7,padx=(40,5), pady=10)



battery_label = Label(batteryFrame, 
                    text="",
                    width=5, 
                    font=font_big,
                    fg="white", bg=dark_grey ,anchor="w")
battery_label.grid(row=0, column=0, pady=5)

battery_progress_bar = ttk.Progressbar(batteryFrame,
                                    orient=HORIZONTAL,
                                    length=60, mode="determinate")
battery_progress_bar.grid(row=0, column=2, padx=3, pady=5)


#BOTTOM

bottomFrame = Frame(root, width=1920, height=1030, bg=dark_grey)
bottomFrame.grid(row=1,column=0)
bottomFrame.grid_propagate(False) 


#NARROW

narrowFrame = Frame(bottomFrame, width=225, height=1000, bg=dark_grey)
narrowFrame.grid(row=0,column=0, pady=1)
narrowFrame.grid_propagate(False) 

narrowFrame_margins = {'padx':3,'pady':2}
narrowFrame_options = {'border':3, 'width':220}
narrowFrame_text_options = {'anchor':'w', 'width':32 }

#LOGO
logo = ImageTk.PhotoImage(PIL.Image.open("logo.png").resize((95,95)))
logoLabel = Label( narrowFrame, image=logo, bg=dark_grey)
logoLabel.grid(row=0,column=0,padx=75)

#STATU FRAME
statuFrame = Frame(narrowFrame,**narrowFrame_options,height=171, bg=light_grey)
statuFrame.grid(row=1,column=0, **narrowFrame_margins)
statuFrame.grid_propagate(False) 

statuText1 = Label(statuFrame, text=u"Uçuşa Hazır", **narrowFrame_text_options, font=font_label, bg=light_grey) 
statuText1.grid(row=0,column=0,padx=4)

statuText2 = Label(statuFrame, text=u"Yükselme", **narrowFrame_text_options, font=font_label, bg=light_grey)
statuText2.grid(row=1,column=0,padx=4)

statuText3 = Label(statuFrame, text=u"Model Uydu İniş",**narrowFrame_text_options , font=font_label, bg=light_grey)
statuText3.grid(row=2,column=0,padx=4)

statuText4 = Label(statuFrame, text=u"Ayrılma",**narrowFrame_text_options, font=font_label, bg=light_grey)
statuText4.grid(row=3,column=0,padx=4)

statuText5 = Label(statuFrame, text=u"Görev Yükü İniş", **narrowFrame_text_options, font=font_label, bg=light_grey)
statuText5.grid(row=4,column=0,padx=4)

statuText6 = Label(statuFrame, text=u"Kurtarma Bekleniyor", **narrowFrame_text_options, font=font_label, bg=light_grey)
statuText6.grid(row=5,column=0,padx=4)

statuText7 = Label(statuFrame, text=u"Paket Video Alındı", **narrowFrame_text_options, font=font_label, bg=light_grey)
statuText7.grid(row=6,column=0,padx=4)

statuText8 = Label(statuFrame, text=u"Paket Video Gönderildi", **narrowFrame_text_options, font=font_label, bg=light_grey)
statuText8.grid(row=7,column=0,padx=4)

statu_labels = [statuText1,statuText2,statuText3,statuText4,statuText5,statuText6,statuText7, statuText8]

# ---------------------------------------------------------------------------------------------------------------------------

# base frame
videoTransferFrame = Frame(narrowFrame,**narrowFrame_options,height=195, bg=light_grey)
videoTransferFrame.grid(row=3,column=0, **narrowFrame_margins) 
videoTransferFrame.grid_propagate(False)

# video transfer statu frame
videoTransStatuFrame = Frame(videoTransferFrame) 
videoTransStatuFrame.grid(row=0,column=0, padx=4,pady=4)
videoTransStatuFrame.grid_propagate(False)

videoTransStatu = Label(videoTransStatuFrame, text="BAĞLANTI SAĞLAYIN", anchor='center', width=28 , font=font_label, bg="red", fg="white"  )
videoTransStatu.pack()

# IP Text Frame
videoTransIPtextFrame = Frame(videoTransferFrame, bg=light_grey)
videoTransIPtextFrame.grid(row=1,column=0, padx=4,pady=4)

videoTransIPlabel = Label(videoTransIPtextFrame, text="IP: ", width=3, anchor="w", font= font_label, bg=light_grey)
videoTransIPlabel.grid(row=0,column=0, padx=(5,1))

videoTransIPtext = Text(videoTransIPtextFrame, width=18,height=1)
videoTransIPtext.insert(END, "http://192.168.4.5")
videoTransIPtext.grid(row=0,column=1)

# Button Frame
videoTransButtonFrame = Frame(videoTransferFrame, bg=light_grey)
videoTransButtonFrame.grid(row=2,column=0, padx=4,pady=4)

getIPButton = Button(videoTransButtonFrame, text="Tamam", font=font_button, width=25, command=lambda:getIP(videoTransIPtext) )
getIPButton.grid(row=0,column=0, padx=2, pady=3)


global t_videoTransConnect
def create_t_videoTransConnect():
    global t_videoTransConnect
    t_videoTransConnect = threadFactory(target_=videoTransConnect, args_=(videoTransStatu,)) 
    t_videoTransConnect.create()
    t_videoTransConnect.start()

videoTransConnectButton = Button(videoTransButtonFrame, text="Bağlan", font=font_button, width=25, command=create_t_videoTransConnect ) 
videoTransConnectButton.grid(row=1,column=0, padx=2, pady=3)

videoTransPickFileButton = Button(videoTransButtonFrame, text="Dosya Seç" ,font=font_button, width=25,command=lambda: videoTransPickFile(videoTransStatu))
videoTransPickFileButton.grid(row=2,column=0, padx=2, pady=3)

global t_videoTransSend
def create_t_videoTransSend():
    global t_videoTransSend
    t_videoTransSend = threadFactory(target_=videoTransSend, args_=(videoTransStatu,)) 
    t_videoTransSend.create()
    t_videoTransSend.start()

videoTransSendButton = Button(videoTransButtonFrame, text="Dosyayı Gönder", font=font_button, width=25, command=create_t_videoTransSend )  
videoTransSendButton.grid(row=3,column=0, padx=2, pady=(3,0))

# ---------------------------------------------------------------------------------------------------------------------------


AsekronButtonFrame = Frame(narrowFrame,**narrowFrame_options,height=30, bg=light_grey)
AsekronButtonFrame.grid(row=4,column=0, **narrowFrame_margins)
AsekronButtonFrame.grid_propagate(False)

AsenkronButton = Button(AsekronButtonFrame, text="Asenkron Video Alımı", font=font_button, width=32, command=openAsenkronWin)
AsenkronButton.place(relx=.5, rely=.5,anchor= CENTER)




#EXTENSIVE

extensiveFrame = Frame(bottomFrame, width=1305, height=1000, bg=dark_grey)
extensiveFrame.grid(row=0,column=1)
extensiveFrame.grid_propagate(False)

extensiveFrame_margins = {'padx':3,'pady':3}
extensiveFrame_options = {'border':3, 'width':240}
extensiveFrame_text_options = {'anchor':'w', 'width':32 } 

#EXTENSIVE TOP
extensiveTopFrame = Frame(extensiveFrame, width=1305, height=500, bg=dark_grey)
extensiveTopFrame.grid(row=0,column=0)
extensiveTopFrame.grid_propagate(False)

#EXTENSIVE TOP LEFT

extensiveTopLeftFrame = Frame(extensiveTopFrame, width=300, height=500, bg=dark_grey)
extensiveTopLeftFrame.grid(row=0,column=0)



cameraFrame = Frame(extensiveTopLeftFrame, width=295, height=245, bg=light_grey)
cameraFrame.grid(row=0,column=0, **extensiveFrame_margins)
cameraFrame.grid_propagate(False)

camera_label = Label(cameraFrame,width=42,height=13, bg = light_grey)
camera_label.grid(row=0,column=0, pady=2)


capture = cv2.VideoCapture(1) 
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('uzaykt-u23.mp4', fourcc, 20.0, (640, 480))


cameraButtonFrame = Frame(cameraFrame, bg= light_grey) 
cameraButtonFrame.grid(row=1,column=0,padx=2, pady=2)


cameraConnectButton = Button(cameraButtonFrame, text=u"Kameraya Bağlan", width=14, command = lambda : SelectCamera(camera_label) )
cameraConnectButton.grid(row=0,column=0,padx=2)

cameraStopButton = Button(cameraButtonFrame, text=u"Kaydı Bitir",width=12, command= finishStream)
cameraStopButton.grid(row=0,column=1,padx=2)

openCameraFileButton = Button(cameraButtonFrame, text=u"Dosyayı Aç", width= 12, command = openCameraFile)
openCameraFileButton.grid(row=0,column=2,padx=2)




MapFrame = Frame(extensiveTopLeftFrame, bg=light_grey)
MapFrame.grid(row=1,column=0, **extensiveFrame_margins)
MapFrame.grid_propagate(False)

yukMap = tkintermapview.TkinterMapView(MapFrame, corner_radius=0, width=295, height=250)
yukMap.pack(fill="both", expand = 1)
yukMap.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
yukMap.set_position(40.99300733397944, 39.77555646086991, marker=True) # (40.998066,39.763824) 40.99300733397944, 39.77555646086991
# yukMap.set_zoom(10)


#EXTENSIVE GRAPH SIDE
GraphCanvas = Canvas(extensiveTopFrame, width=1005, height=500, bg=dark_grey)
GraphCanvas.grid(row=0,column=1,**extensiveFrame_margins)
GraphCanvas.grid_propagate(False)

figSize_options =(2.50,2.45)
graph_margins = { 'pady':2 }

font = {'size'   : 6}
matplotlib.rc('font', **font)

#basınç 1
fig_plot1= Figure(figsize=(figSize_options), dpi=100)
plot1= fig_plot1.add_subplot(111) # matplotlib.axes._subplots.AxesSubplot
plot1.set_title(u'Görev Yükü Basıncı (hPa)',fontsize=12)
plot1.autoscale()
plot1.ticklabel_format(useOffset=False)
plot1Canvas = FigureCanvasTkAgg(fig_plot1, master=GraphCanvas)
plot1Canvas.get_tk_widget().grid(row=0,column=0,**graph_margins)
plot1Canvas.draw()

#basınç 2
fig_plot2= Figure(figsize=(figSize_options), dpi=100)
plot2= fig_plot2.add_subplot(111)
plot2.set_title(u'Taşıyıcı Basıncı (hPa)',fontsize=12)
plot2.autoscale()
plot2.ticklabel_format(useOffset=False)
plot2Canvas = FigureCanvasTkAgg(fig_plot2, master=GraphCanvas)
plot2Canvas.get_tk_widget().grid(row=1,column=0,**graph_margins)
plot2Canvas.draw()

#yükseklik 1
fig_plot3= Figure(figsize=(figSize_options), dpi=100)
plot3= fig_plot3.add_subplot(111)
plot3.set_title(u'Görev Yükü Yüksekliği (m)',fontsize=12)
plot3.autoscale()
plot3.ticklabel_format(useOffset=False)
plot3Canvas = FigureCanvasTkAgg(fig_plot3, master=GraphCanvas)
plot3Canvas.get_tk_widget().grid(row=0,column=1,**graph_margins)
plot3Canvas.draw()

#yükseklik 2
fig_plot4= Figure(figsize=figSize_options, dpi=100)
plot4= fig_plot4.add_subplot(111)
plot4.set_title(u'Taşıyıcı Yüksekliği (m)',fontsize=12)
plot4.autoscale()
plot4.ticklabel_format(useOffset=False)
plot4Canvas = FigureCanvasTkAgg(fig_plot4, master=GraphCanvas)
plot4Canvas.get_tk_widget().grid(row=1,column=1, **graph_margins)
plot4Canvas.draw()

#irtifa farkı
fig_plot5= Figure(figsize=figSize_options, dpi=100)
plot5= fig_plot5.add_subplot(111)
plot5.set_title('İrtifa Farkı (m)',fontsize=12)
plot5.autoscale()
plot5.ticklabel_format(useOffset=False)
plot5Canvas = FigureCanvasTkAgg(fig_plot5, master=GraphCanvas)
plot5Canvas.get_tk_widget().grid(row=0,column=2, **graph_margins)
plot5Canvas.draw()

#sıcaklık
fig_plot6= Figure(figsize=figSize_options, dpi=100)
plot6= fig_plot6.add_subplot(111)
plot6.set_title(u'Sıcaklık (°C)',fontsize=12)
plot6.autoscale()
plot6.ticklabel_format(useOffset=False)
plot6Canvas = FigureCanvasTkAgg(fig_plot6, master=GraphCanvas)
plot6Canvas.get_tk_widget().grid(row=1,column=2, **graph_margins)
plot6Canvas.draw()

#pil
fig_plot7= Figure(figsize=(figSize_options), dpi=100)
plot7= fig_plot7.add_subplot(111)
plot7.set_title('Pil Gerilimi (V)',fontsize=12)
plot7.autoscale()
plot7.ticklabel_format(useOffset=False)
plot7Canvas = FigureCanvasTkAgg(fig_plot7, master=GraphCanvas)
plot7Canvas.get_tk_widget().grid(row=0,column=3, **graph_margins)
plot7Canvas.draw()

#hız
fig_plot8= Figure(figsize=(figSize_options), dpi=100)
plot8= fig_plot8.add_subplot(111)
plot8.set_title(u'İniş Hızı (m/sn)',fontsize=12)
plot8.autoscale()
plot8.ticklabel_format(useOffset=False)
plot8Canvas = FigureCanvasTkAgg(fig_plot8, master=GraphCanvas)
plot8Canvas.get_tk_widget().grid(row=1,column=3, **graph_margins)
plot8Canvas.draw()

paramForGraphes = [
    { 'plot':plot1,
       'yindex':4,
        'canvas':plot1Canvas
        },
    { 'plot':plot2,
       'yindex':5,
        'canvas':plot2Canvas
        },
    { 'plot':plot3,
       'yindex':6,
        'canvas':plot3Canvas
        },
    { 'plot':plot4,
       'yindex':7,
        'canvas':plot4Canvas
        },
    { 'plot':plot5,
       'yindex':8,
        'canvas':plot5Canvas
        },
    { 'plot':plot6,
       'yindex':10,
        'canvas':plot6Canvas
        },
    { 'plot':plot7,
       'yindex':11,
        'canvas': plot7Canvas
        },
    { 'plot':plot8,
       'yindex':9,
        'canvas':plot8Canvas
        }
    ]

#EXTENSIVE BOTTOM
extensiveBottomFrame = Frame(extensiveFrame, width=1305, height=250, bg=dark_grey)
extensiveBottomFrame.grid(row=1,column=0)
extensiveBottomFrame.grid_propagate(False)

# 3D ANIMATION
AnimationFrame = Frame(extensiveBottomFrame, width=300, height=235, bg=light_grey)
AnimationFrame.grid(row=0,column=0,**extensiveFrame_margins) 

anim3d = App3D(AnimationFrame, width=295, height=235)
anim3d.pack(fill=BOTH, expand=YES)
anim3d.animate = 900


# creating tab notebook
telemetryDisplay = ttk.Notebook(extensiveBottomFrame, width=1025, height=210)
telemetryDisplay.grid(row=0,column=1,**extensiveFrame_margins)
telemetryDisplay.grid_propagate(False)

# creating dot telemetry tab
dotTelemetryTabFrame = Frame(telemetryDisplay, bg=light_grey)
dotTelemetryTabFrame.pack(fill="both", expand = 1)

# creating alltelemetry tab
allTelemetryTabFrame = Frame(telemetryDisplay,bg= light_grey)
allTelemetryTabFrame.pack(fill="both", expand = 1)

pureTelemetryTabFrame = Frame(telemetryDisplay,bg= light_grey)
pureTelemetryTabFrame.pack(fill="both", expand = 1)

telemetryDisplay.add(dotTelemetryTabFrame, text= u"Anlık Telemetri")
telemetryDisplay.add(allTelemetryTabFrame, text= u"Hepsini Göster")
telemetryDisplay.add(pureTelemetryTabFrame, text= u"Serial Gösterimi")


# 19 veri
# dot telemetry tab context
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
        # teleTitle[data] = teleTitle[data].encode('UTF-8')
        textData = Label(dotTelemetryTabFrame, anchor = "w",width= 32, font=font_label, text= (teleTitle[dataIndex]+ units[dataIndex]) , bg=light_grey)
        textData.grid(row=rw, column=col, padx=4, pady=10)
        dataIndex = dataIndex + 1 




# all telemetry tab context

# creating canvas for scrollbar 
allTelemetryCanvas = Canvas(allTelemetryTabFrame, bg=light_grey)
allTelemetryCanvas.pack(side="left", fill="both", expand=True)

# creating frame for content
allTelemetry = Frame(allTelemetryCanvas, bg= light_grey )
# allTelemetry.pack(fill="both", expand = 1)
allTelemetryCanvas.create_window((0, 0), window=allTelemetry, anchor="nw")

allTelemetry.bind(
    "<Configure>",
    lambda e: allTelemetryCanvas.configure(
        scrollregion=allTelemetryCanvas.bbox("all") ) )

def OnMouseWheel(event):
    scrollbar.yview("scroll",event.delta,"units")
    return "break"


tableTeleTitle = [" ","Paketno","Durum","ARAS", "Saat",
        "1Basınç","2Basınç",
        "1Yükseklik","2Yükseklik",
        "İrtifaFarkı","İnişHızı",
        "Sıcaklık",
        "PilGerilimi",
        "La1","Long1","Al1",
        "Pitch","Roll","Yaw",
        "Takım No"]

# başlığın başında bir boşluk
empty = Label(allTelemetry, text=" ", bg= light_grey, width=2)
empty.grid(row=0,column=0,padx=2, pady=0.5)

# başlıklar
for j in range(1,20):
    entry = Label(allTelemetry,text=tableTeleTitle[j], font=("Helvetica",8),bg= light_grey, anchor='w', width=7, bd=2)
    entry.grid(row=0, column=j,padx=2, pady=0.5)

scrollbar1 = ttk.Scrollbar(allTelemetryTabFrame, orient='vertical', command=allTelemetryCanvas.yview)

allTelemetryTabFrame.bind("<MouseWheel>", OnMouseWheel) 
# scrollbar.focus_set()

scrollbar1.pack(side=RIGHT, fill="y")
allTelemetryCanvas.configure(yscrollcommand=scrollbar1.set)



# pure telemetry tab context

pureTelemetryLabel = Label(pureTelemetryTabFrame, text="serial data", anchor='center', width=130 , font=font_label, bg=light_grey )  
pureTelemetryLabel.place(relx=.5, rely=.5,anchor= CENTER)


#SERIAL CONNECTION
SerialConFrame = Frame(narrowFrame,**narrowFrame_options,height=224, bg=light_grey)
SerialConFrame.grid(row=2,column=0, **narrowFrame_margins)
SerialConFrame.grid_propagate(False)


SerialConTextFrame = Frame(SerialConFrame)
SerialConTextFrame.grid(row=0,column=0, padx=4,pady=5)
SerialConTextFrame.grid_propagate(False)

SerialConText = Label(SerialConTextFrame, text="BAĞLANTI SAĞLAYIN", anchor='center', width=28 , font=font_label, bg="red", fg="white"  )
SerialConText.pack()


SerialConComboFrame = Frame(SerialConFrame, bg=light_grey) 
SerialConComboFrame.grid(row=1,column=0, padx=4,pady=5)

import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
port_list = []
for port in ports:
    port_list.append(port.device)
            

SerialConComboText1 = Label(SerialConComboFrame, text="COM Port: ", width=10, anchor="w", font= font_label, bg=light_grey, fg="black" )
SerialConComboText1.grid(row=0,column=0, padx=5,pady=2) 

portList =port_list # ["COM3", "COM5", "COM8","COM7", "COM4","COM6"]
port = StringVar()
portCombo = ttk.Combobox(SerialConComboFrame, textvariable=port, font= font_label, values = portList, width=10, height=4)
portCombo.set("port seçin") 
portCombo.grid(row=0,column=1, padx=5,pady=2)

SerialConComboText2 = Label(SerialConComboFrame, text="HIZ: ", width=10, anchor="w", font= font_label, bg=light_grey, fg="black" )
SerialConComboText2.grid(row=1,column=0, padx=5,pady=2) 

speedList = [ "115200", "921600", "19200","157600", "74880"]
speed = StringVar()
speedCombo = ttk.Combobox(SerialConComboFrame, textvariable=speed, font= font_label, values = speedList, width=10, height=4)
speedCombo.set("hız seçin") 
speedCombo.grid(row=1,column=1, padx=5,pady=2) 

# global değişkenler
TeleDatas=list()
old_datas = list()



SerialConButtonFrame = Frame(SerialConFrame, bg=light_grey)
SerialConButtonFrame.grid(row=2,column=0 ,pady=5)


getConInfoButton = Button(SerialConButtonFrame, text="Tamam", font=font_button, width=32, command=lambda: getConnectInfo(portCombo, speedCombo) )                        
getConInfoButton.grid(row=0,column=0, padx=2, pady=2)

ButtonInnerFrame = Frame(SerialConButtonFrame, bg=light_grey) 
ButtonInnerFrame.grid(row=1,column=0, padx=2, pady=2)


global t_port
def create_t_port():
    global t_port
    t_port = threadFactory(target_=PortConnect, args_=(ser, handler, SerialConText) ) 
    t_port.create()
    t_port.start()


#t_port = threading.Thread ( target= PortConnect, args=(ser, handler, SerialConText) )
PortConnectButton = Button(ButtonInnerFrame, text="Bağlantı Kur", font=font_button, width=15, 
                           command = create_t_port )
PortConnectButton.grid(row=0,column=0, padx=2, pady=2)

global thread_StartListing
def create_thread_StartListing():
    global thread_StartListing
    thread_StartListing = threadFactory(target_=StartListing, args_=( ser, handler, SerialConText, dotTelemetryTabFrame, allTelemetry,pureTelemetryLabel, PacketLabel, paramForGraphes, aras_frames, statu_labels, yukMap, DateTimeLabel, anim3d )) 
    thread_StartListing.create()
    thread_StartListing.start()

#def thread_start():
#    thread_StartListing = threading.Thread(target= StartListing,  args=( ser, handler, SerialConText, dotTelemetryTabFrame, allTelemetry,pureTelemetryLabel, PacketLabel, paramForGraphes, aras_frames, statu_labels, yukMap, DateTimeLabel, anim3d ) )
#    thread_StartListing.start()

StartTelemetryButton = Button(ButtonInnerFrame, text="Listelemeye Başla", font=font_button, width=15, command= create_thread_StartListing )
StartTelemetryButton.grid(row=0,column=1, padx=2)


def finishListing(event:threading.Event):
    if event.is_set():
        return
    thread_StartListing.finish()
    #ser.setBreak(True)
    #time.sleep(0.2)
    #ser.sendBreak(duration = 0.02)
    #time.sleep(0.2)

    storeCSV(all_datas)
    ser.close()
    t_port.finish()

global thread_FinishListing
def create_thread_FinishListing():
    global thread_FinishListing
    thread_FinishListing = threadFactory(target_=finishListing)
    thread_FinishListing.create()
    thread_FinishListing.start()
    

StopTelemetryButton = Button(ButtonInnerFrame, text="Listelemeyi Durdur", font=font_button, width=15, command= create_thread_FinishListing )
StopTelemetryButton.grid(row=1,column=0, padx=2, pady=2)


OpenTeleFolderButton = Button(ButtonInnerFrame, text="CSV Konumunu Aç", font=font_button, width=15, command= OpenCSV)
OpenTeleFolderButton.grid(row=1,column=1, padx=2, pady=2)

CleanButton = Button(SerialConButtonFrame, text="Verileri Temizle", font=font_button, width=32)
CleanButton.grid(row=2,column=0, padx=2, pady=2)


#--------------------------------------------------------------------------------------------------------
#belki içlerine argüman olarak verilerek başka bir dosyada yine yazılırlardı.


def battery():
    battery_info = psutil.sensors_battery
    global percent
    percent = battery_info().percent
    battery_label.config(text="%" + str(percent))

    battery_label.after(600000,battery)


def battery_progress(): 
    global percent
    battery_progress_bar['value'] = percent
    battery_progress_bar.after(600000,battery_progress)



if __name__== "__main__":

    # dosyayı temizleme
    if (os.path.exists("TELEMETRI VERILERI/telemetri.csv")):

        datafile_csv = open("TELEMETRI VERILERI/telemetri.csv", "a", newline='')
        datafile_csv.seek(0)
        datafile_csv.truncate(0)

        headers = ["PAKETNUMARASI","UYDUSTATÜSÜ","HATAKODU", "GÖNDERMESAATİ", "BASINÇ1", "BASINÇ2", 
                   "YÜKSEKLİK1", "YÜKSEKLİK2", "İRTİFAFARKI", "İNİŞHIZI", "SICAKLIK", "PİLGERİLİMİ", 
                   "GPS1 LATITUDE", "GPS1 LONGITUDE", "GPS1 ALTITUDE",
                   "PITCH", "ROLL", "YAW","TAKIMNO"]
        headerWriter = csv.DictWriter(datafile_csv, fieldnames= headers )
        headerWriter.writeheader()
        datafile_csv.close()


    battery()
    battery_progress()

    root.mainloop()
