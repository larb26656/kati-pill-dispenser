from pygame import mixer
import pygame
import pymysql
from gtts import gTTS
import time
import language_service
from langdetect import detect
from time import strftime
from weather import Weather
import os

mixer.init()

def get_directory(file_name):
    return str("voice_sound/"+language_service.get_lang()+"/"+file_name)

def get_directory_with_set_language(file_name,language):
    return str("voice_sound/"+language+"/"+file_name)

def convert_fahrenheit_to_celsius(fahrenheit):
    return str(round((int(fahrenheit)-32)/2));

def play():
    mixer.music.play()
    
def play_with_delay():
    mixer.music.play()
    while mixer.music.get_busy():
        pass
    
def play_loop():
    mixer.music.play(loops = -1)
    
def stop():
    mixer.music.stop()

def set_msg_pill_alarm():
    mixer.music.load(get_directory('pill_alarm.mp3'))
    
def set_msg_put_glass_far_alarm():
    mixer.music.load(get_directory('put_glass_far_alarm.mp3'))
    
def set_msg_pill_dispensing_alarm():
    mixer.music.load(get_directory('pill_dispensing_alarm.mp3'))
    
def set_msg_put_glass_near_alarm():
    mixer.music.load(get_directory('put_glass_near_alarm.mp3'))
    
def set_msg_put_glass_far_after_take_pill_alarm():
    mixer.music.load(get_directory('put_glass_far_after_take_pill_alarm.mp3'))

def set_msg_pill_found_alarm():
    mixer.music.load(get_directory('pill_found_alarm.mp3'))
    
def set_custom_msg(text_to_talk):
    language=detect(text_to_talk)
    if(language=="th"):
        language_directory="thai"
    else:
        language_directory="english"
    tts = gTTS(text=text_to_talk,lang=language)
    tts.save(get_directory_with_set_language('custom_msg_temp.mp3',language_directory))
    mixer.music.load(get_directory_with_set_language('custom_msg_temp.mp3',language_directory))

def set_custom_msg_with_filename(text_to_talk,filename):
    language=detect(text_to_talk)
    if(language=="th"):
        language_directory="thai"
    else:
        language_directory="english"
    tts = gTTS(text=text_to_talk,lang=language)
    tts.save(get_directory_with_set_language(filename+'.mp3',language_directory))
    mixer.music.load(get_directory_with_set_language(filename+'.mp3',language_directory))

def get_and_play_with_delay_command_not_found():
    mixer.music.load(get_directory('comand_not_found_ans.mp3'))
    if (language_service.get_lang_short() == "th"):
        text = "ขอโทษค่ะดิฉันไม่เข้าใจกรุณาลองอีกครั้ง"
    elif (language_service.get_lang_short() == "en"):
        text = "Sorry i can't understand please try again."
    play_with_delay()
    mixer.music.load(get_directory('temp_file.mp3'))
    return text

def get_and_play_with_delay_pill_not_found_ans():
    mixer.music.load(get_directory('pill_not_found_ans.mp3'))
    if(language_service.get_lang_short()=="th"):
        text="ไม่พบยาในระบบหรือในช่องจ่ายยา"
    elif(language_service.get_lang_short()=="en"):
        text="Not found pill in system or slot."
    play_with_delay()
    mixer.music.load(get_directory('temp_file.mp3'))
    return text

def get_and_play_with_delay_calculator_enable_ans():
    mixer.music.load(get_directory('calculator_enable_ans.mp3'))
    if (language_service.get_lang_short() == "th"):
        text = "กรุณาพูดคำถามคณิตศาสตร์ที่ต้องการให้ดิฉันคำนวณ"
    elif (language_service.get_lang_short() == "en"):
        text = "Please talk math quiz do you want to calculator."
    play_with_delay()
    mixer.music.load(get_directory('temp_file.mp3'))
    return text

def get_and_play_with_delay_calculator_disable_ans():
    mixer.music.load(get_directory('calculator_disable_ans.mp3'))
    if (language_service.get_lang_short() == "th"):
        text = "รูปแบบคำถามคณิตศาสตร์ผิดพลาดกรุณาลองอีกครั้ง"
    elif (language_service.get_lang_short() == "en"):
        text = "Error math quiz format please try again."
    play_with_delay()
    mixer.music.load(get_directory('temp_file.mp3'))
    return text

def get_and_play_with_delay_number_ans(number):
    tts = gTTS(text=number,lang=language_service.get_lang_short())
    tts.save(get_directory('number_ans.mp3'))
    mixer.music.load(get_directory('number_ans.mp3'))
    play_with_delay()
    mixer.music.load(get_directory('temp_file.mp3'))
    return number

def get_and_play_with_delay_time_ans():
    text = language_service.get_time_ans_text()
    tts = gTTS(text=text,lang=language_service.get_lang_short())
    tts.save(get_directory('time_ans.mp3'))
    mixer.music.load(get_directory('time_ans.mp3'))
    play_with_delay()
    mixer.music.load(get_directory('temp_file.mp3'))
    return text

    
def get_and_play_with_delay_date_ans():
    text = language_service.get_date_ans_text()
    tts = gTTS(text=text,lang=language_service.get_lang_short())
    tts.save(get_directory('date_ans.mp3'))
    mixer.music.load(get_directory('date_ans.mp3'))
    play_with_delay()
    mixer.music.load(get_directory('temp_file.mp3'))
    return text

def get_and_play_with_delay_weather_ans():
    weather = Weather()
    location = weather.lookup_by_location(language_service.get_provinces_name_english())
    condition = location.condition()
    forecasts = location.forecast()
    text = language_service.get_temperature_ans_text(convert_fahrenheit_to_celsius(forecasts[0].low()),convert_fahrenheit_to_celsius(forecasts[0].high()))
    tts = gTTS(text=text,lang=language_service.get_lang_short())
    tts.save(get_directory('temperature_ans.mp3'))
    mixer.music.load(get_directory('temperature_ans.mp3'))
    play_with_delay()
    mixer.music.load(get_directory('temp_file.mp3'))
    return text