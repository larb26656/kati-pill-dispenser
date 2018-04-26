from PyQt4 import QtCore as core
import pymysql
import connect_service
import pyrebase
from time import localtime, strftime
import time
import threading
import config_service
import json
import ast

def get_json_format(data,result):
    return json.dumps({"data": data, "result": result}, ensure_ascii=False)

def get_dict_from_json(json_data):
    return ast.literal_eval(json_data)

def get_date_time_short():
    return str(strftime("%Y%m%d%H%M%S", localtime()))

def get_date_time_full():
    return str(strftime("%d/%m/%Y %H:%M", localtime()))

def get_english_pill_unit_convert(num):
    if(int(num)<=1):
        return str(num)+" pill"
    else:
        return str(num)+" pills"

def get_last_pill_log_id():
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='kati',charset='utf8')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `pill_log`ORDER BY Pill_log_id DESC")
    for r in cur:
        return str(r['Pill_log_id'])
    cur.close()
    conn.close()

def get_last_behavior_id():
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `behavior`ORDER BY Behavior_id DESC")
    for r in cur:
        return str(r['Behavior_id'])
    cur.close()
    conn.close()

def get_available_member_id():
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `member` WHERE `Member_visiblestatus` = '1'")
    for r in cur:
        return str(r['Member_id'])
    cur.close()
    conn.close()
    
def get_available_token_kati_read_list():
    list = []
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `outsider` WHERE `Outsider_visiblestatus` = '1' AND Outsider_level <> 'patient'")
    for r in cur:
        list.append(str(r['Outsider_token']))
    return(list)
    cur.close()
    conn.close()

def get_available_token_kati_command_list():
    list = []
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `outsider` WHERE `Outsider_visiblestatus` = '1' AND Outsider_level = 'patient'")
    for r in cur:
        list.append(str(r['Outsider_token']))
    return(list)
    cur.close()
    conn.close()

def get_available_token_kati_read_dict():
    count=0
    dict = {}
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `outsider` WHERE `Outsider_visiblestatus` = '1' AND Outsider_level <> 'patient'")
    for r in cur:
        dict[count]=[str(r['Outsider_id']),str(r['Outsider_token'])]
        count +=1
    return dict
    cur.close()
    conn.close()

def get_available_token_kati_command_dict():
    count=0
    dict = {}
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `outsider` WHERE `Outsider_visiblestatus` = '1' AND Outsider_level = 'patient'")
    for r in cur:
        dict[count]=[str(r['Outsider_id']),str(r['Outsider_token'])]
        count +=1
    return dict
    cur.close()
    conn.close()

def get_pill_thai_commonname_with_pill_id(pill_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `pill` WHERE Pill_id = '"+str(pill_id)+"'")
    for r in cur:
        return str(r['Pill_commonname_thai'])
    cur.close()
    conn.close()

def get_pill_thai_commonname_with_pill_log_id(pill_log_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `pill_log` INNER JOIN pill ON pill_log.Pill_id = pill.Pill_id WHERE Pill_log_id= '"+str(pill_log_id)+"'")
    for r in cur:
        return str(r['Pill_commonname_thai'])
    cur.close()
    conn.close()

def get_pill_english_commonname_with_pill_id(pill_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `pill` WHERE Pill_id = '"+str(pill_id)+"'")
    for r in cur:
        return str(r['Pill_commonname_english'])
    cur.close()
    conn.close()

def get_pill_english_commonname_with_pill_log_id(pill_log_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `pill_log` INNER JOIN pill ON pill_log.Pill_id = pill.Pill_id WHERE Pill_log_id= '"+str(pill_log_id)+"'")
    for r in cur:
        return str(r['Pill_commonname_english'])
    cur.close()
    conn.close()

def get_date_time_short_with_pill_log_id(pill_log_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT CONCAT(SUBSTRING(Pill_log_datetime,1,4) ,SUBSTRING(Pill_log_datetime,6,2),SUBSTRING(Pill_log_datetime,9,2),SUBSTRING(Pill_log_datetime,12,2),SUBSTRING(Pill_log_datetime,15,2),SUBSTRING(Pill_log_datetime,18,2)) AS Date_time_short ,CONCAT(SUBSTRING(Pill_log_datetime,9,2),'/',SUBSTRING(Pill_log_datetime,6,2),'/',SUBSTRING(Pill_log_datetime,1,4) ,' ',SUBSTRING(Pill_log_datetime,12,2),':',SUBSTRING(Pill_log_datetime,15,2)) AS Date_time_full FROM `pill_log` WHERE Pill_log_id ='"+str(pill_log_id)+"'")
    for r in cur:
        return str(r['Date_time_short'])
    cur.close()
    conn.close()

def get_date_time_full_with_pill_log_id(pill_log_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(
        "SELECT CONCAT(SUBSTRING(Pill_log_datetime,1,4) ,SUBSTRING(Pill_log_datetime,6,2),SUBSTRING(Pill_log_datetime,9,2),SUBSTRING(Pill_log_datetime,12,2),SUBSTRING(Pill_log_datetime,15,2),SUBSTRING(Pill_log_datetime,18,2)) AS Date_time_short ,CONCAT(SUBSTRING(Pill_log_datetime,9,2),'/',SUBSTRING(Pill_log_datetime,6,2),'/',SUBSTRING(Pill_log_datetime,1,4) ,' ',SUBSTRING(Pill_log_datetime,12,2),':',SUBSTRING(Pill_log_datetime,15,2)) AS Date_time_full FROM `pill_log` WHERE Pill_log_id ='" + str(pill_log_id) + "'")
    for r in cur:
        return str(r['Date_time_full'])
    cur.close()
    conn.close()

def get_date_time_short_with_behavior_id(behavior_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT CONCAT(SUBSTRING(Behavior_datetime,1,4) ,SUBSTRING(Behavior_datetime,6,2),SUBSTRING(Behavior_datetime,9,2),SUBSTRING(Behavior_datetime,12,2),SUBSTRING(Behavior_datetime,15,2),SUBSTRING(Behavior_datetime,18,2)) AS Date_time_short ,CONCAT(SUBSTRING(Behavior_datetime,9,2),'/',SUBSTRING(Behavior_datetime,6,2),'/',SUBSTRING(Behavior_datetime,1,4) ,' ',SUBSTRING(Behavior_datetime,12,2),':',SUBSTRING(Behavior_datetime,15,2)) AS Date_time_full FROM behavior WHERE Behavior_id = '"+str(behavior_id)+"'")
    for r in cur:
        return str(r['Date_time_short'])
    cur.close()
    conn.close()

def get_date_time_full_with_behavior_id(behavior_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(
        "SELECT CONCAT(SUBSTRING(Behavior_datetime,1,4) ,SUBSTRING(Behavior_datetime,6,2),SUBSTRING(Behavior_datetime,9,2),SUBSTRING(Behavior_datetime,12,2),SUBSTRING(Behavior_datetime,15,2),SUBSTRING(Behavior_datetime,18,2)) AS Date_time_short ,CONCAT(SUBSTRING(Behavior_datetime,9,2),'/',SUBSTRING(Behavior_datetime,6,2),'/',SUBSTRING(Behavior_datetime,1,4) ,' ',SUBSTRING(Behavior_datetime,12,2),':',SUBSTRING(Behavior_datetime,15,2)) AS Date_time_full FROM behavior WHERE Behavior_id = '" + str(behavior_id) + "'")
    for r in cur:
        return str(r['Date_time_full'])
    cur.close()
    conn.close()

def get_pills_thai_commonname_with_schedule_id(schedule_id):
    pills_name = ""
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `schedule` INNER JOIN dispenser ON schedule.Schedule_id=dispenser.Schedule_id INNER JOIN slot ON dispenser.Slot_id=slot.Slot_id INNER JOIN pill ON slot.Pill_id=pill.Pill_id WHERE dispenser.Schedule_id = '"+str(schedule_id)+"'")
    for r in cur:
        pills_name += str(r['Pill_commonname_thai'])+" "+str(r['Pill_dispenseramount'])+" เม็ด "
    return str(pills_name)
    cur.close()
    conn.close()

def get_pills_english_commonname_with_schedule_id(schedule_id):
    pills_name = ""
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `schedule` INNER JOIN dispenser ON schedule.Schedule_id=dispenser.Schedule_id INNER JOIN slot ON dispenser.Slot_id=slot.Slot_id INNER JOIN pill ON slot.Pill_id=pill.Pill_id WHERE dispenser.Schedule_id = '"+str(schedule_id)+"'")
    for r in cur:
        pills_name += str(r['Pill_commonname_english'])+" "+get_english_pill_unit_convert(str(r['Pill_dispenseramount']))+" "
    return str(pills_name)
    cur.close()
    conn.close()

def get_pills_thai_commonname_with_behavior_id(behavior_id):
    pills_name = ""
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `behavior` INNER JOIN schedule ON behavior.Schedule_id=schedule.Schedule_id INNER JOIN dispenser ON schedule.Schedule_id=dispenser.Schedule_id INNER JOIN slot ON dispenser.Slot_id=slot.Slot_id INNER JOIN pill ON slot.Pill_id=pill.Pill_id WHERE Behavior_id = '"+str(behavior_id)+"'")
    for r in cur:
        pills_name += str(r['Pill_commonname_thai'])+" "+str(r['Pill_dispenseramount'])+" เม็ด "
    return str(pills_name)
    cur.close()
    conn.close()

def get_pills_english_commonname_with_behavior_id(behavior_id):
    pills_name = ""
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `behavior` INNER JOIN schedule ON behavior.Schedule_id=schedule.Schedule_id INNER JOIN dispenser ON schedule.Schedule_id=dispenser.Schedule_id INNER JOIN slot ON dispenser.Slot_id=slot.Slot_id INNER JOIN pill ON slot.Pill_id=pill.Pill_id WHERE Behavior_id = '" + str(behavior_id) + "'")
    for r in cur:
        pills_name += str(r['Pill_commonname_english'])+" "+get_english_pill_unit_convert(str(r['Pill_dispenseramount']))+" "
    return str(pills_name)
    cur.close()
    conn.close()

def get_one_pill_thai_commonname_with_behavior_id(behavior_id):
    pill_name = ""
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `behavior` INNER JOIN pill ON behavior.Pill_id=pill.Pill_id  WHERE Behavior_id = '" + str(behavior_id) + "'")
    for r in cur:
        pill_name += str(r['Pill_commonname_thai'])+" "+str(r['Pill_dispenseramount'])+" เม็ด "
    return str(pill_name)
    cur.close()
    conn.close()

def get_one_pill_english_commonname_with_behavior_id(behavior_id):
    pill_name = ""
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `behavior` INNER JOIN pill ON behavior.Pill_id=pill.Pill_id  WHERE Behavior_id = '" + str(behavior_id) + "'")
    for r in cur:
        pill_name += str(r['Pill_commonname_english'])+" "+get_english_pill_unit_convert(str(r['Pill_dispenseramount']))+" "
    return str(pill_name)
    cur.close()
    conn.close()

def get_firebase_database_sent_error_log_dict():
    count = 0
    dict = {}
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `firebase_error_log` WHERE Firebase_error_log_service = 'database'")
    numrows = int(cur.rowcount)
    if(numrows >= 1):
        for r in cur:
            dict[count]=[str(r['Firebase_error_log_id']),str(r['Firebase_error_log_JSON_detail'])]
            count += 1
        return dict
    else:
        return None
    cur.close()
    conn.close()

def get_firebase_notification_sent_error_log_dict():
    count = 0
    dict = {}
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `firebase_error_log` WHERE Firebase_error_log_service = 'notification'")
    numrows = int(cur.rowcount)
    if(numrows >= 1):
        for r in cur:
            dict[count]=[str(r['Firebase_error_log_id']),str(r['Firebase_error_log_JSON_detail'])]
            count += 1
        return dict
    else:
        return None
    cur.close()
    conn.close()

def check_outsider():
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `outsider` WHERE `Outsider_visiblestatus` = '1'")
    numrows = int(cur.rowcount)
    if(numrows >= 1):
        return True
    else:
        return False
    cur.close()
    conn.close()

def delete_firebase_error_log(firebase_error_log_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("DELETE FROM firebase_error_log WHERE Firebase_error_log_id = '"+firebase_error_log_id+"'")
    conn.commit()
    cur.close()
    conn.close()
    
def insert_pill_out_of_stock_message(pill_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("INSERT INTO pill_log(Pill_log_type,Pill_log_datetime,Pill_id) value('outofstock',NOW(),'"+str(pill_id)+"')")
    primary_key=cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()
    return primary_key

def insert_pill_almost_out_of_stock_message(pill_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("INSERT INTO pill_log(Pill_log_type,Pill_log_datetime,Pill_id) value('almostoutofstock',NOW(),'"+str(pill_id)+"')")
    primary_key = cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()
    return primary_key
    
def insert_pill_log_notification():
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("INSERT INTO pill_log_notification(Pill_log_id,Member_id,Msg_status) values('"+get_last_pill_log_id()+"','"+get_available_member_id()+"','1')")
    conn.commit()
    cur.close()
    conn.close()

def insert_behavior_took_pill_message(schedule_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("INSERT INTO behavior(Behavior_type,Behavior_datetime,Schedule_id,Pill_id) value('tookpill',NOW(),'"+str(schedule_id)+"','0')")
    primary_key = cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()
    return primary_key

def insert_behavior_forgot_take_pill_message(schedule_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("INSERT INTO behavior(Behavior_type,Behavior_datetime,Schedule_id,Pill_id) value('forgottakepill',NOW(),'"+str(schedule_id)+"','0')")
    primary_key = cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()
    return primary_key

def insert_behavior_took_one_pill_message(pill_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("INSERT INTO behavior(Behavior_type,Behavior_datetime,Schedule_id,Pill_id) value('tookpill',NOW(),'0','"+str(pill_id)+"')")
    primary_key = cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()
    return primary_key

def insert_behavior_forgot_take_one_pill_message(pill_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("INSERT INTO behavior(Behavior_type,Behavior_datetime,Schedule_id,Pill_id) value('forgottakepill',NOW(),'0','"+str(pill_id)+"')")
    primary_key = cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()
    return primary_key

def insert_behavior_come_but_no_take_pill_message():
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("INSERT INTO behavior(Behavior_type,Behavior_datetime,Schedule_id,Pill_id) value('comebutnotakepill',NOW(),'0','0')")
    primary_key = cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()
    return primary_key

def insert_behavior_notification():
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("INSERT INTO behavior_notification(Behavior_id,Member_id,Msg_status) values('"+get_last_behavior_id()+"','"+get_available_member_id()+"','1')")
    conn.commit()
    cur.close()
    conn.close()

def insert_memo_log(memo_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("INSERT INTO memo_log(Memo_id,Memo_log_datetime) value('"+str(memo_id)+"',NOW())")
    primary_key=cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()
    return primary_key

def insert_firebase_notification_sent_error_log(json_data):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("INSERT INTO firebase_error_log(Firebase_error_log_service,Firebase_error_log_JSON_detail) values('notification',\""+str(json_data)+"\")")
    conn.commit()
    cur.close()
    conn.close()

def insert_firebase_database_sent_error_log(json_data):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("INSERT INTO firebase_error_log(Firebase_error_log_service,Firebase_error_log_JSON_detail) values('database',\""+str(json_data)+"\")")
    conn.commit()
    cur.close()
    conn.close()

def sent_firebase_notification_with_json(json_data):
    data_message = get_dict_from_json(json_data)
    try:
        push_service = connect_service.get_connect_firebase_cloud_message_kati_read()
        registration_ids = get_available_token_kati_read_list()
        try:
            push_service.multiple_devices_data_message(registration_ids=registration_ids, data_message=data_message)
            config_service.set_config_robot_connect_true_status()
            return True
        except:
            config_service.set_config_robot_connect_false_status()
            return False
    except:
        config_service.set_config_robot_connect_false_status()
        return False

def sent_firebase_pill_out_of_stock_notification(pill_log_id):
    data_message = {
        "Title": "<Pill>",
        "Body_thai": "ยา " + get_pill_thai_commonname_with_pill_log_id(pill_log_id) + " หมด",
        "Body_english": get_pill_english_commonname_with_pill_log_id(pill_log_id) + " is out of stock",
    }
    try:
        push_service = connect_service.get_connect_firebase_cloud_message_kati_read()
        registration_ids = get_available_token_kati_read_list()
        try:
            push_service.multiple_devices_data_message(registration_ids=registration_ids, data_message=data_message)
            config_service.set_config_robot_connect_true_status()
            return get_json_format(data_message, True)
        except:
            config_service.set_config_robot_connect_false_status()
            return get_json_format(data_message, False)
    except:
        config_service.set_config_robot_connect_false_status()
        return get_json_format(data_message, False)


def sent_firebase_pill_almost_out_of_stock_notification(pill_log_id):
    data_message = {
        "Title": "<Pill>",
        "Body_thai": "ยา " + get_pill_thai_commonname_with_pill_log_id(pill_log_id) + " ใกล้หมด",
        "Body_english": get_pill_english_commonname_with_pill_log_id(pill_log_id) + " is almost out of stock",
    }
    try:
        push_service = connect_service.get_connect_firebase_cloud_message_kati_read()
        registration_ids = get_available_token_kati_read_list()
        try:
            push_service.multiple_devices_data_message(registration_ids=registration_ids, data_message=data_message)
            config_service.set_config_robot_connect_true_status()
            return get_json_format(data_message, True)
        except:
            config_service.set_config_robot_connect_false_status()
            return get_json_format(data_message, False)
    except:
        config_service.set_config_robot_connect_false_status()
        return get_json_format(data_message, False)


def sent_firebase_behavior_took_pill_notification(behavior_id):
    data_message = {
        "Title": "<Behavior>",
        "Body_thai": "ผู้ป่วยรับประทานยา " + get_pills_thai_commonname_with_behavior_id(behavior_id),
        "Body_english": "Patient took a pill " + get_pills_english_commonname_with_behavior_id(behavior_id),
    }
    try:
        push_service = connect_service.get_connect_firebase_cloud_message_kati_read()
        registration_ids = get_available_token_kati_read_list()
        try:
            push_service.multiple_devices_data_message(registration_ids=registration_ids, data_message=data_message)
            config_service.set_config_robot_connect_true_status()
            return get_json_format(data_message, True)
        except:
            config_service.set_config_robot_connect_false_status()
            return get_json_format(data_message, False)
    except:
        config_service.set_config_robot_connect_false_status()
        return get_json_format(data_message, False)


def sent_firebase_behavior_forgot_take_pill_notification(behavior_id):
    data_message = {
        "Title": "<Behavior>",
        "Body_thai": "ผู้ป่วยลืมรับประทานยา " + get_pills_thai_commonname_with_behavior_id(behavior_id),
        "Body_english": "Patient forgot to take a pill " + get_pills_english_commonname_with_behavior_id(behavior_id),
    }
    try:
        push_service = connect_service.get_connect_firebase_cloud_message_kati_read()
        registration_ids = get_available_token_kati_read_list()
        try:
            push_service.multiple_devices_data_message(registration_ids=registration_ids, data_message=data_message)
            config_service.set_config_robot_connect_true_status()
            return get_json_format(data_message, True)
        except:
            config_service.set_config_robot_connect_false_status()
            return get_json_format(data_message, False)
    except:
        config_service.set_config_robot_connect_false_status()
        return get_json_format(data_message, False)


def sent_firebase_behavior_took_one_pill_notification(behavior_id):
    data_message = {
        "Title": "<Behavior>",
        "Body_thai": "ผู้ป่วยรับประทานยา " + get_one_pill_thai_commonname_with_behavior_id(behavior_id),
        "Body_english": "Patient took a pill " + get_one_pill_english_commonname_with_behavior_id(behavior_id),
    }
    try:
        push_service = connect_service.get_connect_firebase_cloud_message_kati_read()
        registration_ids = get_available_token_kati_read_list()
        try:
            push_service.multiple_devices_data_message(registration_ids=registration_ids, data_message=data_message)
            config_service.set_config_robot_connect_true_status()
            return get_json_format(data_message, True)
        except:
            config_service.set_config_robot_connect_false_status()
            return get_json_format(data_message, False)
    except:
        config_service.set_config_robot_connect_false_status()
        return get_json_format(data_message, False)


def sent_firebase_behavior_forgot_take_one_pill_notification(behavior_id):
    data_message = {
        "Title": "<Behavior>",
        "Body_thai": "ผู้ป่วยลืมรับประทานยา " + get_one_pill_thai_commonname_with_behavior_id(behavior_id),
        "Body_english": "Patient forgot to take a pill " + get_one_pill_english_commonname_with_behavior_id(
            behavior_id),
    }
    try:
        push_service = connect_service.get_connect_firebase_cloud_message_kati_read()
        registration_ids = get_available_token_kati_read_list()
        try:
            push_service.multiple_devices_data_message(registration_ids=registration_ids, data_message=data_message)
            config_service.set_config_robot_connect_true_status()
            return get_json_format(data_message, True)
        except:
            config_service.set_config_robot_connect_false_status()
            return get_json_format(data_message, False)
    except:
        config_service.set_config_robot_connect_false_status()
        return get_json_format(data_message, False)


def sent_firebase_behavior_come_but_no_take_pill_notification(self):
    data_message = {
        "Title": "<Behavior>",
        "Body_thai": "ผู้ป่วยมาหน้าเครื่องแต่ไม่ได้รับยา",
        "Body_english": "Patient Come to kati but no take pill.",
    }
    try:
        push_service = connect_service.get_connect_firebase_cloud_message_kati_read()
        registration_ids = get_available_token_kati_read_list()
        try:
            push_service.multiple_devices_data_message(registration_ids=registration_ids, data_message=data_message)
            config_service.set_config_robot_connect_true_status()
            return get_json_format(data_message, True)
        except:
            config_service.set_config_robot_connect_false_status()
            return get_json_format(data_message, False)
    except:
        config_service.set_config_robot_connect_false_status()
        return get_json_format(data_message, False)


def sent_firebase_memo_message_notification(message):
    data_message = {
        "Title": "<Message>",
        "Body_thai": str(message),
        "Body_english": str(message)
    }
    try:
        push_service = connect_service.get_connect_firebase_cloud_message_kati_command()
        registration_ids = get_available_token_kati_command_list()
        try:
            push_service.multiple_devices_data_message(registration_ids=registration_ids, data_message=data_message)
            config_service.set_config_robot_connect_true_status()
            return get_json_format(data_message, True)
        except:
            config_service.set_config_robot_connect_false_status()
            return get_json_format(data_message, False)
    except:
        config_service.set_config_robot_connect_false_status()
        return get_json_format(data_message, False)


def sent_firebase_schedule_message_notification():
    data_message = {
        "Title": "<Message>",
        "Body_thai": "ถึงเวลาที่คุณต้องรับประทานยาแล้วกรุณามารับประทานยาด้วยค่ะ",
        "Body_english": "It's time to take medicine please come to take medicine."
    }
    try:
        push_service = connect_service.get_connect_firebase_cloud_message_kati_command()
        registration_ids = get_available_token_kati_command_list()
        try:
            push_service.multiple_devices_data_message(registration_ids=registration_ids, data_message=data_message)
            config_service.set_config_robot_connect_true_status()
            return get_json_format(data_message, True)
        except:
            config_service.set_config_robot_connect_false_status()
            return get_json_format(data_message, False)
    except:
        config_service.set_config_robot_connect_false_status()
        return get_json_format(data_message, False)

def insert_firebase_database_with_json(json_data):
    data = get_dict_from_json(json_data)
    token = json.loads(json.dumps(get_dict_from_json(json_data)))['Token']
    try:
        firebase = pyrebase.initialize_app(connect_service.get_connect_firebase_real_time_database_kati_read())
        try:
            db = firebase.database()
            try:
                db.child(str(token+"/pill")).push(data)
                config_service.set_config_robot_connect_true_status()
                return True
            except:
                config_service.set_config_robot_connect_false_status()
                return False
        except:
            config_service.set_config_robot_connect_false_status()
            return False
    except:
        config_service.set_config_robot_connect_false_status()
        return False

def insert_firebase_pill_out_of_stock_data(pill_log_id, token):
    try:
        firebase = pyrebase.initialize_app(connect_service.get_connect_firebase_real_time_database_kati_read())
        try:
            db = firebase.database()
            data = {
                "Notification_detail_thai": "ยา " + get_pill_thai_commonname_with_pill_log_id(pill_log_id) + " หมด",
                "Notification_detail_english": get_pill_english_commonname_with_pill_log_id(
                    pill_log_id) + " is out of stock",
                "Notification_date": get_date_time_short_with_pill_log_id(pill_log_id),
                "Notification_date_with_format": get_date_time_full_with_pill_log_id(pill_log_id),
                "Token": str(token),
                "Notification_visible_status": "1",
                "Token_Notification_visible_status": str(token + "_1"),
            }
            try:
                db.child(str(token+"/pill")).push(data)
                config_service.set_config_robot_connect_true_status()
                return get_json_format(data,True)
            except:
                config_service.set_config_robot_connect_false_status()
                return get_json_format(data, False)
        except:
            config_service.set_config_robot_connect_false_status()
            return get_json_format(data, False)
    except:
        config_service.set_config_robot_connect_false_status()
        return get_json_format(data, False)

def insert_firebase_pill_almost_out_of_stock_data(pill_log_id, token):
    try:
        firebase = pyrebase.initialize_app(connect_service.get_connect_firebase_real_time_database_kati_read())
        try:
            db = firebase.database()
            data = {
              "Notification_detail_thai": "ยา " + get_pill_thai_commonname_with_pill_log_id(pill_log_id)+" ใกล้หมด",
              "Notification_detail_english": get_pill_english_commonname_with_pill_log_id(pill_log_id)+" is almost out of stock",
              "Notification_date": get_date_time_short_with_pill_log_id(pill_log_id),
              "Notification_date_with_format":  get_date_time_full_with_pill_log_id(pill_log_id),
              "Token": str(token),
              "Notification_visible_status": "1",
              "Token_Notification_visible_status": str(token+"_1"),
            }
            try:
                db.child(str(token+"/pill")).push(data)
                config_service.set_config_robot_connect_true_status()
                return get_json_format(data, True)
            except:
                config_service.set_config_robot_connect_false_status()
                return get_json_format(data, False)
        except:
            config_service.set_config_robot_connect_false_status()
            return get_json_format(data, False)
    except:
        config_service.set_config_robot_connect_false_status()
        return get_json_format(data, False)
    
def insert_firebase_behavior_took_pill_data(behavior_id, token):
    try:
        firebase = pyrebase.initialize_app(connect_service.get_connect_firebase_real_time_database_kati_read())
        try:
            db = firebase.database()
            data = {
              "Notification_detail_thai": "ผู้ป่วยรับประทานยา "+get_pills_thai_commonname_with_behavior_id(behavior_id),
              "Notification_detail_english": "Patient took a pill " + get_pills_english_commonname_with_behavior_id(behavior_id),
              "Notification_date": get_date_time_short_with_behavior_id(behavior_id),
              "Notification_date_with_format":  get_date_time_full_with_behavior_id(behavior_id),
              "Token": str(token),
              "Notification_visible_status": "1",
              "Token_Notification_visible_status": str(token+"_1"),
            }
            try:
                db.child(str(token+"/behavior")).push(data)
                config_service.set_config_robot_connect_true_status()
                return get_json_format(data, True)
            except:
                config_service.set_config_robot_connect_false_status()
                return get_json_format(data, False)
        except:
            config_service.set_config_robot_connect_false_status()
            return get_json_format(data, False)
    except:
        config_service.set_config_robot_connect_false_status()
        return get_json_format(data, False)

def insert_firebase_behavior_forgot_take_pill_data(behavior_id, token):
    try:
        firebase = pyrebase.initialize_app(connect_service.get_connect_firebase_real_time_database_kati_read())
        try:
            db = firebase.database()
            data = {
              "Notification_detail_thai": "ผู้ป่วยลืมรับประทานยา "+get_pills_thai_commonname_with_behavior_id(behavior_id),
              "Notification_detail_english": "Patient forgot to take a pill " + get_pills_english_commonname_with_behavior_id(behavior_id),
              "Notification_date": get_date_time_short_with_behavior_id(behavior_id),
              "Notification_date_with_format":  get_date_time_full_with_behavior_id(behavior_id),
              "Token": str(token),
              "Notification_visible_status": "1",
              "Token_Notification_visible_status": str(token+"_1"),
            }
            try:
                db.child(str(token+"/behavior")).push(data)
                config_service.set_config_robot_connect_true_status()
                return get_json_format(data, True)
            except:
                config_service.set_config_robot_connect_false_status()
                return get_json_format(data, False)
        except:
            config_service.set_config_robot_connect_false_status()
            return get_json_format(data, False)
    except:
        config_service.set_config_robot_connect_false_status()
        return get_json_format(data, False)

def insert_firebase_behavior_took_one_pill_data(behavior_id, token):
    try:
        firebase = pyrebase.initialize_app(connect_service.get_connect_firebase_real_time_database_kati_read())
        try:
            db = firebase.database()
            data = {
              "Notification_detail_thai": "ผู้ป่วยรับประทานยา "+get_one_pill_thai_commonname_with_behavior_id(behavior_id),
              "Notification_detail_english": "Patient took a pill " + get_one_pill_english_commonname_with_behavior_id(behavior_id),
              "Notification_date": get_date_time_short_with_behavior_id(behavior_id),
              "Notification_date_with_format":  get_date_time_full_with_behavior_id(behavior_id),
              "Token": str(token),
              "Notification_visible_status": "1",
              "Token_Notification_visible_status": str(token+"_1"),
            }
            try:
                db.child(str(token+"/behavior")).push(data)
                config_service.set_config_robot_connect_true_status()
                return get_json_format(data, True)
            except:
                config_service.set_config_robot_connect_false_status()
                return get_json_format(data, False)
        except:
            config_service.set_config_robot_connect_false_status()
            return get_json_format(data, False)
    except:
        config_service.set_config_robot_connect_false_status()
        return get_json_format(data, False)

def insert_behavior_forgot_take_one_pill_data(behavior_id,token):
    try:
        firebase = pyrebase.initialize_app(connect_service.get_connect_firebase_real_time_database_kati_read())
        try:
            db = firebase.database()
            data = {
              "Notification_detail_thai": "ผู้ป่วยลืมรับประทานยา "+get_one_pill_thai_commonname_with_behavior_id(behavior_id),
              "Notification_detail_english": "Patient forgot to take a pill " + get_one_pill_english_commonname_with_behavior_id(behavior_id),
              "Notification_date": get_date_time_short_with_behavior_id(behavior_id),
              "Notification_date_with_format":  get_date_time_full_with_behavior_id(behavior_id),
              "Token": str(token),
              "Notification_visible_status": "1",
              "Token_Notification_visible_status": str(token+"_1"),
            }
            try:
                db.child(str(token+"/behavior")).push(data)
                config_service.set_config_robot_connect_true_status()
                return get_json_format(data, True)
            except:
                config_service.set_config_robot_connect_false_status()
                return get_json_format(data, False)
        except:
            config_service.set_config_robot_connect_false_status()
            return get_json_format(data, False)
    except:
        config_service.set_config_robot_connect_false_status()
        return get_json_format(data, False)

def insert_firebase_behavior_come_but_no_take_pill_data(behavior_id, token):
    try:
        firebase = pyrebase.initialize_app(connect_service.get_connect_firebase_real_time_database_kati_read())
        try:
            db = firebase.database()
            data = {
              "Notification_detail_thai": "ผู้ป่วยมาหน้าเครื่องแต่ไม่ได้รับยา",
              "Notification_detail_english": "Patient Come to kati but no take pill.",
              "Notification_date": get_date_time_short_with_behavior_id(behavior_id),
              "Notification_date_with_format":  get_date_time_full_with_behavior_id(behavior_id),
              "Token": str(token),
              "Notification_visible_status": "1",
              "Token_Notification_visible_status": str(token+"_1"),
            }
            try:
                db.child(str(token+"/behavior")).push(data)
                config_service.set_config_robot_connect_true_status()
                return get_json_format(data, True)
            except:
                config_service.set_config_robot_connect_false_status()
                return get_json_format(data, False)
        except:
            config_service.set_config_robot_connect_false_status()
            return get_json_format(data, False)
    except:
        config_service.set_config_robot_connect_false_status()
        return get_json_format(data, False)


def sent_all_pill_out_of_stock(pill_id):
    pill_log_id = insert_pill_out_of_stock_message(pill_id)
    insert_pill_log_notification()
    if(check_outsider()):
        json_sent_firebase_pill_out_of_stock_notification = json.loads(sent_firebase_pill_out_of_stock_notification(pill_log_id))
        if(json_sent_firebase_pill_out_of_stock_notification['result']):
            pass
        else:
            insert_firebase_notification_sent_error_log(json_sent_firebase_pill_out_of_stock_notification['data'])
            for i in range(len(get_available_token_kati_read_dict())):
                json_insert_pill_out_of_stock_data = json.loads(insert_firebase_pill_out_of_stock_data(pill_log_id, get_available_token_kati_read_dict().get(i)[1]))
                if(json_insert_pill_out_of_stock_data['result']):
                    pass
                else:
                    insert_firebase_database_sent_error_log(json_insert_pill_out_of_stock_data['data'])

def sent_all_pill_almost_out_of_stock(pill_id):
    pill_log_id = insert_pill_almost_out_of_stock_message(pill_id)
    insert_pill_log_notification()
    if(check_outsider()):
        json_sent_firebase_pill_almost_out_of_stock_notification = json.loads(sent_firebase_pill_almost_out_of_stock_notification(pill_log_id))
        if(json_sent_firebase_pill_almost_out_of_stock_notification['result']):
            pass
        else:
            insert_firebase_notification_sent_error_log(json_sent_firebase_pill_almost_out_of_stock_notification['data'])
            for i in range(len(get_available_token_kati_read_dict())):
                json_insert_firebase_pill_almost_out_of_stock_data = json.loads(insert_firebase_pill_almost_out_of_stock_data(pill_log_id,get_available_token_kati_read_dict().get(i)[1]))
                if (json_insert_firebase_pill_almost_out_of_stock_data['result']):
                    pass
                else:
                    insert_firebase_database_sent_error_log(json_insert_firebase_pill_almost_out_of_stock_data['data'])
      
def sent_all_behavior_took_pill(schedule_id):
    behavior_id = insert_behavior_took_pill_message(schedule_id)
    insert_behavior_notification()
    if(check_outsider()):
        json_sent_firebase_behavior_took_pill_notification = json.loads(sent_firebase_behavior_took_pill_notification(behavior_id))
        if (json_sent_firebase_behavior_took_pill_notification['result']):
            pass
        else:
            insert_firebase_notification_sent_error_log(json_sent_firebase_behavior_took_pill_notification['data'])
            for i in range(len(get_available_token_kati_read_dict())):
                json_insert_firebase_behavior_took_pill_data = json.loads(insert_firebase_behavior_took_pill_data(behavior_id, get_available_token_kati_read_dict().get(i)[1]))
                if(json_insert_firebase_behavior_took_pill_data['result']):
                    pass
                else:
                    insert_firebase_database_sent_error_log(json_insert_firebase_behavior_took_pill_data['data'])
      
def sent_all_behavior_forgot_take_pill(schedule_id):
    behavior_id = insert_behavior_forgot_take_pill_message(schedule_id)
    insert_behavior_notification()
    if(check_outsider()):
        json_sent_firebase_behavior_forgot_take_pill_notification = json.loads(sent_firebase_behavior_forgot_take_pill_notification(behavior_id))
        if (json_sent_firebase_behavior_forgot_take_pill_notification['result']):
            pass
        else:
            insert_firebase_notification_sent_error_log(json_sent_firebase_behavior_forgot_take_pill_notification['data'])
            for i in range(len(get_available_token_kati_read_dict())):
                json_insert_firebase_behavior_forgot_take_pill_data = json.loads(insert_firebase_behavior_forgot_take_pill_data(behavior_id, get_available_token_kati_read_dict().get(i)[1]))
                if(json_insert_firebase_behavior_forgot_take_pill_data['result']):
                    pass
                else:
                    insert_firebase_database_sent_error_log(json_insert_firebase_behavior_forgot_take_pill_data['data'])

def sent_all_behavior_took_one_pill(pill_id):
    behavior_id = insert_behavior_took_one_pill_message(pill_id)
    insert_behavior_notification()
    if (check_outsider()):
        json_sent_firebase_behavior_took_one_pill_notification = json.loads(sent_firebase_behavior_took_one_pill_notification(behavior_id))
        if (json_sent_firebase_behavior_took_one_pill_notification['result']):
            pass
        else:
            insert_firebase_notification_sent_error_log(json_sent_firebase_behavior_took_one_pill_notification['data'])
            for i in range(len(get_available_token_kati_read_dict())):
                json_insert_firebase_behavior_took_one_pill_data = json.loads(insert_firebase_behavior_took_one_pill_data(behavior_id, get_available_token_kati_read_dict().get(i)[1]))
                if (json_insert_firebase_behavior_took_one_pill_data['result']):
                    pass
                else:
                    insert_firebase_database_sent_error_log(json_insert_firebase_behavior_took_one_pill_data['data'])

def sent_all_behavior_forgot_take_one_pill(pill_id):
    behavior_id = insert_behavior_forgot_take_one_pill_message(pill_id)
    insert_behavior_notification()
    if (check_outsider()):
        json_sent_firebase_behavior_forgot_take_one_pill_notification = json.loads(sent_firebase_behavior_forgot_take_one_pill_notification(behavior_id))
        if (json_sent_firebase_behavior_forgot_take_one_pill_notification['result']):
            pass
        else:
            insert_firebase_notification_sent_error_log(json_sent_firebase_behavior_forgot_take_one_pill_notification['data'])
            for i in range(len(get_available_token_kati_read_dict())):
                json_insert_behavior_forgot_take_one_pill_data = json.loads(insert_behavior_forgot_take_one_pill_data(behavior_id, get_available_token_kati_read_dict().get(i)[1]))
                if (json_insert_behavior_forgot_take_one_pill_data['result']):
                    pass
                else:
                    insert_firebase_database_sent_error_log(json_insert_behavior_forgot_take_one_pill_data['data'])

def sent_all_behavior_come_but_no_take_pill():
    behavior_id = insert_behavior_come_but_no_take_pill_message()
    insert_behavior_notification()
    if (check_outsider()):
        json_sent_firebase_behavior_come_but_no_take_pill_notification = json.loads(sent_firebase_behavior_come_but_no_take_pill_notification(behavior_id))
        if (json_sent_firebase_behavior_come_but_no_take_pill_notification['result']):
            pass
        else:
            insert_firebase_notification_sent_error_log(json_sent_firebase_behavior_come_but_no_take_pill_notification['data'])
            for i in range(len(get_available_token_kati_read_dict())):
                json_insert_firebase_behavior_come_but_no_take_pill_data = json.loads(insert_firebase_behavior_come_but_no_take_pill_data(behavior_id, get_available_token_kati_read_dict().get(i)[1]))
                if (json_insert_firebase_behavior_come_but_no_take_pill_data['result']):
                    pass
                else:
                    insert_firebase_database_sent_error_log(json_insert_firebase_behavior_come_but_no_take_pill_data['data'])

def sent_all_memo_message(message):
    if(check_outsider()):
        json_sent_firebase_memo_message_notification = json.loads(sent_firebase_memo_message_notification(message))
        if (json_sent_firebase_memo_message_notification['result']):
            pass
        else:
            insert_firebase_notification_sent_error_log(json_sent_firebase_memo_message_notification['data'])

def sent_all_schedule_message():
    if(check_outsider()):
        json_sent_firebase_schedule_message_notification = json.loads(sent_firebase_schedule_message_notification())
        if (json_sent_firebase_schedule_message_notification['result']):
            pass
        else:
            insert_firebase_notification_sent_error_log(json_sent_firebase_schedule_message_notification['data'])

def sent_all_data_error_data_again():
    firebase_notification_sent_error_log_dict = get_firebase_notification_sent_error_log_dict()
    if firebase_notification_sent_error_log_dict is not None:
        for i in range(len(firebase_notification_sent_error_log_dict)):
            if(sent_firebase_notification_with_json(firebase_notification_sent_error_log_dict.get(i)[1])):
                delete_firebase_error_log(firebase_notification_sent_error_log_dict.get(i)[0])
    firebase_database_sent_error_log_dict = get_firebase_database_sent_error_log_dict()
    if firebase_database_sent_error_log_dict is not None:
        for i in range(len(firebase_database_sent_error_log_dict)):
            if(insert_firebase_database_with_json(firebase_database_sent_error_log_dict.get(i)[1])):
                delete_firebase_error_log(firebase_database_sent_error_log_dict.get(i)[0])

def sent_all_pill_out_of_stock_in_background(pill_id):
    sent_pill_out_of_stock_thread = threading.Thread(target=sent_all_pill_out_of_stock , args=(pill_id,))
    sent_pill_out_of_stock_thread.start()

def sent_all_pill_almost_out_of_stock_in_background(pill_id):
    sent_pill_almost_out_of_stock_thread = threading.Thread(target=sent_all_pill_almost_out_of_stock , args=(pill_id,))
    sent_pill_almost_out_of_stock_thread.start()

def sent_all_behavior_took_pill_in_background(schedule_id):
    sent_behavior_took_pill_thread = threading.Thread(target=sent_all_behavior_took_pill , args=(schedule_id,))
    sent_behavior_took_pill_thread.start()

def sent_all_behavior_forgot_take_pill_in_background(schedule_id):
    sent_behavior_forgot_take_pill_thread = threading.Thread(target=sent_all_behavior_forgot_take_pill , args=(schedule_id,))
    sent_behavior_forgot_take_pill_thread.start()

def sent_all_behavior_took_one_pill_in_background(pill_id):
    sent_behavior_took_one_pill_thread = threading.Thread(target=sent_all_behavior_took_one_pill , args=(pill_id,))
    sent_behavior_took_one_pill_thread.start()

def sent_all_behavior_forgot_take_one_pill_in_background(pill_id):
    sent_behavior_forgot_take_one_pill_thread = threading.Thread(target=sent_all_behavior_forgot_take_one_pill , args=(pill_id,))
    sent_behavior_forgot_take_one_pill_thread.start()

def sent_all_behavior_come_but_no_take_pill_in_background():
    sent_behavior_come_but_no_take_pill_thread = threading.Thread(target=sent_all_behavior_come_but_no_take_pill)
    sent_behavior_come_but_no_take_pill_thread.start()
    
def sent_all_memo_message_in_background(message):
    sent_all_memo_message_thread = threading.Thread(target=sent_all_memo_message , args=(message,))
    sent_all_memo_message_thread.start()

def sent_all_schedule_message_in_background():
    sent_all_schedule_message_thread = threading.Thread(target=sent_all_schedule_message)
    sent_all_schedule_message_thread.start()

def sent_all_data_error_data_again_in_background():
    sent_data_error_data_again_thread = threading.Thread(target=sent_all_data_error_data_again)
    sent_data_error_data_again_thread.start()

class Sent_all_data_error_Thread(core.QThread):
    def run(self):
        while True:
            sent_all_data_error_data_again_in_background()
            time.sleep(15)


