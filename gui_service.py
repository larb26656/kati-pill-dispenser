from PyQt4 import QtGui as gui
from PyQt4 import QtCore as core
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView
import notification_service
import clock_service
import setting_service
import sys
import socket

class MainApp(gui.QWidget):
    def __init__(self, parent=None):
        super(MainApp,self).__init__(parent)
        self.web_view = QWebView()
        self.web_view.setWindowTitle("Kati")
        self.web_view.setGeometry(80, 80, 480, 256)
        #self.web_view.showMaximized()
        if(self.is_connected()):
            setting_service.set_robot_connect_true_status()
        else:
            setting_service.set_robot_connect_false_status()
        self.thread = clock_service.Start_clock_Thread()
        self.thread.start()
        self.thread2 = notification_service.Sent_all_data_error_Thread()
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

    def is_connected(self):
        REMOTE_SERVER = "www.google.com"
        try:
            host = socket.gethostbyname(REMOTE_SERVER)
            s = socket.create_connection((host, 80), 2)
            return True
        except:
            pass
        return False

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
