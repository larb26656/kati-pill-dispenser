import sys
import pymysql
import connect_service
from time import strftime
import datetime

def get_lang():
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM robot_setting ")
    for r in cur:
        return str(r['Robot_lang'])
    cur.close()
    conn.close()

def get_lang_short():
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM robot_setting ")
    for r in cur:
        if(str(r['Robot_lang'])=="thai"):
            return "th"
        elif(str(r['Robot_lang'])=="english"):
            return "en"
    cur.close()
    conn.close()

def get_provinces_name_english():
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `robot_setting` INNER JOIN provinces ON robot_setting.Provinces_id = provinces.Provinces_id")
    for r in cur:
        return str(r['Provinces_name_english'])
    cur.close()
    conn.close()

def get_month_thai_text(num_of_month):
    if(int(num_of_month)==1):
        return "มกราคม"
    elif(int(num_of_month)==2):
        return "กุมภาพันธ์"
    elif(int(num_of_month)==3):
        return "มีนาคม"
    elif(int(num_of_month)==4):
        return "เมษายน"
    elif(int(num_of_month)==5):
        return "พฤษภาคม"
    elif(int(num_of_month)==6):
        return "มิถุนายน"
    elif(int(num_of_month)==7):
        return "กรกฎาคม"
    elif(int(num_of_month)==8):
        return "สิงหาคม"
    elif(int(num_of_month)==9):
        return "กันยายน"
    elif(int(num_of_month)==10):
        return "ตุลาคม"
    elif(int(num_of_month)==11):
        return "พฤศจิกายน"
    elif(int(num_of_month)==12):
        return "ธันวาคม"
    else:
        return "Error"

def get_month_english_text(num_of_month):
    if (int(num_of_month) == 1):
        return "January"
    elif (int(num_of_month) == 2):
        return "February"
    elif (int(num_of_month) == 3):
        return "March"
    elif (int(num_of_month) == 4):
        return "April"
    elif (int(num_of_month) == 5):
        return "May"
    elif (int(num_of_month) == 6):
        return "June"
    elif (int(num_of_month) == 7):
        return "July"
    elif (int(num_of_month) == 8):
        return "August"
    elif (int(num_of_month) == 9):
        return "September"
    elif (int(num_of_month) == 10):
        return "October"
    elif (int(num_of_month) == 11):
        return "November"
    elif (int(num_of_month) == 12):
        return "December"
    else:
        return "Error"

def get_year_thai_format(num_of_year):
    return str(int(num_of_year)+543)

def get_error_ans_text():
    if (get_lang() == "thai"):
        return "เกิดข้อผิดพลาด"
    elif (get_lang() == "english"):
        return "Error."

def get_kati_is_busy_ans_text():
    if (get_lang() == "thai"):
        return "ดิฉันยังไม่พร้อมรับคำสั่งกรุณาลองอีกครั้งค่ะ"
    elif (get_lang() == "english"):
        return "I'm busy."

def get_time_ans_text():
    if(get_lang()=="thai"):
        return "ขณะนี้เวลา "+strftime("%H:%M:%S")
    elif(get_lang()=="english"):
        return "it's "+strftime("%H:%M:%S")+"."

def get_date_ans_text():
    if(get_lang()=="thai"):
        return "วันที่ "+strftime("%d")+" "+get_month_thai_text(strftime("%m"))+" "+get_year_thai_format(strftime("%Y"))
    elif(get_lang()=="english"):
        return "Today is " + strftime("%d") + " " + get_month_english_text(strftime("%m")) + " " + strftime("%Y")+"."

def get_temperature_ans_text(low_temperature,high_temperature):
    if(get_lang()=="thai"):
        return "สภาพอากาศวันนี้มีอุณหภูมิต่ำสุดคือ "+low_temperature+"องศาเซลเซียส และมีอุณหภูมิสูงสุดคือ "+high_temperature+" องศาเซลเซียส"
    elif(get_lang()=="english"):
        return "Today weather have low temperature is "+low_temperature+" celsius and high temperature is "+high_temperature+" celsius."

def get_and_play_with_delay_command_not_found_ans_text():
    if (get_lang() == "thai"):
        return "ขอโทษค่ะดิฉันไม่เข้าใจกรุณาลองอีกครั้ง"
    elif (get_lang() == "english"):
        return "Sorry i can't understand please try again."

def get_and_play_with_delay_pill_not_found_ans_text():
    if(get_lang()=="thai"):
        return "ไม่พบยาในระบบหรือในช่องจ่ายยา"
    elif(get_lang()=="english"):
        return "Not found pill in system or slot."

def get_and_play_with_delay_pill_found_ans_text():
    if(get_lang()=="thai"):
        return "พบยาในระบบกรุณามารับยาด้วยค่ะ"
    elif(get_lang()=="english"):
        return "Found pill in system please come to receive pill."

def get_and_play_with_delay_calculator_enable_ans_text():
    if (get_lang() == "thai"):
        return "กรุณาพูดคำถามคณิตศาสตร์ที่ต้องการให้ดิฉันคำนวณ"
    elif (get_lang() == "english"):
        return "Please talk math quiz do you want to calculator."

def get_and_play_with_delay_calculator_disable_ans_text():
    if (get_lang() == "thai"):
        return "รูปแบบคำถามคณิตศาสตร์ผิดพลาดกรุณาลองอีกครั้ง"
    elif (get_lang() == "english"):
        return "Error math quiz format please try again."

def get_and_play_with_delay_memo_enable_ans_text():
    if (get_lang() == "thai"):
        return "กรุณาพูดข้อความที่ต้องการแจ้งเตือน"
    elif (get_lang() == "english"):
        return "Please talk text do you want to notification."