import time

def get_distance_less():
    f = open('sensor_dummy_data/infrared_status.txt', 'r', encoding='utf-8')
    data = f.read()
    f.close()
    if(int(data)==0):
        return True
    else:
        return False

def start_count_detect():
    count_status = False
    count = 0
    countdown = 3
    while (count_status==False):
        if(get_distance_less()):
            count=count+1
            if(count == 3):
                break
        else:
            if(count > 0):
                if(countdown > 0):
                    countdown=countdown-1
                else:
                    if(count >= 0 ):
                        count=count-1
            else:
                countdown = 3
        time.sleep(1)