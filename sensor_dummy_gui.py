from tkinter import *
import time
from tkinter import messagebox

top = Tk()
top.geometry("400x100")
infrared_val = StringVar()
ultrasonic_val = StringVar()
stepmotor_val = StringVar()

def set_people_come():
    f = open('sensor_dummy_data/infrared_status.txt', 'r+', encoding='utf-8')
    f.write("0")
    f.close

def set_people_gone():
    f = open('sensor_dummy_data/infrared_status.txt', 'r+', encoding='utf-8')
    f.write("1")
    f.close

def set_glass_in():
    f = open('sensor_dummy_data/ultrasonic_status.txt', 'r+', encoding='utf-8')
    f.write("1")
    f.close

def set_glass_out():
    f = open('sensor_dummy_data/ultrasonic_status.txt', 'r+', encoding='utf-8')
    f.write("0")
    f.close

def get_infrared_text():
    f = open('sensor_dummy_data/infrared_status.txt', 'r+', encoding='utf-8')
    data = f.read()
    f.close()
    if(int(data)==0):
        return "Infrared sensor status : Found human"
    else:
        return "Infrared sensor status : Not found"

def get_ultrasonic_text():
    f = open('sensor_dummy_data/ultrasonic_status.txt', 'r+', encoding='utf-8')
    data = f.read()
    f.close()
    if(int(data)==1):
        return "Ultrasonic sensor status : glass in robot"
    else:
        return "Ultrasonic sensor status : glass out robot"

def people_come_button_do():
    set_people_come()
    infrared_val.set(get_infrared_text())

def people_gone_button_do():
    set_people_gone()
    infrared_val.set(get_infrared_text())

def glass_in_button_do():
    set_glass_in()
    ultrasonic_val.set(get_ultrasonic_text())

def glass_out_button_do():
    set_glass_out()
    ultrasonic_val.set(get_ultrasonic_text())

set_people_gone()
set_glass_in()
infrared_label = Label(top,  textvariable=infrared_val)
infrared_val.set(get_infrared_text())
ultrasonic_label = Label(top, textvariable=ultrasonic_val)
ultrasonic_val.set(get_ultrasonic_text())
stepmotor_label = Label(top, textvariable=stepmotor_val)
people_come_button = Button(top, text ="People come", command = people_come_button_do)
people_gone_button = Button(top, text ="People gone", command = people_gone_button_do)
glass_in_button = Button(top, text ="Put the glass in", command = glass_in_button_do)
glass_out_button = Button(top, text ="Put the glass out", command = glass_out_button_do)
infrared_label.place(x=0,y=0)
ultrasonic_label.place(x=0,y=15)
stepmotor_label.place(x=0,y=30)
people_come_button.place(x=0,y=45)
people_gone_button.place(x=100,y=45)
glass_in_button.place(x=200,y=45)
glass_out_button.place(x=300,y=45)

top.mainloop()