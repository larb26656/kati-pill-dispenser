def get_distance_less():
    f = open('sensor_dummy_data/ultrasonic_status.txt', 'r', encoding='utf-8')
    data = f.read()
    f.close()
    if(int(data)==1):
        return True
    else:
        return False

def get_distance_more():
    f = open('sensor_dummy_data/ultrasonic_status.txt', 'r', encoding='utf-8')
    data = f.read()
    f.close()
    if(int(data)==0):
        return True
    else:
        return False
