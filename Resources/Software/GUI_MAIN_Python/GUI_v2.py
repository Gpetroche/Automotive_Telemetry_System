import os
import customtkinter
from PIL import Image
import time
import csv


##Librerias para el gráfico en tiempo real:
from math import sin
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from numpy import *
import random
from itertools import count
import pandas as pd
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure

##Librerias relacionadas con comunicación Serial:
import serial
import serial.tools.list_ports


# Window configuration
customtkinter.set_appearance_mode("dark")
app = customtkinter.CTk()
app.title("                                                                                                  GUI Telemetry System designed by Gerardo A. Petroche")
app.geometry("950x600")
app.resizable(False,False)
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "E:\TFG\SOFTWARE\GUI\OLD\GUI_Python")
RPM = "0"
SPEED = "0"
COOLANT_TEMPERATURE = "0"
GEAR_ENGAGED = "0"    
Array_Data=[RPM, SPEED, COOLANT_TEMPERATURE, GEAR_ENGAGED]
global cond 

#Serial communication variables
port_list = []
global flag_debug 
global selected_serial_communication
global serial_communication

#Telemetry data variables
global battery_voltage_value
global oil_pressure_value
global neutral_gear_value
global tachometer_value 
global speedometer_value 
global fuel_value 

global data_matrix
data_matrix = []
global lines
global writer

###### FUNCTIONS
def GoToSelectionWindow():
    app.welcome_title.place_forget()  # remove login frame
    app.welcome_subtitle.place_forget()
    app.welcome_start_button.place_forget()
    app.welcome_data.place_forget()
    selection_window(app)

def FromSelectionWindowToStartWindow():
    app.main_label.place_forget()
    app.back_button.place_forget()

    app.frame_demo_mode.place_forget()
    app.button_demo_mode.place_forget()
    app.bg_frame_demo_mode.place_forget()
    
    app.frame_telemetry_mode.place_forget()
    app.button_telemetry_mode.place_forget()
    app.bg_frame_telemetry_mode.place_forget()

    app.optionmenu_data_1.place_forget()
    app.optionmenu_data_2.place_forget()
    app.optionmenu_data_3.place_forget()
    app.frame_data_1.place_forget()
    app.frame_data_2.place_forget()
    app.frame_data_3.place_forget()
    app.canvas.place_forget()
    app.canvas.place_forget()
    app.canvas.place_forget()
    app.start_button.place_forget()
    app.stop_button.place_forget()
    start_window(app)

def FromSelectionWindowToDemoMode():
    app.main_label.place_forget()
    app.back_button.place_forget()

    app.frame_demo_mode.place_forget()
    app.button_demo_mode.place_forget()
    app.bg_frame_demo_mode.place_forget()
    
    app.frame_telemetry_mode.place_forget()
    app.button_telemetry_mode.place_forget()
    app.bg_frame_telemetry_mode.place_forget()
    demo_mode(app)

def FromSelectionWindowToTelemetryMode():
    app.main_label.place_forget()
    app.back_button.place_forget()

    app.frame_demo_mode.place_forget()
    app.button_demo_mode.place_forget()
    app.bg_frame_demo_mode.place_forget()
    
    app.frame_telemetry_mode.place_forget()
    app.button_telemetry_mode.place_forget()
    app.bg_frame_telemetry_mode.place_forget()
    telemetry_mode(app)




def start_window(app):
    #### WIDGETS:
    app.welcome_title = customtkinter.CTkLabel(master=app,
                                            text="Graphical User Interface for an\n Automotive Adquisition and Telemetry System",
                                            font=customtkinter.CTkFont(size=40, weight="bold"),
                                            text_color="White")

    app.welcome_subtitle = customtkinter.CTkLabel(master=app,
                                                text="Designed by Gerardo A. Petroche",
                                                font = customtkinter.CTkFont(size=12, slant="italic"),
                                                text_color="#717171")

    app.welcome_start_button = customtkinter.CTkButton(master=app,
                                                        text="START",
                                                        command=GoToSelectionWindow,
                                                        width=300,
                                                        height=50,
                                                        fg_color="#C70039",
                                                        hover_color="#7A0023",
                                                        border_width=2,
                                                        border_color="black")
    

    app.welcome_data = customtkinter.CTkLabel(master=app,
                                                text="\t\t\t\tCourse 2022-2023\n\t\t                      Automotive Engineering Degree\n\t       Universitat de Vic - Universitat Central de Catalunya",
                                                font=customtkinter.CTkFont(size=10),
                                                text_color="#900C3F")
    

    ###### PLACEs
    app.welcome_title.place(x=50, y=150)
    app.welcome_subtitle.place(x=400, y=270)
    app.welcome_start_button.place(x=350, y=400)
    app.welcome_data.place(x=660, y=550)

def selection_window(app):
    ########## WIDGETS ########### 
    app.frame_demo_mode = customtkinter.CTkFrame(master=app,
                                                width= 400,
                                                height=300,
                                                corner_radius=10,
                                                fg_color="#626567")
    
    app.main_label = customtkinter.CTkLabel(master=app,
                                                 text="MAIN MENU - SELECT YOUR MODE",
                                                 font=customtkinter.CTkFont(size=30, weight="bold"),
                                                 text_color="White")

    app.back_button = customtkinter.CTkButton(master=app,
                                                  text="Back",
                                                  command=FromSelectionWindowToStartWindow,
                                                  width=200,
                                                  fg_color="#C70039",
                                                  hover_color="#7A0023",
                                                  border_width=2,
                                                  border_color="black")

    app.bg_frame_demo_mode = customtkinter.CTkFrame(master=app,
                                                width= 400,
                                                height=300,
                                                corner_radius=10,
                                                fg_color="#626567")

    app.button_demo_mode = customtkinter.CTkButton(master=app,
                                                    text="DEMO MODE",
                                                    command=FromSelectionWindowToDemoMode,
                                                    width=350, height=40, fg_color="#2980B9",
                                                    hover_color="#1F618D",
                                                    border_width=1,
                                                    border_color="black")

    app.image_demo_mode = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "velocimetro_imagen.png")),
                                                    dark_image=Image.open(os.path.join(image_path, "velocimetro_imagen.png")),
                                                    size=(225,225))
    app.frame_demo_mode = customtkinter.CTkLabel(master=app,
                                                height=225,
                                                width=225,
                                                image=app.image_demo_mode,
                                                bg_color="#626567",
                                                text="")

    app.bg_frame_telemetry_mode = customtkinter.CTkFrame(master=app,
                                                        width= 400,
                                                        height=300,
                                                        corner_radius=10,
                                                        fg_color="#626567")

    app.button_telemetry_mode = customtkinter.CTkButton(master=app,
                                                            text="TELEMETRY MODE",
                                                            command=FromSelectionWindowToTelemetryMode,
                                                            width=350,
                                                            height=40,
                                                            fg_color="#16A085",
                                                            hover_color="#117A65",
                                                            border_width=1,
                                                            border_color="black")

    app.image_telemetry_mode = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "telemetria_imagen.png")),
                                                    dark_image=Image.open(os.path.join(image_path, "telemetria_imagen.png")),
                                                    size=(225,225))
    app.frame_telemetry_mode = customtkinter.CTkLabel(master=app,
                                                        height=225,
                                                        width=225,
                                                        image=app.image_telemetry_mode,
                                                        bg_color="#626567",
                                                        text="")
    


    ########### PLACEs ###########
    app.main_label.place(x=250,y=20)
    app.back_button.place(x=20, y=550)

    app.frame_demo_mode.place(x=140, y=135)
    app.button_demo_mode.place(x=75, y=375)
    app.bg_frame_demo_mode.place(x=50, y=125)

    app.frame_telemetry_mode.place(x=600, y=135)
    app.button_telemetry_mode.place(x=525, y=375)
    app.bg_frame_telemetry_mode.place(x=500, y=125)

def demo_mode(app):
    global cond
    cond = False
    ########## WIDGETS ########### 
    app.back_button = customtkinter.CTkButton(master=app,
                                                text="Back",
                                                command=FromSelectionWindowToStartWindow,
                                                width=200,
                                                height=45,
                                                fg_color="#C70039",
                                                hover_color="#7A0023",
                                                border_width=2,
                                                border_color="black")

    app.frame_data_1 = customtkinter.CTkFrame(master=app,
                                            width= 930,
                                            height=175,
                                            corner_radius=5,
                                            fg_color="#626567")

    app.optionmenu_data_1 = customtkinter.CTkOptionMenu(master=app,
                                                        height=10,
                                                        width=120,
                                                        dynamic_resizing= True,
                                                        values=Array_Data)
    
    app.labeloptionmenu_1 = customtkinter.CTkLabel(master=app,
                                                   text= "CHANNEL 1:")

    app.frame_data_2 = customtkinter.CTkFrame(master=app,
                                        width= 930,
                                        height=175,
                                        corner_radius=5,
                                        fg_color="#626567")

    app.optionmenu_data_2 = customtkinter.CTkOptionMenu(master=app,
                                                        height=10,
                                                        width=120,
                                                        dynamic_resizing= True,
                                                        values=Array_Data)
    
    app.labeloptionmenu_2 = customtkinter.CTkLabel(master=app,
                                                   text= "CHANNEL 2:")

    app.frame_data_3 = customtkinter.CTkFrame(master=app,
                                            width= 930,
                                            height=175,
                                            corner_radius=5,
                                            fg_color="#626567")

    app.optionmenu_data_3 = customtkinter.CTkOptionMenu(master=app,
                                                        height=10,
                                                        width=120,
                                                        dynamic_resizing= True,
                                                        values=Array_Data)
    
    app.labeloptionmenu_3 = customtkinter.CTkLabel(master=app,
                                                   text= "CHANNEL 3:")
    
    app.start_button = customtkinter. CTkButton(master=app,
                                                height=45,
                                                width=125,
                                                text= "Start",
                                                fg_color="#626567",
                                                hover_color="#00FF00",
                                                command=StartDemo)
    
    app.stop_button = customtkinter. CTkButton(master=app,
                                                height=45,
                                                width=125,
                                                text= "Stop",
                                                fg_color="#626567",
                                                hover_color="#FF0000",
                                                command=StopDemo)

    plot_object1()
    plot_object2()
    plot_object3()


    ########### PLACEs ###########
    app.back_button.place(x=20, y=550)
    app.frame_data_1.place(x=10, y=10)
    app.optionmenu_data_1.place(x=250, y=575)
    app.labeloptionmenu_1.place(x= 275, y=545)
    app.frame_data_2.place(x=10, y=190)
    app.optionmenu_data_2.place(x=400, y=575)
    app.labeloptionmenu_2.place(x=425, y=545)
    app.frame_data_3.place(x=10, y=370)
    app.optionmenu_data_3.place(x=550, y=575)
    app.labeloptionmenu_3.place(x=575, y=545)
    app.start_button.place(x=685, y=550)
    app.stop_button.place(x=815, y=550)

def StartDemo():
    global cond
    cond = True

def StopDemo():
    global cond
    cond = False


def start_serial_communication():
    global selected_serial_communication
    global serial_communication

    selected_serial_communication = app.optionmenu_serial_port.get()
    serial_communication = serial.Serial(selected_serial_communication, 115200)
    time.sleep(0.5)
    if(serial_communication.is_open == True):
        app.labelconnected.place(x=200, y=20)
        app.optionmenu_serial_port.place_forget()
        

def telemetry_mode(app):
    global lines
    ########## WIDGETS ########### 
    app.geometry("1000x800")
    app.resizable(False,False)

    ports = serial.tools.list_ports.comports()

    # Agregar todos los puertos a una lista
    for port in ports:
        port_list.append(port.device+": "+port.description)


    def debug_mode():
        global selected_serial_communication
        global serial_communication

        global battery_voltage_value
        global oil_pressure_value
        global neutral_gear_value
        global tachometer_value
        global speedometer_value
        global fuel_value
        
        app.textbox.place(x=250, y=700)
        app.textbox.insert("insert","---------------------------------------------------------------------\tDEBUG MODE ENABLED\t--------------------------------------------------------------------\n")

        if(serial_communication.is_open == True):
            while True:
                
                RawString = serial_communication.readline()                                  #Datos leidos sin tratar enviados por Arduino.
                RawDataIn = RawString.decode("utf-8").strip()
                RawDataIn = RawDataIn.split(",")
                len_RawDataIn =  len(RawDataIn)
                if (len_RawDataIn == 4):
                    RawDataIn.pop(0)
                DataIn = int(RawDataIn[1])

                bin_num = bin(DataIn & int("1"*32, 2))[2:]
                #print(bin_num)                                #Decodificamos datos enviados por Arduino de binario a string.
                #bin_num = "10001110010110100101101110010001"
                battery_voltage_value = int(bin_num) & 0xFF
                oil_pressure_value = int(bin_num,2) >> 8 & 0b1
                neutral_gear_value = int(bin_num,2) >> 9 & 0b1
                tachometer_value = int(bin_num,2) >> 10 & 0xFF
                speedometer_value = int(bin_num,2) >> 18 & 0xFF
                fuel_value = int(bin_num,2) >> 26 & 0x7F

                app.textbox.insert("insert", 
                                "Battery Voltage: "+ str(battery_voltage_value) + "\t\t          " +
                                "Oil Pressure: "+ str(oil_pressure_value) + "\t\t          " +
                                "Neutral Gear: "+ str(neutral_gear_value) + "\t\t          " +
                                "Engine RPM: " + str(tachometer_value) + "\t\t          " + 
                                "Speed [Km/h]: "+ str(speedometer_value) + "\t\t          " +
                                "Fuel [%]: "+ str(fuel_value) +"\n")
                
            
            

    app.back_button = customtkinter.CTkButton(master=app,
                                                text="Back",
                                                command=FromSelectionWindowToStartWindow,
                                                width=200,
                                                fg_color="#C70039",
                                                hover_color="#7A0023",
                                                border_width=2,
                                                border_color="black")
    
    app.optionmenu_serial_port = customtkinter.CTkOptionMenu(master=app,
                                                            height=25,
                                                            width=500,
                                                            dynamic_resizing= False,
                                                            values=port_list)
    
    app.connect_serial_port_button = customtkinter. CTkButton(master=app,
                                                            height=25,
                                                            width=125,
                                                            text= "CONNECT",
                                                            fg_color="#626567",
                                                            hover_color="#00FF00",
                                                            command=start_serial_communication)
    
    app.labelconnected = customtkinter.CTkLabel(master=app,
                                                   text= "SUCCESSFULLY CONNECTED")
    
    app.frame_data_1 = customtkinter.CTkFrame(master=app,
                                            width= 975,
                                            height=600,
                                            corner_radius=5,
                                            fg_color="#626567")
    
    #app.frame_data_2 = customtkinter.CTkFrame(master=app,
    #                                    width= 975,
    #                                    height=200,
    #                                    corner_radius=5,
    #                                    fg_color="#626567")
    #
    #app.frame_data_3 = customtkinter.CTkFrame(master=app,
    #                                        width= 975,
    #                                        height=200,
    #                                        corner_radius=5,
    #                                        fg_color="#626567")
    
    app.debug_button = customtkinter.CTkButton(master=app,
                                                text="DEBUG MODE",
                                                command=debug_mode,
                                                width=200,
                                                fg_color="#C70039",
                                                hover_color="#7A0023",
                                                border_width=2,
                                                border_color="black")

    app.frame_debug = customtkinter.CTkFrame(master=app,
                                             width= 300,
                                             height=30,
                                             corner_radius=5,
                                             fg_color="#626567")
    
    app.textbox = customtkinter.CTkTextbox(master=app,
                                      border_width=2,
                                      height= 90,
                                      width=725,
                                      font=customtkinter.CTkFont(size=14),
                                      activate_scrollbars=False,
                                      corner_radius=5)
    


    ########### PLACEs ###########
    app.back_button.place(x=25, y=750)
    app.optionmenu_serial_port.place(x=15, y=20)
    app.connect_serial_port_button.place(x=565, y=20)
    app.frame_data_1.place(x=15, y=75)
    #app.frame_data_2.place(x=15, y=300)
    #app.frame_data_3.place(x=15, y=525)
    app.debug_button.place(x=775 ,y=20)
    #if(serial_communication.is_open == True):
    plot_realdata()
    





    
def plot_values():
    #x_vals=[0,1,2,3,4,5]
    #y_vals=[0,5,1,3,2,4]

    x_vals=[]
    y_vals1=[]
    y_vals2=[]

    index=count()
    fig = Figure(figsize=(12.25,1.75), dpi=75)
    def animate(i):
        
        x_vals.append(next(index))
        y_vals1.append(random.randint(0,10))
        y_vals2.append(random.randint(0,10))

        plt.cla()

        plot = plt.plot(x_vals,y_vals1, label= "Channel 1")
        plot = plt.plot(x_vals,y_vals2, label= "Channel 2")

        plt.grid()
        plt.legend(loc="upper left")
        plt.tight_layout()
    
    ani = FuncAnimation(plt.gcf(), animate, interval=1000, frames=10)
    canvas = FigureCanvasTkAgg(fig, master=app)
    canvas.get_tk_widget().place(x=15, y=45)

    #plt.show()


    #figure = plt.figure(figsize=(12.25,1.75), dpi=75)
    #figure.add_subplot(111).plot(x_vals,y_vals)
    #chart = FigureCanvasTkAgg(figure, app)
    #chart.get_tk_widget().place(x=15, y=45)
    
def plot_object1():
    global cond
    #-----------------------------------------PLOT OBJECT ON GUI-----------------------
    fig = Figure();
    fig = Figure(figsize=(12.25,1.75), dpi=75)
    ax = fig.add_subplot(111)

    ax.set_title("CHANNEL 1")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Voltage")
    ax.set_xlim(0, 5)
    ax.set_ylim(-0.5, 100)
    lines = ax.plot([],[])[0]


    canvas = FigureCanvasTkAgg(fig, master=app) 
    canvas.get_tk_widget().place(x=15, y=15, width = 920, height= 165)
    canvas.draw()

    #----------------------------BUTTON-----------------------------
    app.update();
    
    data = np.array([random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100)])
    time = np.array([0,1,2,3,4,5])
    lines.set_xdata(time)
    lines.set_ydata(data)

    if (cond == True):
        canvas = FigureCanvasTkAgg(fig, master=app)
        canvas.get_tk_widget().place(x=15, y=15, width = 920, height= 165)
        canvas.draw()
        app.after(1000,plot_object1)

def plot_object2():
    
    #-----------------------------------------PLOT OBJECT ON GUI-----------------------
    fig = Figure();
    fig = Figure(figsize=(12.25,1.75), dpi=75)
    ax = fig.add_subplot(111)

    ax.set_title("CHANNEL 2")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Voltage")
    ax.set_xlim(0, 5)
    ax.set_ylim(-100, 100)
    lines = ax.plot([],[])[0]

    canvas = FigureCanvasTkAgg(fig, master=app)
    canvas.get_tk_widget().place(x=15, y=195, width = 920, height= 165)
    canvas.draw()

    #----------------------------BUTTON-----------------------------
    app.update();
    
    data = np.array([random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100)])
    time = np.array([0,1,2,3,4,5])
    lines.set_xdata(time)
    lines.set_ydata(data)

    canvas.draw()
    app.after(1000,plot_object2)

def plot_object3():
    
    #-----------------------------------------PLOT OBJECT ON GUI-----------------------
    fig = Figure();
    fig = Figure(figsize=(12.25,1.75), dpi=75)
    ax = fig.add_subplot(111)

    ax.set_title("CHANNEL 3")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Voltage")
    ax.set_xlim(0, 5)
    ax.set_ylim(-0.5, 100)
    lines = ax.plot([],[])[0]

    canvas = FigureCanvasTkAgg(fig, master=app)
    canvas.get_tk_widget().place(x=15, y=375, width = 920, height= 165)
    canvas.draw()

    #----------------------------BUTTON-----------------------------
    app.update();
    
    data = np.array([random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100)])
    time = np.array([0,1,2,3,4,5])
    lines.set_xdata(time)
    lines.set_ydata(data)

    canvas.draw()
    app.after(1000,plot_object3)

def plot_realdata():
    global selected_serial_communication
    global serial_communication

    global battery_voltage_value
    global oil_pressure_value
    global neutral_gear_value
    global tachometer_value
    global speedometer_value
    global fuel_value

    global data_matrix
    global lines

    data_received = []

    if(serial_communication.is_open == True):

        RawString = serial_communication.readline()                                  #Datos leidos sin tratar enviados por ECU.
        RawDataIn = RawString.decode("utf-8").strip()
        RawDataIn = RawDataIn.split(",")
        DataIn = int(RawDataIn[1])
        bin_num = bin(DataIn & int("1"*32, 2))[2:]

        battery_voltage_value = int(bin_num) & 0xFF
        oil_pressure_value = int(bin_num,2) >> 8 & 0b1
        neutral_gear_value = int(bin_num,2) >> 9 & 0b1
        tachometer_value = int(bin_num,2) >> 10 & 0xFF
        speedometer_value = int(bin_num,2) >> 18 & 0xFF
        fuel_value = int(bin_num,2) >> 26 & 0x7F

        with open('Data_recorded.csv', mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(battery_voltage_value, oil_pressure_value, neutral_gear_value, tachometer_value, speedometer_value, fuel_value)
        data_received.append(battery_voltage_value, oil_pressure_value, neutral_gear_value, tachometer_value, speedometer_value, fuel_value)
        
        data_matrix.append(data_received)



    #-----------------------------------------PLOT OBJECT ON GUI-----------------------
    fig = Figure();
    fig = Figure(figsize=(12.25,1.75), dpi=75)
    ax = fig.add_subplot(111)

    ax.set_title("REAL ADQUIRED DATA")
    ax.set_xlabel("TIME")
    ax.set_ylabel("Voltage")
    ax.set_xlim(0, 5)
    ax.set_ylim(-0.5, 100)
    lines = ax.plot([],[])[0]

    canvas = FigureCanvasTkAgg(fig, master=app)
    canvas.get_tk_widget().place(x=25, y=90, width = 950, height= 575)
    canvas.draw()
    app.update();
    
    data = np.array([random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100)])
    time = np.array([0,1,2,3,4,5])
    lines.set_xdata(time)
    lines.set_ydata(data)

start_window(app)
app.mainloop()

exit()