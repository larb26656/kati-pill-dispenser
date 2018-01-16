def get_distance_less():
    f = open('sensor_dummy_data/infrared_status.txt', 'r', encoding='utf-8')
    data = f.read()
    f.close()
    if(int(data)==0):
        return True
    else:
        return False
    
