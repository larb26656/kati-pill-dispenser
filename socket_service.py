import socket
import connect_service
from pprint import pprint
from flask import Flask, jsonify, request, abort
from time import strftime
import pymysql
import text_to_speech_service
import time
import stepmotor_service
from concurrent.futures import ThreadPoolExecutor

calculator_enable_status = False
executor = ThreadPoolExecutor(1)
app=Flask(__name__)


@app.route('/sent', methods=['POST'])
def search_data():
        query = str(request.form['text'])
        print(query)
        if(get_kati_status()=="free"):
                return get_conversation(query)
        else:
                return "(busy)"

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
                    text=text_to_speech_service.get_and_play_with_delay_time_ans()
                    set_kati_face_status("normal")
                    return text
                elif(r['Conversation_type'] == "date"):
                    set_kati_face_status("talk")
                    text=text_to_speech_service.get_and_play_with_delay_date_ans()
                    set_kati_face_status("normal")
                    return text
                elif(r['Conversation_type'] == "weather"):
                    set_kati_face_status("talk")
                    text = text_to_speech_service.get_and_play_with_delay_weather_ans()
                    set_kati_face_status("normal")
                    return text
                elif(r['Conversation_type'] == "calculator"):
                    set_kati_face_status("talk")
                    text = text_to_speech_service.get_and_play_with_delay_calculator_enable_ans()
                    set_kati_face_status("normal")
                    executor.submit(calculator_enable)
                    return text
                elif(r['Conversation_type'] == "pill_dispenser"):
                    if(stepmotor_service.check_pil_exisit_and_num_of_pill(str(r['Pill_id']))):
                        text = "found"
                        set_kati_status("pill_dispenser" + str(r['Pill_id']))
                    else:
                        set_kati_face_status("talk")
                        text = text_to_speech_service.get_and_play_with_delay_pill_not_found_ans()
                        set_kati_face_status("normal")
                    return text
        else:
            set_kati_face_status("talk")
            text = text_to_speech_service.get_and_play_with_delay_command_not_found()
            set_kati_face_status("normal")
            return text
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

def calculator_enable():
    global calculator_enable_status
    calculator_enable_status = True
    for num in range(1, 30):
        if(calculator_enable_status):
            pass
        else:
            return None
        time.sleep(1)
    calculator_enable_status = False

def calculator(quest):
    global calculator_enable_status
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
        calculator_enable_status = False
        set_kati_face_status("talk")
        text = text_to_speech_service.get_and_play_with_delay_number_ans(str(eval(question)))
        set_kati_face_status("normal")
        return text

    except SyntaxError:
        set_kati_face_status("talk")
        text = text_to_speech_service.get_and_play_with_delay_calculator_disable_ans()
        set_kati_face_status("normal")
        calculator_enable_status = False
        return text

app.run(debug=True, host='0.0.0.0')
