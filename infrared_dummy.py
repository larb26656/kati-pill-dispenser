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

"""def test_a():
    print("success")

def aaaa(method):
    count1 = 0
    count2 = 0
    while True:
        if(get_distance_less()):
            count1 = count1 + 1
            print("count1:"+str(count1))
            if(count1 == 20):
                method()
        else:
            count2 = count2 + 1
            print("count2:"+str(count2))
            if(count2 == 20):
                return False
        time.sleep(1)

aaaa(test_a)"""

