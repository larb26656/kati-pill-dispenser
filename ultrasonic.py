#Libraries
import RPi.GPIO as GPIO
import time
import math
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
echo_pin = 13
trig_pin = 19
ultrasonic_range = 3
ultrasonic_range_more = 4

GPIO.setup(echo_pin, GPIO.IN)
GPIO.setup(trig_pin, GPIO.OUT)


def get_distance_less():
    # set Trigger to HIGH
    GPIO.output(trig_pin, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(echo_pin) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(echo_pin) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = math.floor((TimeElapsed * 34300) / 2)

  
 
    if(distance <= ultrasonic_range):
        return True
    else:
        return False

    
def get_distance_more():
    # set Trigger to HIGH
    GPIO.output(trig_pin, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(echo_pin) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(echo_pin) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = math.floor((TimeElapsed * 34300) / 2)
    
    if(distance >= ultrasonic_range_more):
        return True
    else:
        return False
