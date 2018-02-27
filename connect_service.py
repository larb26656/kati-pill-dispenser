import pymysql
from PyQt4.QtGui import QMessageBox
from pyfcm import FCMNotification
from firebase import firebase

def get_connect_sql():
        return pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='kati',charset='utf8')

def get_connect_firebase_real_time_database():
    return {
  "apiKey": "AIzaSyBEihoJYWWFkEaiOrqJcN6rcYKHYW1mMXU",
  "authDomain": "kati-a04e1.firebaseapp.com",
  "databaseURL": "https://kati-a04e1.firebaseio.com",
  "storageBucket": "kati-a04e1.appspot.com",
  "messagingSenderId": "642042925714"
    }
def get_connect_firebase_cloud_message():
    return FCMNotification(api_key="AIzaSyDyZzkLDxupheGiHtz6lAATU28cplq0Tj0")
