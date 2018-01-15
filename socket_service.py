import socket
import connect_service
from pprint import pprint
from flask import Flask, jsonify, request, abort
from time import strftime
import pymysql
from weather import Weather
import text_to_speech_service
import time
from concurrent.futures import ThreadPoolExecutor

calculator_enable_status = False
executor = ThreadPoolExecutor(1)
app=Flask(__name__)


@app.route('/sent', methods=['GET'])
def search_data():
        query = request.args.get("text")
        print(query)
        if(get_kati_status()=="free"):
                return get_conversation(query)
        else:
                return "kati is busy"

@app.route('/get_ip')
def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

def get_conversation(text):
    global scheldule_id,scheldule_time,scheldule_time_diff
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM conversation WHERE Conversation_quiz = '"+text+"'")
    if(calculator_enable_status):
        return calculator(text)
    else:
        if(cur.rowcount > 0):
            for r in cur:
                if(r['Conversation_type'] == "time"):
                    set_kati_face_status("talk")
                    text_to_speech_service.set_time_ans()
                    text_to_speech_service.play_with_delay()
                    set_kati_face_status("normal")
                    return "time"
                elif(r['Conversation_type'] == "date"):
                    set_kati_face_status("talk")
                    text_to_speech_service.set_date_ans()
                    text_to_speech_service.play_with_delay()
                    set_kati_face_status("normal")
                    return "date"
                elif(r['Conversation_type'] == "weather"):
                    weather = Weather()
                    location = weather.lookup_by_location(get_provinces_name_english())
                    condition = location.condition()
                    forecasts = location.forecast()
                    return str("อุณหภูมิต่ำสุด "+str(convert_fahrenheit_to_celsius(forecasts[0].low()))+" อุณหภูมิสูงสุด "+str(convert_fahrenheit_to_celsius(forecasts[0].high())))
                elif(r['Conversation_type'] == "calculator"):
                    executor.submit(calculator_enable)
                    return "cal enable"
        else:
            set_kati_face_status("talk")
            text_to_speech_service.set_command_not_found()
            text_to_speech_service.play_with_delay()
            set_kati_face_status("normal")
            return "not found"
        cur.close()
        conn.close()
        


def set_kati_status(text):
        f = open('data/kati_status.txt','w',encoding='utf-8')
        f.write(text)
        f.close
        
def get_kati_status():
        f = open('data/kati_status.txt','r',encoding='utf-8')
        data = f.read()
        return data
        f.close()
        
def set_kati_face_status(text):
        f = open('data/kati_face_status.txt','w',encoding='utf-8')
        f.write(text)
        f.close
        
def get_kati_face_status():
        f = open('data/kati_face_status.txt','r',encoding='utf-8')
        data = f.read()
        return data
        f.close()

def get_provinces_name_english():
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM `robot_setting` INNER JOIN provinces ON robot_setting.Provinces_id = provinces.Provinces_id")
    for r in cur:
        return str(r['Provinces_name_english'])
    cur.close()
    conn.close()

def convert_fahrenheit_to_celsius(fahrenheit):
    return str(round((int(fahrenheit)-32)/2));

def calculator_enable():
    global calculator_enable_status
    calculator_enable_status = True
    time.sleep(30)
    calculator_enable_status = False

def calculator(quest):
    question = str(quest)
    question = question.replace("บวก","+")
    question = question.replace("ลบ","-")
    question = question.replace("คูณ","*")
    question = question.replace("หาร","/")
    question = question.replace("plus","+")
    question = question.replace("minus","-")
    question = question.replace("multiply","*")
    question = question.replace("divide","/")
    try:
        return str(eval(question))
    except SyntaxError:
        return SyntaxError

app.run(debug=True, host='0.0.0.0')
