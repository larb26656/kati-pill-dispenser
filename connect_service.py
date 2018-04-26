import pymysql
from pyfcm import FCMNotification

def get_connect_sql():
    return pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='kati',charset='utf8')

def get_connect_firebase_real_time_database_kati_read():
    return {
  "apiKey": "AIzaSyBEihoJYWWFkEaiOrqJcN6rcYKHYW1mMXU",
  "authDomain": "kati-a04e1.firebaseapp.com",
  "databaseURL": "https://kati-a04e1.firebaseio.com",
  "storageBucket": "kati-a04e1.appspot.com",
  "messagingSenderId": "642042925714"
    }
def get_connect_firebase_real_time_database_kati_command():
    return {
  "apiKey": "AIzaSyBrlIGRSu8I4-B1TFwnargJtl05mzFLRBM",
  "authDomain": "katicommand.firebaseio.com",
  "databaseURL": "https://katicommand.firebaseio.com",
  "storageBucket": "katicommand.appspot.com",
  "messagingSenderId": "742625395929"
    }
def get_connect_firebase_cloud_message_kati_read():
    return FCMNotification(api_key="AIzaSyDyZzkLDxupheGiHtz6lAATU28cplq0Tj0")
def get_connect_firebase_cloud_message_kati_command():
    return FCMNotification(api_key="AIzaSyDc3sNuYyL-Kbf7-R6pgaPL7VjCfwaTOJ0")
