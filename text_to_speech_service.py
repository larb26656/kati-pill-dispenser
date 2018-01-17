from pygame import mixer
import pymysql
from gtts import gTTS
import time
import language_service
from langdetect import detect
from time import strftime
from weather import Weather

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
    
def set_command_not_found():
    mixer.music.load(get_directory('comand_not_found.mp3'))
    
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

def set_pill_not_found_ans():
    mixer.music.load(get_directory('pill_not_found_ans.mp3'))

def set_calculator_enable_ans():
    mixer.music.load(get_directory('calculator_enable_ans.mp3'))

def set_calculator_disable_ans():
    mixer.music.load(get_directory('calculator_disable_ans.mp3'))

def set_number_ans(number):
    tts = gTTS(text=number,lang=language_service.get_lang_short())
    tts.save(get_directory('number_ans.mp3'))
    mixer.music.load(get_directory('number_ans.mp3'))

def set_time_ans():
    time = language_service.get_time_ans_text()
    tts = gTTS(text=time,lang=language_service.get_lang_short())
    tts.save(get_directory('time_ans.mp3'))
    mixer.music.load(get_directory('time_ans.mp3'))
    
def set_date_ans():
    date = language_service.get_date_ans_text()
    tts = gTTS(text=date,lang=language_service.get_lang_short())
    tts.save(get_directory('date_ans.mp3'))
    mixer.music.load(get_directory('date_ans.mp3'))

def set_weather_ans():
    weather = Weather()
    location = weather.lookup_by_location(language_service.get_provinces_name_english())
    condition = location.condition()
    forecasts = location.forecast()
    temperature = language_service.get_temperature_ans_text(convert_fahrenheit_to_celsius(forecasts[0].low()),convert_fahrenheit_to_celsius(forecasts[0].high()))
    tts = gTTS(text=temperature,lang=language_service.get_lang_short())
    tts.save(get_directory('temperature_ans.mp3'))
    mixer.music.load(get_directory('temperature_ans.mp3'))
