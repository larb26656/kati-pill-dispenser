"""import serial
import time

from click._compat import raw_input

arduino = serial.Serial('COM3', 9600)
arduino.write('ssss'.encode())
while True:
	data = arduino.readline()[:-2] #the last bit gets rid of the new-line 
	if data:
		print(data)
	time.sleep(1) """
from time import sleep
import serial


ser = serial.Serial('/dev/ttyUSB0', 9600) # Establish the connection on a specific port

def moving_step_motor(slot_num,num_of_dispenser):
     sleep(1)
     json_text = "{'type':'pill_dispenser','slot_num':"+str(slot_num)+",'num_of_dispenser':"+str(num_of_dispenser)+"}"
     ser.write(json_text.encode())
     ser.flush()
     print(ser.readline()[:-2].decode())

def get_current_time():
     sleep(1)
     json_text = "{'type':'current_time'}"
     ser.write(json_text.encode())
     ser.flush()
     print(ser.readline()[:-2].decode())

