from datetime import datetime
from time import strftime
import pymysql
from threading import Thread
import connect_service
import text_to_speech_service
import ultrasonic_dummy
import infrared_dummy
import stepmotor_service
import notification_service
import setting_service
import language_service
from PyQt4 import QtCore as core
import time
from logging_service import Main_log


class Start_clock_Thread(core.QThread):
    schedule_id = ""
    schedule_time = ""
    schedule_time_diff = ""
    memo_id = ""
    memo_desc = ""
    memo_notification_time = ""
    memo_time_diff = ""
    minutes_pill_dispenser_alarm = 29
    minutes_memo_alarm = 4
    ultrasonic_step = '1'
    behavior_status = False

    def __init__(self, parent=None):
        core.QThread.__init__(self)

    def set_kati_status(self, text):
        f = open('data/kati_status.txt', 'w', encoding='utf-8')
        f.write(text)
        f.close

    def get_kati_status(self):
        f = open('data/kati_status.txt', 'r', encoding='utf-8')
        data = f.read()
        return data
        f.close()

    def set_kati_face_status(self, text):
        f = open('data/kati_face_status.txt', 'w', encoding='utf-8')
        f.write(text)
        f.close

    def get_kati_face_status(self):
        f = open('data/kati_face_status.txt', 'r', encoding='utf-8')
        data = f.read()
        return data
        f.close()

    def get_time_diff(self, time_alarm):
        fmt = '%Y-%m-%d %H:%M:%S'
        self.d1 = datetime.strptime(strftime("%Y-%m-%d") + " " + time_alarm, fmt)
        self.d2 = datetime.strptime(strftime("%Y-%m-%d %H:%M:%S"), fmt)
        # Convert to Unix timestamp
        self.d1_ts = time.mktime(self.d1.timetuple())
        self.d2_ts = time.mktime(self.d2.timetuple())

        self.timediff = int(self.d2_ts - self.d1_ts) / 60
        #old method
        #return math.floor(self.timediff)
        return self.timediff

    def get_schedule_time_list(self):
        global schedule_id, schedule_time, schedule_time_diff
        conn = connect_service.get_connect_sql()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(
            "SELECT Schedule_id,Schedule_time,FLOOR(TIME_TO_SEC(TIMEDIFF(CURTIME(),Schedule_time))/ 60) AS Timediff FROM schedule WHERE FLOOR(TIME_TO_SEC(TIMEDIFF(CURTIME(),Schedule_time))/ 60) >= 0 AND FLOOR(TIME_TO_SEC(TIMEDIFF(CURTIME(),Schedule_time))/ 60) <= " + str(
                self.minutes_pill_dispenser_alarm) + " AND Schedule_visiblestatus = '1' ORDER BY FLOOR(TIME_TO_SEC(TIMEDIFF(CURTIME(),Schedule_time))/ 60) DESC LIMIT 1")
        if (cur.rowcount > 0):
            for r in cur:
                if (self.get_behavior(r['Schedule_id'])):
                    self.schedule_id = ""
                    self.schedule_time = ""
                    self.schedule_time_diff = ""
                else:
                    if(self.get_pill_is_left(r['Schedule_id'])):
                        self.schedule_id = str(r['Schedule_id'])
                        self.schedule_time = str(r['Schedule_time'])
                        self.schedule_time_diff = str(r['Timediff'])
                    else:
                        self.schedule_id = ""
                        self.schedule_time = ""
                        self.schedule_time_diff = ""
        else:
            self.schedule_id = ""
            self.schedule_time = ""
            self.schedule_time_diff = ""
        cur.close()
        conn.close()

    def get_memo_time_list(self):
        global memo_id, memo_desc, memo_notification_time, memo_time_diff
        conn = connect_service.get_connect_sql()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(
            "SELECT *,FLOOR(TIME_TO_SEC(TIMEDIFF(CURTIME(),Memo_notification_time))/ 60) AS Timediff FROM `memo` WHERE FLOOR(TIME_TO_SEC(TIMEDIFF(CURTIME(),Memo_notification_time))/ 60) >= 0 AND FLOOR(TIME_TO_SEC(TIMEDIFF(CURTIME(),Memo_notification_time))/ 60) <= " + str(
                self.minutes_memo_alarm) + " AND (SUBSTRING(Memo_notification_day,DAYOFWEEK(CURDATE()), 1) OR Memo_notification_date = CURDATE()) AND Memo_visiblestatus = '1' ORDER BY FLOOR(TIME_TO_SEC(TIMEDIFF(CURTIME(),Memo_notification_time))/ 60) DESC LIMIT 1")
        if (cur.rowcount > 0):
            for r in cur:
                if (self.get_memo_log(r['Memo_id'])):
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
            self.memo_id = ""
            self.memo_desc = ""
            self.memo_notification_time = ""
            self.memo_time_diff = ""
        cur.close()
        conn.close()

    def get_behavior(self, Schedule_id):
        conn = connect_service.get_connect_sql()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM `behavior` WHERE Schedule_id = '" + str(
            Schedule_id) + "' AND SUBSTR(Behavior_datetime,1,10)=CURDATE() AND (Behavior_type = 'tookpill' OR Behavior_type = 'forgottakepill')")
        if (cur.rowcount > 0):
            return True
        else:
            return False
        cur.close()
        conn.close()

    def get_memo_log(self, Memo_id):
        conn = connect_service.get_connect_sql()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM `memo_log` WHERE Memo_id = '" + str(
            Memo_id) + "' AND SUBSTR(Memo_log_datetime,1,10)=CURDATE()")
        if (cur.rowcount > 0):
            return True
        else:
            return False
        cur.close()
        conn.close()

    def get_pill_is_left(self, Schedule_id):
        conn = connect_service.get_connect_sql()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM `dispenser` INNER JOIN slot ON dispenser.Slot_id = slot.Slot_id INNER JOIN pill ON slot.Pill_id = pill.Pill_id WHERE Schedule_id = '"+str(
            Schedule_id)+"' AND Pill_left > 0")
        if (cur.rowcount > 0):
            return True
        else:
            return False

    def get_time_list(self):
        global kati_status,test
        while True:
            self.get_schedule_time_list()
            self.get_memo_time_list()
            if (self.schedule_time_diff == "" and self.memo_time_diff == "" and not setting_service.get_pill_dispenser_status()):
                self.set_kati_status("free")
            elif (self.schedule_time_diff != "" and self.memo_time_diff == "" and not setting_service.get_pill_dispenser_status()):
                self.set_kati_status("schedule")
            elif (self.memo_time_diff != "" and self.schedule_time_diff == "" and not setting_service.get_pill_dispenser_status()):
                self.set_kati_status("memo")
            elif (self.memo_time_diff == "" and self.schedule_time_diff == "" and setting_service.get_pill_dispenser_status()):
                self.set_kati_status("pill_dispenser")
            else:
                self.set_kati_status("free")
            print(self.get_kati_status())
            time.sleep(1)

    def start_infrared_count_detect_memo(self,time_notification,memo_desc):
        global minutes_memo_alarm
        self.count = 0
        self.countdown = 3
        self.talk_connect_status = False
        if (text_to_speech_service.set_custom_msg(memo_desc)):
            text_to_speech_service.play_loop()
            self.talk_connect_status = True
        else:
            text_to_speech_service.play_with_delay()
        while True:
            if(self.get_time_diff(time_notification) >= 0 and self.get_time_diff(time_notification) <= self.minutes_memo_alarm):
                if(not self.talk_connect_status):
                    if (text_to_speech_service.set_custom_msg(memo_desc)):
                        text_to_speech_service.play_loop()
                        self.talk_connect_status = True
                if (infrared_dummy.get_distance_less()):
                    text_to_speech_service.set_reduce_volume()
                    self.count = self.count + 1
                    if (self.count == 3):
                        break
                else:
                    if (self.count > 0):
                        if (self.countdown > 0):
                            self.countdown = self.countdown - 1
                        else:
                            if (self.count >= 0):
                                self.count = self.count - 1
                                print(self.count)
                    else:
                        self.countdown = 3
                        text_to_speech_service.set_max_volume()
                print(self.count)
                time.sleep(1)
            else:
                break

    def start_infrared_count_detect_pill_dispenser_with_countdown_do_something(self,minutes,method):
        self.sec = minutes*60
        self.sec_count = 0
        self.count = 0
        self.countdown = 3
        while True:
            if (self.sec_count <= self.sec):
                if (infrared_dummy.get_distance_less()):
                    text_to_speech_service.set_reduce_volume()
                    self.count = self.count + 1
                    if (self.count == 3):
                        break
                else:
                    if (self.count > 0):
                        if (self.countdown > 0):
                            self.countdown = self.countdown - 1
                        else:
                            if (self.count >= 0):
                                self.count = self.count - 1
                                print(self.count)
                    else:
                        self.countdown = 3
                        text_to_speech_service.set_max_volume()
                print(self.count)
                time.sleep(1)
            else:
                method()
                self.sec_count = 0

    def start_infrared_count_detect_pill_dispenser_boolean(self,time_notification):
        self.count_status = False
        self.count = 0
        self.countdown = 3
        while (self.count_status == False):
            if(self.get_time_diff(time_notification) >= 0 and self.get_time_diff(time_notification) <= self.minutes_pill_dispenser_alarm):
                if (infrared_dummy.get_distance_less()):
                    text_to_speech_service.set_reduce_volume()
                    print(self.count)
                    self.count = self.count + 1
                    if (self.count == 3):
                        return True
                else:
                    print(self.count)
                    if (self.count > 0):
                        if (self.countdown > 0):
                            self.countdown = self.countdown - 1
                        else:
                            if (self.count >= 0):
                                self.count = self.count - 1
                                print(self.count)
                    else:
                        self.countdown = 3
                        text_to_speech_service.set_max_volume()
                time.sleep(1)
            else:
                return False

    def start_get_distance_less_count_detect_pill_dispenser_with_countdown_do_something(self,minutes,method):
        self.sec = minutes*60
        self.sec_count = 0
        self.count = 0
        self.countdown = 3
        while True:
            if(self.sec_count <= self.sec):
                if (ultrasonic_dummy.get_distance_less()):
                    text_to_speech_service.set_reduce_volume()
                    print(self.count)
                    self.count = self.count + 1
                    if (self.count == 3):
                        break
                else:
                    if (self.count > 0):
                        if (self.countdown > 0):
                            self.countdown = self.countdown - 1
                        else:
                            if (self.count >= 0):
                                self.count = self.count - 1
                                print(self.count)
                    else:
                        self.countdown = 3
                        text_to_speech_service.set_max_volume()
                self.sec_count = self.sec_count +1
                print(self.sec_count)
                time.sleep(1)
            else:
                method()
                self.sec_count = 0

    def start_get_distance_less_count_detect_pill_dispenser_with_countdown_do_something_and_talk(self,minutes,method):
        self.sec = minutes*60
        self.sec_count = 0
        self.count = 0
        self.countdown = 3
        self.cooldown = 3
        self.alarm_status = False
        while True:
            if(self.sec_count <= self.sec):
                if (ultrasonic_dummy.get_distance_less()):
                    text_to_speech_service.set_reduce_volume()
                    print(self.count)
                    self.count = self.count + 1
                    if (self.count == 3):
                        break
                else:
                    if (self.cooldown > 0):
                        self.cooldown = self.cooldown - 1
                    else:
                        if(not self.alarm_status):
                            self.emit(core.SIGNAL("dosomething(QString)"), str("2"))
                            text_to_speech_service.set_msg_put_glass_far_alarm()
                            text_to_speech_service.play_loop()
                            self.alarm_status = True
                        if (self.count > 0):
                            if (self.countdown > 0):
                                self.countdown = self.countdown - 1
                            else:
                                if (self.count >= 0):
                                    self.count = self.count - 1
                                    print(self.count)
                        else:
                            self.countdown = 3
                            text_to_speech_service.set_max_volume()
                print(self.sec_count)
                self.sec_count = self.sec_count +1
                time.sleep(1)
            else:
                method()
                self.sec_count = 0

    def start_get_distance_more_count_detect_pill_dispenser_with_countdown_do_something(self, minutes, method):
        self.sec = minutes * 60
        self.sec_count = 0
        self.count = 0
        self.countdown = 3
        while True:
            if (self.sec_count <= self.sec):
                if (ultrasonic_dummy.get_distance_more()):
                    text_to_speech_service.set_reduce_volume()
                    print(self.count)
                    self.count = self.count + 1
                    if (self.count == 3):
                        break
                else:
                    if (self.count > 0):
                        if (self.countdown > 0):
                            self.countdown = self.countdown - 1
                        else:
                            if (self.count >= 0):
                                self.count = self.count - 1
                                print(self.count)
                    else:
                        self.countdown = 3
                        text_to_speech_service.set_max_volume()
                print(self.sec_count)
                self.sec_count = self.sec_count + 1
                time.sleep(1)
            else:
                method()
                self.sec_count = 0

    def get_pill_dispenser_with_schedule_sensor_detect(self,time):
        self.emit(core.SIGNAL("dosomething(QString)"), str("2"))
        text_to_speech_service.set_msg_pill_alarm()
        text_to_speech_service.play_loop()
        if(self.start_infrared_count_detect_pill_dispenser_boolean(time)):
            self.start_get_distance_less_count_detect_pill_dispenser_with_countdown_do_something_and_talk(1,notification_service.sent_all_behavior_come_but_no_take_pill_in_background)
            self.emit(core.SIGNAL("dosomething(QString)"), str("2"))
            text_to_speech_service.set_msg_pill_dispensing_alarm()
            text_to_speech_service.play_loop()
            stepmotor_service.pill_dispenser_with_schedule_id(self.schedule_id)
            self.emit(core.SIGNAL("dosomething(QString)"), str("2"))
            text_to_speech_service.set_msg_put_glass_near_alarm()
            text_to_speech_service.play_loop()
            self.start_get_distance_more_count_detect_pill_dispenser_with_countdown_do_something(1,notification_service.sent_all_behavior_come_but_no_take_pill_in_background)
            self.emit(core.SIGNAL("dosomething(QString)"), str("2"))
            text_to_speech_service.set_msg_put_glass_far_after_take_pill_alarm()
            text_to_speech_service.play_loop()
            self.start_get_distance_less_count_detect_pill_dispenser_with_countdown_do_something(1,notification_service.sent_all_behavior_come_but_no_take_pill_in_background)
            return True
        else:
            return False

    def get_pill_dispenser_with_command_sensor_detect(self,pill_id):
        self.emit(core.SIGNAL("dosomething(QString)"), str("2"))
        text_to_speech_service.set_msg_pill_found_alarm()
        text_to_speech_service.play_loop()
        self.start_infrared_count_detect_pill_dispenser_with_countdown_do_something(15,notification_service.sent_all_behavior_come_but_no_take_pill_in_background)
        self.start_get_distance_less_count_detect_pill_dispenser_with_countdown_do_something_and_talk(1,notification_service.sent_all_behavior_come_but_no_take_pill_in_background)
        self.emit(core.SIGNAL("dosomething(QString)"), str("2"))
        text_to_speech_service.set_msg_pill_dispensing_alarm()
        text_to_speech_service.play_loop()
        stepmotor_service.pill_dispenser_with_pill_id(pill_id)
        self.emit(core.SIGNAL("dosomething(QString)"), str("2"))
        text_to_speech_service.set_msg_put_glass_near_alarm()
        text_to_speech_service.play_loop()
        self.start_get_distance_more_count_detect_pill_dispenser_with_countdown_do_something(1,notification_service.sent_all_behavior_come_but_no_take_pill_in_background)
        self.emit(core.SIGNAL("dosomething(QString)"), str("2"))
        text_to_speech_service.set_msg_put_glass_far_after_take_pill_alarm()
        text_to_speech_service.play_loop()
        self.start_get_distance_less_count_detect_pill_dispenser_with_countdown_do_something(1,notification_service.sent_all_behavior_come_but_no_take_pill_in_background)

    def start_clock(self):
        setting_service.set_pill_dispenser_false_status()
        self.set_kati_status("free")
        self.set_kati_face_status("normal")
        global kati_status, speak_status, ultrasonic_step, behavior_status, has_run ,test
        background_thread = Thread(target=self.get_time_list, args=())
        background_thread.start()
        while True:
            if (self.get_kati_status() == "free"):
                self.face_status = False
                print(strftime("%Y-%m-%d %H:%M:%S"))
                if (self.get_kati_face_status() == "normal"):
                    while (self.get_kati_face_status() == "normal" and self.get_kati_status() == "free"):
                        if (self.face_status == False):
                            self.emit(core.SIGNAL("dosomething(QString)"), str("1"))
                            print("1")
                            self.face_status = True
                        print("11")
                        time.sleep(1)
                    self.face_status = False
                elif (self.get_kati_face_status() == "talk"):
                    while (self.get_kati_face_status() == "talk" and self.get_kati_status() == "free"):
                        if (self.face_status == False):
                            self.emit(core.SIGNAL("dosomething(QString)"), str("2"))
                            print("2")
                            self.face_status = True
                        print("22")
                        time.sleep(1)
                    self.face_status = False
            elif (self.get_kati_status() == "schedule"):
                Main_log.logger.info("Kati do schedule notification.")
                schedule_time = self.schedule_time
                schedule_id = self.schedule_id
                notification_service.sent_all_schedule_message_in_background()
                if(self.get_pill_dispenser_with_schedule_sensor_detect(schedule_time)):
                    notification_service.sent_all_behavior_took_pill_in_background(schedule_id)
                    self.set_kati_status("free")
                    text_to_speech_service.stop()
                    self.emit(core.SIGNAL("dosomething(QString)"), str("1"))
                else:
                    notification_service.sent_all_behavior_forgot_take_pill_in_background(schedule_id)
                    self.set_kati_status("free")
                    text_to_speech_service.stop()
                    self.emit(core.SIGNAL("dosomething(QString)"), str("1"))

                print("stop")
            elif (self.get_kati_status() == "memo"):
                Main_log.logger.info("Kati do memo notification.")
                memo_id = self.memo_id
                memo_desc = self.memo_desc
                memo_notification_time = self.memo_notification_time
                print("ring_memo")
                notification_service.sent_all_memo_message_in_background(memo_desc)
                self.emit(core.SIGNAL("dosomething(QString)"), str("3" + memo_desc))
                self.start_infrared_count_detect_memo(memo_notification_time,memo_desc)
                text_to_speech_service.stop()
                print("finish")
                self.emit(core.SIGNAL("dosomething(QString)"), str("4" + memo_desc))
                notification_service.insert_memo_log(memo_id)
                self.set_kati_status("free")

            elif (self.get_kati_status() == "pill_dispenser"):
                Main_log.logger.info("Kati do pill dispenser")
                self.pill_id = setting_service.get_pill_id()
                self.get_pill_dispenser_with_command_sensor_detect(self.pill_id)
                notification_service.sent_all_behavior_took_one_pill_in_background(self.pill_id)
                text_to_speech_service.stop()
                setting_service.set_pill_dispenser_false_status()
                print("stop")
            time.sleep(1)

        def start_server(self):
            self.i = 0
            while True:
                time.sleep(1)
                if (self.i < 6):
                    print(self.i)
                    self.i = self.i + 1
                else:
                    self.i = 0
                    self.emit(core.SIGNAL("dosomething(QString)"), str(self.i))

    def run(self):
        self.start_clock()