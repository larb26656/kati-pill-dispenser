from pygame import mixer
import pygame
import pymysql
from gtts import gTTS
import time
import language_service
from langdetect import detect
from time import strftime
from weather import Weather
import config_service
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

def set_reduce_volume():
    mixer.music.set_volume(0.5)

def set_max_volume():
    mixer.music.set_volume(1.0)

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
    try:
        int(text_to_talk)
        language = language_service.get_lang_short()
    except:
        language = detect(text_to_talk)
    if (language == "th"):
        language_directory = "thai"
    else:
        language_directory = "english"
    try:
        tts = gTTS(text=text_to_talk, lang=language)
        tts.save(get_directory_with_set_language('custom_msg_temp.mp3', language_directory))
        mixer.music.load(get_directory_with_set_language('custom_msg_temp.mp3', language_directory))
        config_service.set_config_robot_connect_true_status()
        return True
    except:
        mixer.music.load(get_directory_with_set_language('lost_connect_ans.mp3', language_directory))
        config_service.set_config_robot_connect_false_status()
        return False


    """try:
        text_to_talk = int(text_to_talk)
        language = language_service.get_lang_short()
    except:
        language = detect(text_to_talk)
        print(language)
    if(language=="th"):
        language_directory = "thai"
        language = "th"
    else:
        language_directory = "english"
        language = "en"
    #try:
    tts = gTTS(text=text_to_talk,lang=language_service.get_lang_short())
    tts.save(get_directory_with_set_language('custom_msg_temp.mp3', language_directory))
    mixer.music.load(get_directory_with_set_language('custom_msg_temp.mp3', language_directory))
    config_service.set_config_robot_connect_true_status()
    return True
    except:
        print("aaa")
        mixer.music.load(get_directory_with_set_language('lost_connect_ans.mp3', language_directory))
        config_service.set_config_robot_connect_false_status()
        return False"""

def set_custom_msg_with_filename(text_to_talk,filename):
    language=detect(text_to_talk)
    if(language=="th"):
        language_directory="thai"
    else:
        language_directory="english"
    try:
        tts = gTTS(text=text_to_talk,lang=language)
        tts.save(get_directory_with_set_language(filename+'.mp3',language_directory))
        mixer.music.load(get_directory_with_set_language(filename+'.mp3',language_directory))
    except:
        mixer.music.load(get_directory_with_set_language('lost_connect_ans.mp3', language_directory))

def get_and_play_with_delay_command_not_found_ans():
    text = language_service.get_and_play_with_delay_command_not_found_ans_text()
    mixer.music.load(get_directory('comand_not_found_ans.mp3'))
    play_with_delay()
    mixer.music.load(get_directory('temp_file.mp3'))
    return text

def get_and_play_with_delay_pill_not_found_ans():
    text = language_service.get_and_play_with_delay_pill_not_found_ans_text()
    mixer.music.load(get_directory('pill_not_found_ans.mp3'))
    play_with_delay()
    mixer.music.load(get_directory('temp_file.mp3'))
    return text

def get_and_play_with_delay_calculator_enable_ans():
    text = language_service.get_and_play_with_delay_calculator_enable_ans_text()
    mixer.music.load(get_directory('calculator_enable_ans.mp3'))
    play_with_delay()
    mixer.music.load(get_directory('temp_file.mp3'))
    return text

def get_and_play_with_delay_calculator_disable_ans():
    text = language_service.get_and_play_with_delay_calculator_disable_ans_text()
    mixer.music.load(get_directory('calculator_disable_ans.mp3'))
    play_with_delay()
    mixer.music.load(get_directory('temp_file.mp3'))
    return text

def get_and_play_with_delay_number_ans(number):
    try:
        tts = gTTS(text=number,lang=language_service.get_lang_short())
        tts.save(get_directory('number_ans.mp3'))
        mixer.music.load(get_directory('number_ans.mp3'))
        play_with_delay()
        mixer.music.load(get_directory('temp_file.mp3'))
        config_service.set_config_robot_connect_true_status()
    except:
        mixer.music.load(get_directory('lost_connect_ans.mp3'))
        play_with_delay()
        mixer.music.load(get_directory('temp_file.mp3'))
        config_service.set_config_robot_connect_false_status()
    return number

def get_and_play_with_delay_time_ans():
    text = language_service.get_time_ans_text()
    try:
        tts = gTTS(text=text,lang=language_service.get_lang_short())
        tts.save(get_directory('time_ans.mp3'))
        mixer.music.load(get_directory('time_ans.mp3'))
        play_with_delay()
        mixer.music.load(get_directory('temp_file.mp3'))
    except:
        mixer.music.load(get_directory('lost_connect_ans.mp3'))
        play_with_delay()
        mixer.music.load(get_directory('temp_file.mp3'))
    return text

    
def get_and_play_with_delay_date_ans():
    text = language_service.get_date_ans_text()
    try:
        tts = gTTS(text=text,lang=language_service.get_lang_short())
        tts.save(get_directory('date_ans.mp3'))
        mixer.music.load(get_directory('date_ans.mp3'))
        play_with_delay()
        mixer.music.load(get_directory('temp_file.mp3'))
        config_service.set_config_robot_connect_true_status()
    except:
        mixer.music.load(get_directory('lost_connect_ans.mp3'))
        play_with_delay()
        mixer.music.load(get_directory('temp_file.mp3'))
        config_service.set_config_robot_connect_false_status()
    return text

def get_and_play_with_delay_weather_ans():
    try:
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
        config_service.set_config_robot_connect_true_status()
    except:
        text = "error";
        mixer.music.load(get_directory('lost_connect_ans.mp3'))
        play_with_delay()
        mixer.music.load(get_directory('temp_file.mp3'))
        config_service.set_config_robot_connect_false_status()
    finally:
        return text

def get_and_play_with_delay_memo_enable_ans():
    text = language_service.get_and_play_with_delay_memo_enable_ans_text()
    tts = gTTS(text=text,lang=language_service.get_lang_short())
    tts.save(get_directory('memo_enable_ans.mp3'))
    mixer.music.load(get_directory('memo_enable_ans.mp3'))
    play_with_delay()
    mixer.music.load(get_directory('temp_file.mp3'))
    return text

