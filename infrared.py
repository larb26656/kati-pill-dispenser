import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)

def get_distance_less():
    if(GPIO.input(26)==0):
        return True
    else:
        return False

    
