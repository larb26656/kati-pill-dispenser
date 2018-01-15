import pymysql
import connect_service
from pyfcm import FCMNotification
import pyrebase
import json
from time import localtime, strftime
from weather import Weather
import time
import threading

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
    token_list = []
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `member` WHERE `Member_visiblestatus` = '1'")
    for r in cur:
        return str(r['Member_id'])
    cur.close()
    conn.close()
    
def get_available_token_list():
    token_list = []
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `outsider` WHERE `Outsider_visiblestatus` = '1'")
    for r in cur:
        token_list.append(str(r['Outsider_token']))
    return(token_list)
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

def get_pill_english_commonname_with_pill_id(pill_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `pill` WHERE Pill_id = '"+str(pill_id)+"'")
    for r in cur:
        return str(r['Pill_commonname_english'])
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

def check_outsider():
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `outsider` WHERE `Outsider_visiblestatus` = '1'")
    numrows = int(cur.rowcount)
    if(numrows > 1):
        return True
    else:
        return False
    cur.close()
    conn.close()

def update_behavior_sync_status(behavior_notification_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("UPDATE behavior_notification SET Sync_status='1' WHERE Behavior_notification_id="+str(behavior_notification_id))
    conn.commit()
    cur.close()
    conn.close()

def sent_firebase_pill_out_of_stock_notification(pill_id):
    data_message = {
        "Title": "<Pill>",
        "Body_thai": "ยา " + get_pill_thai_commonname_with_pill_id(pill_id)+" หมด",
        "Body_english":  get_pill_english_commonname_with_pill_id(pill_id)+" is out of stock",
    }
    push_service = connect_service.get_connect_firebase_cloud_message()
    registration_ids = get_available_token_list()
    try:
        push_service.multiple_devices_data_message(registration_ids=registration_ids,data_message=data_message)
    except:
        result = "network error."
    
def sent_firebase_pill_almost_out_of_stock_notification(pill_id):
    data_message = {
        "Title": "<Pill>",
        "Body_thai": "ยา " + get_pill_thai_commonname_with_pill_id(pill_id)+" ใกล้หมด",
        "Body_english":  get_pill_english_commonname_with_pill_id(pill_id)+" is almost out of stock",
    }
    push_service = connect_service.get_connect_firebase_cloud_message()
    registration_ids = get_available_token_list()
    result = push_service.multiple_devices_data_message(registration_ids=registration_ids, data_message=data_message)
    print (result)
    
def sent_firebase_behavior_took_pill_notification(schedule_id):
    data_message = {
        "Title": "<Behavior>",
        "Body_thai": "ผู้ป่วยรับประทานยา "+get_pills_thai_commonname_with_schedule_id(schedule_id),
        "Body_english": "Patient took a pill " + get_pills_english_commonname_with_schedule_id(schedule_id),
    }
    push_service = connect_service.get_connect_firebase_cloud_message()
    registration_ids = get_available_token_list()
    result = push_service.multiple_devices_data_message(registration_ids=registration_ids, data_message=data_message)
    print (result)

def sent_firebase_behavior_forgot_take_pill_notification(schedule_id):
    data_message = {
        "Title": "<Behavior>",
        "Body_thai": "ผู้ป่วยลืมรับประทานยา "+get_pills_thai_commonname_with_schedule_id(schedule_id),
        "Body_english": "Patient forgot to take a pill " + get_pills_english_commonname_with_schedule_id(schedule_id),
    }
    push_service = connect_service.get_connect_firebase_cloud_message()
    registration_ids = get_available_token_list()
    result = push_service.multiple_devices_data_message(registration_ids=registration_ids, data_message=data_message)
    print (result)
    
def sent_firebase_message_notification(message):
    data_message = {
        "Title": "<Message>",
        "Body": str(message),
    }
    push_service = connect_service.get_connect_firebase_cloud_message()
    registration_ids = get_available_token_list()
    result = push_service.multiple_devices_data_message(registration_ids=registration_ids, data_message=data_message)
    print (result)
    
def insert_pill_out_of_stock_message(pill_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("INSERT INTO pill_log(Pill_log_type,Pill_log_datetime,Pill_id) value('outofstock',NOW(),'"+str(pill_id)+"')")
    conn.commit()
    cur.close()
    conn.close()

def insert_pill_almost_out_of_stock_message(pill_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("INSERT INTO pill_log(Pill_log_type,Pill_log_datetime,Pill_id) value('almostoutofstock',NOW(),'"+str(pill_id)+"')")
    conn.commit()
    cur.close()
    conn.close()
    
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
    cur.execute("INSERT INTO behavior(Behavior_type,Behavior_datetime,Schedule_id) value('tookpill',NOW(),'"+str(schedule_id)+"')")
    conn.commit()
    cur.close()
    conn.close()

def insert_behavior_forgot_take_pill_message(schedule_id):
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("INSERT INTO behavior(Behavior_type,Behavior_datetime,Schedule_id) value('forgottakepill',NOW(),'"+str(schedule_id)+"')")
    conn.commit()
    cur.close()
    conn.close()

def insert_behavior_notification():
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("INSERT INTO behavior_notification(Behavior_id,Member_id,Msg_status) values('"+get_last_behavior_id()+"','"+get_available_member_id()+"','1')")
    conn.commit()
    cur.close()
    conn.close()
    
def insert_pill_out_of_stock_data(pill_id,token):
    firebase = pyrebase.initialize_app(connect_service.get_connect_firebase_real_time_database())
    db = firebase.database()
    data ={
      "Notification_detail_thai": "ยา " + get_pill_thai_commonname_with_pill_id(pill_id)+" หมด",
      "Notification_detail_english": get_pill_english_commonname_with_pill_id(pill_id)+" is out of stock",
      "Notification_date": get_date_time_short(),
      "Notification_date_with_format":  get_date_time_full(),
      "Token": str(token),
      "Notification_visible_status": "1",
      "Token_Notification_visible_status": str(token+"_1"),
        }
    print(db.child(str(token+"/pill")).push(data))

def insert_pill_almost_out_of_stock_data(pill_id,token):
    firebase = pyrebase.initialize_app(connect_service.get_connect_firebase_real_time_database())
    db = firebase.database()
    data ={
      "Notification_detail_thai": "ยา " + get_pill_thai_commonname_with_pill_id(pill_id)+" ใกล้หมด",
      "Notification_detail_english": get_pill_english_commonname_with_pill_id(pill_id)+" is almost out of stock",
      "Notification_date": get_date_time_short(),
      "Notification_date_with_format":  get_date_time_full(),
      "Token": str(token),
      "Notification_visible_status": "1",
      "Token_Notification_visible_status": str(token+"_1"),
        }
    print(db.child(str(token+"/pill")).push(data))
    
def insert_behavior_took_pill_data(schedule_id,token):
    firebase = pyrebase.initialize_app(connect_service.get_connect_firebase_real_time_database())
    db = firebase.database()
    data ={
      "Notification_detail_thai": "ผู้ป่วยรับประทานยา "+get_pills_thai_commonname_with_schedule_id(schedule_id),
      "Notification_detail_english": "Patient took a pill " + get_pills_english_commonname_with_schedule_id(schedule_id),
      "Notification_date": get_date_time_short(),
      "Notification_date_with_format":  get_date_time_full(),
      "Token": str(token),
      "Notification_visible_status": "1",
      "Token_Notification_visible_status": str(token+"_1"),
        }
    print(db.child(str(token+"/behavior")).push(data))

def insert_behavior_forgot_take_pill_data(schedule_id,token):
    firebase = pyrebase.initialize_app(connect_service.get_connect_firebase_real_time_database())
    db = firebase.database()
    data ={
      "Notification_detail_thai": "ผู้ป่วยลืมรับประทานยา "+get_pills_thai_commonname_with_schedule_id(schedule_id),
      "Notification_detail_english": "Patient forgot to take a pill " + get_pills_english_commonname_with_schedule_id(schedule_id),
      "Notification_date": get_date_time_short(),
      "Notification_date_with_format":  get_date_time_full(),
      "Token": str(token),
      "Notification_visible_status": "1",
      "Token_Notification_visible_status": str(token+"_1"),
        }
    print(db.child(str(token+"/behavior")).push(data))

def sent_all_pill_out_of_stock(pill_id):
    insert_pill_out_of_stock_message(pill_id)
    insert_pill_log_notification()
    if(check_outsider()):
        sent_firebase_pill_out_of_stock_notification(pill_id)
        for token in get_available_token_list():
            insert_pill_out_of_stock_data(pill_id,token)
        
def sent_all_pill_almost_out_of_stock(pill_id):
    insert_pill_almost_out_of_stock_message(pill_id)
    insert_pill_log_notification()
    if(check_outsider()):
        sent_firebase_pill_almost_out_of_stock_notification(pill_id)
        for token in get_available_token_list():  
          insert_pill_almost_out_of_stock_data(pill_id,token)
      
def sent_all_behavior_took_pill(schedule_id):
    insert_behavior_took_pill_message(schedule_id)
    insert_behavior_notification()
    if(check_outsider()):
        sent_firebase_behavior_took_pill_notification(schedule_id)
        for token in get_available_token_list():  
          insert_behavior_took_pill_data(schedule_id,token)
      
def sent_all_behavior_forgot_take_pill(schedule_id):
    insert_behavior_forgot_take_pill_message(schedule_id)
    insert_behavior_notification()
    if(check_outsider()):
        sent_firebase_behavior_forgot_take_pill_notification(schedule_id)
        for token in get_available_token_list():  
          insert_behavior_forgot_take_pill_data(schedule_id,token)

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
    
def sent_firebase_message_notification_in_background(message):
    sent_firebase_message_notification_thread = threading.Thread(target=sent_firebase_message_notification , args=(message,))
    sent_firebase_message_notification_thread.start()

sent_firebase_pill_out_of_stock_notification(1)
#sent_all_behavior_forgot_take_pill_in_background(13)
#sent_firebase_message_notification_in_background("ทดสอบแจ้งเเือนข้อความ")