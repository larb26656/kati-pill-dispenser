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

class MainApp(gui.QWidget):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.web_view = QWebView()
        self.web_view.setWindowTitle("Kati")
        self.web_view.setGeometry(0, 0, 480, 256)
        # self.web_view.showMaximized()
        self.normal_face()
        self.web_view.show()

    def normal_face(self):
        r = QUrl("http://127.0.0.1/kati2/robot_gui/normal_face.php")
        self.web_view.load(r)

    def talk_face(self):
        r = QUrl("http://127.0.0.1/kati2/robot_gui/talk_face.php")
        self.web_view.load(r)

    def text_display(self, text):
        r = QUrl("http://127.0.0.1/kati2/robot_gui/text_display.php?text=" + text)
        self.web_view.load(r)


app = gui.QApplication(sys.argv)
form = MainApp()
form.text_display("ทดสอบ")
app.exec_()