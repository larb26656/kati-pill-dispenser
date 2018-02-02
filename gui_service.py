from PyQt4 import QtGui as gui
from PyQt4 import QtCore as core
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView
from datetime import datetime
from time import strftime
import time
import pymysql
from threading import Thread
import math
import text_to_speech_service
import ultrasonic_dummy
import infrared_dummy
import stepmotor_service
import notification_service

import sys
import time

class TestThread(core.QThread):
    def run(self):
        while True:
            print("a")
            time.sleep(1)
class ServerThread(core.QThread):
    
    schedule_id = ""
    schedule_time = ""
    schedule_time_diff = ""
    memo_id = ""
    memo_desc = ""
    memo_notification_time = ""
    memo_time_diff = ""
    minutes_alarm = 1
    minutes_alarm_text = 1
    ultrasonic_step = '1'
    behavior_status = False
    
    def __init__(self, parent=None):
        core.QThread.__init__(self)

    def set_kati_status(self,text):
        f = open('data/kati_status.txt','w',encoding='utf-8')
        f.write(text)
        f.close
        
    def get_kati_status(self):
        f = open('data/kati_status.txt','r',encoding='utf-8')
        data = f.read()
        return data
        f.close()

    def set_kati_face_status(self,text):
        f = open('data/kati_face_status.txt','w',encoding='utf-8')
        f.write(text)
        f.close
        
    def get_kati_face_status(self):
        f = open('data/kati_face_status.txt','r',encoding='utf-8')
        data = f.read()
        return data
        f.close()
        
    def get_time_diff(self,time_alarm):
        fmt = '%Y-%m-%d %H:%M:%S'
        self.d1 = datetime.strptime(strftime("%Y-%m-%d")+" "+time_alarm, fmt)
        self.d2 = datetime.strptime(strftime("%Y-%m-%d %H:%M:%S"), fmt)
        # Convert to Unix timestamp
        self.d1_ts = time.mktime(self.d1.timetuple())
        self.d2_ts = time.mktime(self.d2.timetuple())

        self.timediff = int(self.d2_ts-self.d1_ts) / 60
        return math.floor(self.timediff)


    def get_schedule_time_list(self):
        global schedule_id,schedule_time,schedule_time_diff
        conn = pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='kati',charset='utf8')
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT Schedule_id,Schedule_time,FLOOR(TIME_TO_SEC(TIMEDIFF(CURTIME(),Schedule_time))/ 60) AS Timediff FROM schedule WHERE FLOOR(TIME_TO_SEC(TIMEDIFF(CURTIME(),Schedule_time))/ 60) >= 0 AND FLOOR(TIME_TO_SEC(TIMEDIFF(CURTIME(),Schedule_time))/ 60) <= "+str(self.minutes_alarm)+" AND Schedule_visiblestatus = '1' ORDER BY FLOOR(TIME_TO_SEC(TIMEDIFF(CURTIME(),Schedule_time))/ 60) DESC LIMIT 1")
        if(cur.rowcount > 0):
            for r in cur:
                if(self.get_behavior(r['Schedule_id'])):
                    self.schedule_id = ""
                    self.schedule_time = ""
                    self.schedule_time_diff = ""
                else:
                    self.schedule_id = str(r['Schedule_id'])
                    self.schedule_time = str(r['Schedule_time'])
                    self.schedule_time_diff = str(r['Timediff'])
        else:
            self.schedule_id = ""
            self.schedule_time = ""
            self.schedule_time_diff = ""
        cur.close()
        conn.close()

    def get_memo_time_list(self):
        global memo_id,memo_desc,memo_notification_time,memo_time_diff
        conn = pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='kati',charset='utf8')
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT *,FLOOR(TIME_TO_SEC(TIMEDIFF(CURTIME(),Memo_notification_time))/ 60) AS Timediff FROM `memo` WHERE FLOOR(TIME_TO_SEC(TIMEDIFF(CURTIME(),Memo_notification_time))/ 60) >= 0 AND FLOOR(TIME_TO_SEC(TIMEDIFF(CURTIME(),Memo_notification_time))/ 60) <= "+str(self.minutes_alarm_text)+" AND (SUBSTRING(Memo_notification_day,DAYOFWEEK(CURDATE()), 1) OR Memo_notification_date = CURDATE()) AND Memo_visiblestatus = '1' ORDER BY FLOOR(TIME_TO_SEC(TIMEDIFF(CURTIME(),Memo_notification_time))/ 60) DESC LIMIT 1")
        if(cur.rowcount > 0):
            for r in cur:
                if(self.get_memo_log(r['Memo_id'])):
                    self.memo_id = ""
                    self.memo_desc = ""
                    self.memo_notification_time = ""
                    self.memo_time_diff = ""  
                else:
                    self.memo_id = str(r['Memo_id'])
                    self.memo_desc = str(r['Memo_desc'])
                    self.memo_notification_time = str(r['Memo_notification_time'])
                    self.memo_time_diff = str(r['Timediff'])
        else:
            memo_id = ""
            memo_desc = ""
            memo_notification_time = ""
            memo_time_diff = ""  
        cur.close()
        conn.close()

    def get_behavior(self,Schedule_id):
        conn = pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='kati',charset='utf8')
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM `behavior` WHERE Schedule_id = '"+str(Schedule_id)+"' AND SUBSTR(Behavior_datetime,1,10)=CURDATE()")
        if(cur.rowcount > 0):
            return True
        else:
            return False
        cur.close()
        conn.close()
        
    def get_memo_log(self,Memo_id):
        conn = pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='kati',charset='utf8')
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM `memo_log` WHERE Memo_id = '"+str(Memo_id)+"' AND SUBSTR(Memo_log_datetime,1,10)=CURDATE()")
        if(cur.rowcount > 0):
            return True
        else:
            return False
        cur.close()
        conn.close()

    def get_time_list(self):
        global kati_status
        while True:
            self.get_schedule_time_list()
            self.get_memo_time_list()
            if(self.get_kati_status()[:14]=="pill_dispensor"):
                if(self.schedule_time_diff == "" and self.memo_time_diff == ""):
                    self.set_kati_status("free")
                elif(self.schedule_time_diff != "" and self.memo_time_diff == ""):
                    self.set_kati_status("schedule")
                elif(self.memo_time_diff != "" and self.schedule_time_diff == ""):
                    self.set_kati_status("memo")
                else:
                    self.set_kati_status("schedule")
            print(self.get_kati_status())
            time.sleep(1)
  

    def start_clock(self):
        self.set_kati_status("free")
        self.set_kati_face_status("normal")
        global kati_status,speak_status,ultrasonic_step,behavior_status,has_run
        background_thread = Thread(target=self.get_time_list, args=())
        background_thread.start()

        while True:
            if(self.get_kati_status() == "free"):
                self.face_status = False
                self.speak1_status = False
                self.speak2_status = False
                self.speak3_status = False
                self.speak4_status = False
                self.speak5_status = False
                self.speak6_status = False
                self.count1 = 1
                self.count2 = 1
                self.count3 = 1
                self.count4 = 1
                print(strftime("%Y-%m-%d %H:%M:%S"))
                if(self.get_kati_face_status() == "normal"):
                    while(self.get_kati_face_status() == "normal" and self.get_kati_status() == "free"):
                        if(self.face_status == False):
                            self.emit(core.SIGNAL("dosomething(QString)"), str("1"))
                            print("1")
                            self.face_status = True
                        print("11")
                        time.sleep(1)
                    self.face_status = False 
                elif(self.get_kati_face_status() == "talk"):
                    while(self.get_kati_face_status() == "talk" and self.get_kati_status() == "free"):
                        if(self.face_status == False):
                            self.emit(core.SIGNAL("dosomething(QString)"), str("2"))
                            print("2")
                            self.face_status = True
                        print("22")
                        time.sleep(1)
                    self.face_status = False 
            elif(self.get_kati_status() == "schedule"):
                while(self.get_time_diff(self.schedule_time)>=0 and self.get_time_diff(self.schedule_time)<=self.minutes_alarm):
                    print("ring")
                    if(self.ultrasonic_step == '1'):
                        print("wait")
                        if(self.speak1_status == False):
                            self.emit(core.SIGNAL("dosomething(QString)"), str("2"))
                            text_to_speech_service.set_msg_pill_alarm()
                            text_to_speech_service.play_loop()
                            self.speak1_status = True
                        if(infrared_dummy.get_distance_less()):
                            self.count1=self.count1+1
                            print(self.count1)
                            print("1")
                            if(self.count1 == 3):
                                print("step1 pass")
                                self.ultrasonic_step = '2'
                    elif(self.ultrasonic_step == '2'):
                        if(ultrasonic_dummy.get_distance_less()):
                            self.count2=self.count2+1
                            print("2")
                            if(self.count2 == 3):
                                print("step2 pass")
                                self.ultrasonic_step = '3'
                                if(self.speak3_status == False):
                                    self.emit(core.SIGNAL("dosomething(QString)"), str("2"))
                                    text_to_speech_service.set_msg_pill_dispensing_alarm()
                                    text_to_speech_service.play_loop()
                                    self.speak3_status = True
                                stepmotor_service.pill_dispenser_with_schedule_id(self.schedule_id)
                                if(self.speak4_status == False):
                                    self.emit(core.SIGNAL("dosomething(QString)"), str("2"))
                                    text_to_speech_service.set_msg_put_glass_near_alarm()
                                    text_to_speech_service.play_loop()
                                    self.speak4_status = True
                                #จ่ายยาลงมา
                        else:
                            if(self.speak2_status == False):
                                self.emit(core.SIGNAL("dosomething(QString)"), str("2"))
                                text_to_speech_service.set_msg_put_glass_far_alarm()
                                text_to_speech_service.play_loop()
                                self.speak2_status = True
                            print("test1")
                    elif(self.ultrasonic_step == '3'):
                        if(ultrasonic_dummy.get_distance_more()):
                            self.count3=self.count3+1
                            print("3")
                            if(self.count3 == 3):
                                print("step3 pass")
                                self.ultrasonic_step = '4'
                                if(self.speak5_status == False):
                                    self.emit(core.SIGNAL("dosomething(QString)"), str("2"))
                                    text_to_speech_service.set_msg_put_glass_far_after_take_pill_alarm()
                                    text_to_speech_service.play_loop()
                                    self.speak5_status = True
                        else:
                            print("sss")
                    else:
                        if(ultrasonic_dummy.get_distance_less()):
                            self.count4=self.count4+1
                            print("aaaa")
                            if(self.count4 == 3):
                                self.behavior_status = True
                                break
                    time.sleep(1)
                self.speak1_status = False
                self.speak2_status = False
                self.speak3_status = False
                self.speak4_status = False
                self.speak5_status = False
                self.count1 = 1
                self.count2 = 1
                self.count3 = 1
                self.count4 = 1
                if(self.behavior_status):
                    notification_service.sent_all_behavior_took_pill_in_background(self.schedule_id)
                else:
                    notification_service.sent_all_behavior_forgot_take_pill_in_background(self.schedule_id)
                self.behavior_status = False
                self.ultrasonic_step= '1'    
                self.set_kati_status("free")
                text_to_speech_service.stop()
                self.emit(core.SIGNAL("dosomething(QString)"), str("1"))
                self.speak_status = False
                print("stop")
            elif(self.get_kati_status() == "memo"):
                while(self.get_time_diff(self.memo_notification_time)>=0 and self.get_time_diff(self.memo_notification_time)<=self.minutes_alarm_text):
                    print("ring_memo")
                    if(self.ultrasonic_step == '1'):
                        if(self.speak6_status == False):
                            notification_service.sent_firebase_message_notification_in_background(self.memo_desc)
                            self.emit(core.SIGNAL("dosomething(QString)"), str("3"+self.memo_desc))
                            text_to_speech_service.set_custom_msg(self.memo_desc)
                            text_to_speech_service.play_loop()
                            self.speak6_status = True
                        if(infrared_dummy.get_distance_less()):
                            self.count1=self.count1+1
                            print(self.count1)
                            print("1")
                            if(self.count1 == 3):
                                print("step1 pass")
                                self.ultrasonic_step = '2'
                    else:
                        print("stop")
                        break
                    time.sleep(1)
                self.speak6_status = False
                text_to_speech_service.stop()
                self.emit(core.SIGNAL("dosomething(QString)"), str("1"))
                self.ultrasonic_step = '1'
                self.set_kati_status("free")
                self.count1 = 1
                stepmotor_service.insert_memo_log(self.memo_id)

            elif(self.get_kati_status()[:14] == "pill_dispenser"):
                self.pill_id = self.get_kati_status()[14:]
                self.main_loop_status = True
                self.face_status = False
                self.speak1_status = False
                self.speak2_status = False
                self.speak3_status = False
                self.speak4_status = False
                self.speak5_status = False
                self.speak6_status = False
                self.count1 = 1
                self.count2 = 1
                self.count3 = 1
                self.count4 = 1
                while(self.main_loop_status==True):
                    print("ring")
                    if(self.ultrasonic_step == '1'):
                        print("wait")
                        if(self.speak1_status == False):
                            self.emit(core.SIGNAL("dosomething(QString)"), str("2"))
                            text_to_speech_service.set_msg_pill_found_alarm()
                            text_to_speech_service.play_loop()
                            self.speak1_status = True
                        if(infrared_dummy.get_distance_less()):
                            self.count1=self.count1+1
                            print(self.count1)
                            print("1")
                            if(self.count1 == 3):
                                print("step1 pass")
                                self.ultrasonic_step = '2'
                    elif(self.ultrasonic_step == '2'):
                        if(ultrasonic_dummy.get_distance_less()):
                            self.count2=self.count2+1
                            print("2")
                            if(self.count2 == 3):
                                print("step2 pass")
                                self.ultrasonic_step = '3'
                                if(self.speak3_status == False):
                                    self.emit(core.SIGNAL("dosomething(QString)"), str("2"))
                                    text_to_speech_service.set_msg_pill_dispensing_alarm()
                                    text_to_speech_service.play_loop()
                                    self.speak3_status = True
                                stepmotor_service.pill_dispenser_with_pill_id(self.pill_id)
                                if(self.speak4_status == False):
                                    self.emit(core.SIGNAL("dosomething(QString)"), str("2"))
                                    text_to_speech_service.set_msg_put_glass_near_alarm()
                                    text_to_speech_service.play_loop()
                                    self.speak4_status = True
                                #จ่ายยาลงมา
                        else:
                            if(self.speak2_status == False):
                                self.emit(core.SIGNAL("dosomething(QString)"), str("2"))
                                text_to_speech_service.set_msg_put_glass_far_alarm()
                                text_to_speech_service.play_loop()
                                self.speak2_status = True
                            print("test1")
                    elif(self.ultrasonic_step == '3'):
                        if(ultrasonic_dummy.get_distance_more()):
                            self.count3=self.count3+1
                            print("3")
                            if(self.count3 == 3):
                                print("step3 pass")
                                self.ultrasonic_step = '4'
                                if(self.speak5_status == False):
                                    self.emit(core.SIGNAL("dosomething(QString)"), str("2"))
                                    text_to_speech_service.set_msg_put_glass_far_after_take_pill_alarm()
                                    text_to_speech_service.play_loop()
                                    self.speak5_status = True
                        else:
                            print("sss")
                    else:
                        if(ultrasonic_dummy.get_distance_less()):
                            self.count4=self.count4+1
                            print("aaaa")
                            if(self.count4 == 3):
                                self.behavior_status = True
                                break
                    time.sleep(1)
                self.speak1_status = False
                self.speak2_status = False
                self.speak3_status = False
                self.speak4_status = False
                self.speak5_status = False
                self.count1 = 1
                self.count2 = 1
                self.count3 = 1
                self.count4 = 1
                if(self.behavior_status):
                    notification_service.sent_all_behavior_took_one_pill_in_background(self.pill_id)
                else:
                    notification_service.sent_all_behavior_forgot_take_one_pill_in_background(self.pill_id)
                self.behavior_status = False
                self.ultrasonic_step= '1'
                self.set_kati_status("free")
                text_to_speech_service.stop()
                self.emit(core.SIGNAL("dosomething(QString)"), str("1"))
                self.speak_status = False
                print("stop")

            time.sleep(1)

        def start_server(self):
            self.i=0
            while True:
                time.sleep(1)
                if(self.i<6):
                    print(self.i)
                    self.i=self.i+1
                else:
                    self.i=0
                    self.emit(core.SIGNAL("dosomething(QString)"), str(self.i))

    def run(self):
        self.start_clock()

class MainApp(gui.QWidget):
    def __init__(self, parent=None):
        super(MainApp,self).__init__(parent)
        self.web_view = QWebView()
        self.web_view.setWindowTitle("Kati")
        self.web_view.setGeometry(0, 0, 480, 256)
        #self.web_view.showMaximized()
        self.thread = ServerThread()
        self.thread.start()
        self.thread2 = TestThread()
        self.thread2.start()
        self.connect(self.thread, core.SIGNAL("dosomething(QString)"), self.doing)
        self.normal_face()
        self.web_view.show()
        
    def normal_face(self):
        r = QUrl("http://127.0.0.1/kati2/robot_gui/normal_face.php")
        self.web_view.load(r)
        
    def talk_face(self):
        r = QUrl("http://127.0.0.1/kati2/robot_gui/talk_face.php")
        self.web_view.load(r)

    def text_display(self,text):
        r = QUrl("http://127.0.0.1/kati2/robot_gui/text_display.php?text="+text)
        self.web_view.load(r)



    def doing(self, i):
        if(i[:1]=="1"):
            self.normal_face()
        elif(i[:1]=="2"):
            self.talk_face()
        elif(i[:1]=="3"):
            self.text_display(i[1:])
            


    
app = gui.QApplication(sys.argv)
form = MainApp()
app.exec_()
