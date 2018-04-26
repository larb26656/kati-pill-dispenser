import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.IN)
GPIO.setup(26, GPIO.IN)

def get_is_people_come():
    if(GPIO.input(26)==0):
        return True
    else:
        return False

def get_is_exist_glass():
    if(GPIO.input(19)==0):
        return True
    else:
        return False

def get_is_not_exist_glass():
    if(GPIO.input(19)==0):
        return False
    else:
        return True

    
