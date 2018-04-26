import pymysql
import connect_service

def get_config_attribute(attribute):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `config` WHERE Config_name = '" + str(attribute) + "' AND Config_visiblestatus = '1'")
    numrows = int(cur.rowcount)
    if (numrows >= 1):
        for r in cur:
            return str(r['Config_value'])
    else:
        return None
    cur.close()
    conn.close()

def set_config_attribute(attribute,value):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("UPDATE config SET Config_value = '" + str(value) + "' WHERE Config_name = '" + str(attribute) + "'")
    conn.commit()
    cur.close()
    conn.close()

def get_config_robot_connect_status():
    return get_config_attribute("Robot_connect_status")

def set_config_robot_connect_true_status():
    set_config_attribute("Robot_connect_status","1")

def set_config_robot_connect_false_status():
    set_config_attribute("Robot_connect_status","0")

def get_config_robot_face_status():
    return get_config_attribute("Robot_face_status")

def set_config_robot_face_normal_status():
    set_config_attribute("Robot_face_status", "normal")

def set_config_robot_face_talk_status():
    set_config_attribute("Robot_face_status", "talk")

def get_config_robot_lang():
    return get_config_attribute("Robot_lang")

def get_config_pill_dispenser_status():
    result = get_config_attribute("Robot_pill_dispenser_status")
    if(result == "1"):
        return True
    elif (result == "0"):
        return False
    else:
        return False

def get_config_pill_dispenser_pill_id():
    return get_config_attribute("Robot_pill_dispenser_pill_id")

def set_config_pill_dispenser_true_status(pill_id):
    set_config_attribute("Robot_pill_dispenser_status", "1")
    set_config_attribute("Robot_pill_dispenser_pill_id", str(pill_id))

def set_pill_dispenser_false_status():
    set_config_attribute("Robot_pill_dispenser_status", "0")
    set_config_attribute("Robot_pill_dispenser_pill_id", "0")

def get_config_robot_status():
    return get_config_attribute("Robot_status")

def set_config_robot_free_status():
    set_config_attribute("Robot_status", "free")

def set_config_robot_schedule_status():
    set_config_attribute("Robot_status", "schedule")

def set_config_robot_memo_status():
    set_config_attribute("Robot_status", "memo")

def set_config_robot_pill_dispenser_status():
    set_config_attribute("Robot_status", "pill_dispenser")

def get_config_robot_schedule_status():
    result = get_config_attribute("Robot_get_schedule_status")
    if(result == "1"):
        return True
    elif (result == "0"):
        return False
    else:
        return False
    
def set_config_robot_schedule_true_status():
    set_config_attribute("Robot_get_schedule_status", "1")
    
def set_config_robot_schedule_false_status():
    set_config_attribute("Robot_get_schedule_status", "0")
    
    
