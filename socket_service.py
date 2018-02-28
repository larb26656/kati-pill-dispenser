import socket
import connect_service
from flask import Flask, jsonify, request, abort
import pymysql
import text_to_speech_service
import time
import stepmotor_service
import setting_service
from concurrent.futures import ThreadPoolExecutor
import language_service
import json
from logging_service import Socket_log

calculator_enable_status = False
memo_enable_status = False
executor = ThreadPoolExecutor(1)
app=Flask(__name__)


@app.route('/sent', methods=['POST'])
def search_data():
        query = str(request.form['text'])
        print(query)
        if(get_kati_status()=="free"):
                return get_conversation(query)
        else:
                return return_json_format(language_service.get_kati_is_busy_ans_text,"busy")

@app.route('/get_ip')
def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

def get_conversation(text):
    global scheldule_id,scheldule_time,scheldule_time_diff,calculator_enable_status,memo_enable_status
    conn = connect_service.get_connect_sql()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM conversation WHERE Conversation_quiz = '"+text+"'")
    if(calculator_enable_status == True and memo_enable_status == False):
        return calculator(text)
    elif(calculator_enable_status == False and memo_enable_status == True):
        return memo(text)
    elif(calculator_enable_status == True and memo_enable_status == True):
        calculator_enable_status = False
        memo_enable_status = False
        return return_json_format(language_service.get_error_ans_text(),"error")
    else:
        if(cur.rowcount > 0):
            for r in cur:
                if(r['Conversation_type'] == "time"):
                    set_kati_face_status("talk")
                    text=text_to_speech_service.get_and_play_with_delay_time_ans()
                    set_kati_face_status("normal")
                    Socket_log.logger.info("Receive HTTP time request.")
                    return return_json_format(text,"time")
                elif(r['Conversation_type'] == "date"):
                    set_kati_face_status("talk")
                    text=text_to_speech_service.get_and_play_with_delay_date_ans()
                    set_kati_face_status("normal")
                    Socket_log.logger.info("Receive HTTP date request.")
                    return return_json_format(text,"date")
                elif(r['Conversation_type'] == "weather"):
                    set_kati_face_status("talk")
                    text = text_to_speech_service.get_and_play_with_delay_weather_ans()
                    set_kati_face_status("normal")
                    Socket_log.logger.info("Receive HTTP weather request.")
                    return return_json_format(text,"weather")
                elif(r['Conversation_type'] == "calculator"):
                    set_kati_face_status("talk")
                    text = text_to_speech_service.get_and_play_with_delay_calculator_enable_ans()
                    set_kati_face_status("normal")
                    executor.submit(calculator_enable)
                    Socket_log.logger.info("Receive HTTP calculator request.")
                    return return_json_format(text,"calculator")
                elif(r['Conversation_type'] == "pill_dispenser"):
                    if(stepmotor_service.check_pil_exisit_and_num_of_pill(str(r['Pill_id']))):
                        text = language_service.get_and_play_with_delay_pill_found_ans_text()
                        setting_service.set_pill_dispenser_true_status(str(r['Pill_id']))
                    else:
                        set_kati_face_status("talk")
                        text = text_to_speech_service.get_and_play_with_delay_pill_not_found_ans()
                        set_kati_face_status("normal")
                    Socket_log.logger.info("Receive HTTP pill dispenser request.")
                    return return_json_format(text,"pill_dispenser")
                elif(r['Conversation_type'] == "memo"):
                    set_kati_face_status("talk")
                    text = text_to_speech_service.get_and_play_with_delay_memo_enable_ans()
                    set_kati_face_status("normal")
                    executor.submit(memo_enable)
                    Socket_log.logger.info("Receive HTTP memo request.")
                    return return_json_format(text,"memo")
        else:
            set_kati_face_status("talk")
            text = text_to_speech_service.get_and_play_with_delay_command_not_found_ans()
            set_kati_face_status("normal")
            Socket_log.logger.warning("Receive HTTP unknown request.")
            return return_json_format(text,"command_not_found")
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

def memo_enable():
    global memo_enable_status
    memo_enable_status = True
    for num in range(1, 30):
        if(memo_enable_status):
            pass
        else:
            return None
        time.sleep(1)
    memo_enable_status = False

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
        return return_json_format(text,"calculator_success")

    except SyntaxError:
        set_kati_face_status("talk")
        text = text_to_speech_service.get_and_play_with_delay_calculator_disable_ans()
        set_kati_face_status("normal")
        calculator_enable_status = False
        return return_json_format(text,"calculator_error")

def memo(text):
    global memo_enable_status
    memo_enable_status = False
    return return_json_format(text,"memo_save")

def return_json_format(text,type):
    return json.dumps({'text': text, 'type': type}, ensure_ascii=False)

def run_socket_sever():
    app.run(debug=True, host='0.0.0.0')
