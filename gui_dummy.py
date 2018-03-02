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
form.text_display("Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc,")
app.exec_()