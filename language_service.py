import sys
import pymysql
from time import strftime
import datetime

def get_lang():
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='kati',charset='utf8')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM robot_setting ")
    for r in cur:
        return str(r['Robot_lang'])
    cur.close()
    conn.close()

def get_lang_short():
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='kati',charset='utf8')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM robot_setting ")
    for r in cur:
        if(str(r['Robot_lang'])=="thai"):
            return "th"
        elif(str(r['Robot_lang'])=="english"):
            return "en"
    cur.close()
    conn.close()

def get_time_ans_text():
    if(get_lang()=="thai"):
        return "ขณะนี้เวลา "+strftime("%H:%M:%S")
    else:
        return "It's "+strftime("%H:%M:%S")+"."

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

def get_time_ans_text():
    if(get_lang()=="thai"):
        return "ขณะนี้เวลา "+strftime("%H:%M:%S")
    elif(get_lang()=="english"):
        return "it's "+strftime("%H:%M:%S")

def get_date_ans_text():
    if(get_lang()=="thai"):
        return "วันที่ "+strftime("%d")+" "+get_month_thai_text(strftime("%m"))+" "+get_year_thai_format(strftime("%Y"))
    elif(get_lang()=="english"):
        return "Today is " + strftime("%d") + " " + get_month_english_text(strftime("%m")) + " " + strftime("%Y")