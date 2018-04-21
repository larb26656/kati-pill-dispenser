import threading

from PyQt4 import QtGui as gui
from PyQt4 import QtGui
from PyQt4 import QtCore as core
from PyQt4.QtCore import QThread, QUrl, QCoreApplication
from PyQt4.QtWebKit import QWebView
import threading
import notification_service
import clock_service
import config_service
import sys
import socket
import os.path
import traceback
from logging_service import Main_log

class MainApp(gui.QWidget):
    thread = clock_service.Start_clock_Thread()
    thread2 = notification_service.Sent_all_data_error_Thread()

    def run(self, parent=None):
        global thread,thread2
        super(MainApp,self).__init__(parent)
        self.web_view = QWebView()
        self.web_view.setWindowTitle("Kati")
        self.web_view.setGeometry(80, 80, 480, 256)
        self.web_view.showMaximized()
        if(self.is_connected()):
            config_service.set_config_robot_connect_true_status()
        else:
            config_service.set_config_robot_connect_false_status()
        self.thread.start()
        self.thread2.start()
        self.connect(self.thread, core.SIGNAL("dosomething(QString)"), self.doing)
        self.normal_face()
        self.web_view.show()

    def normal_face(self):
        r = QUrl("http://127.0.0.1/robot_gui/normal_face.php")
        self.web_view.load(r)

    def talk_face(self):
        r = QUrl("http://127.0.0.1/robot_gui/talk_face.php")
        self.web_view.load(r)

    def text_display(self,text):
        r = QUrl("http://127.0.0.1/robot_gui/text_display.php?text="+text)
        self.web_view.load(r)

    def text_display_after_time_out(self, text):
        r = QUrl("http://127.0.0.1/robot_gui/text_display_after_time_out.php?text=" + text)
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

    def kill_all_thread(self):
        self.thread.terminate()
        self.thread2.terminate()

    def doing(self, i):
        if(i[:1]=="1"):
            self.normal_face()
        elif(i[:1]=="2"):
            self.talk_face()
        elif(i[:1]=="3"):
            self.text_display(i[1:])
        elif(i[:1]=="4"):
            self.text_display_after_time_out(i[1:])

def install_thread_excepthook():
    """
    Workaround for sys.excepthook thread bug
    (https://sourceforge.net/tracker/?func=detail&atid=105470&aid=1230540&group_id=5470).
    Call once from __main__ before creating any threads.
    If using psyco, call psycho.cannotcompile(threading.Thread.run)
    since this replaces a new-style class method.
    """
    import sys
    run_old = threading.Thread.run
    def run(*args, **kwargs):
        try:
            run_old(*args, **kwargs)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            sys.excepthook(*sys.exc_info())
    threading.Thread.run = run

def handle_exception(exc_type, exc_value, exc_traceback):
    """ handle all exceptions """

    ## KeyboardInterrupt is a special case.
    ## We don't raise the error dialog when it occurs.
    if issubclass(exc_type, KeyboardInterrupt):
        if gui.qApp:
          gui.qApp.quit()
        return

    form.kill_all_thread()

    filename, line, dummy, dummy = traceback.extract_tb( exc_traceback ).pop()
    filename = os.path.basename( filename )
    error    = "%s: %s" % ( exc_type.__name__, exc_value )
    Main_log.logger.error(error)

    QtGui.QMessageBox.critical(None,"Error",
    "<html>A critical error has occured.<br/> "
    + "<b>%s</b><br/><br/>" % error
    + "It occurred at <b>line %d</b> of file <b>%s</b>.<br/>" % (line, filename)
    + "</html>")

    """print ("Closed due to an error. This is the full error report:")
    print ("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))"""
    QCoreApplication.quit()

class FlaskThread(QThread):
    def __init__(self, application):
        QThread.__init__(self)
        self.application = application

    def __del__(self):
        self.wait()

    def run(self):
        self.application.run(host='0.0.0.0')

qtapp = gui.QApplication(sys.argv)
from socket_service import app
webapp = FlaskThread(app)
webapp.start()

qtapp.aboutToQuit.connect(webapp.terminate)
form = MainApp()
install_thread_excepthook()
sys.excepthook = handle_exception
form.run()
Main_log.logger.info("Open main GUI.")
qtapp.exec_()

"""if __name__ == '__main__':
    from socket_service import app
    sys.exit(provide_GUI_for(app))"""

"""install_thread_excepthook()
sys.excepthook = handle_exception

app = gui.QApplication(sys.argv)
form = MainApp()
form.run()
Main_log.logger.info("Open main GUI.")
app.exec_()"""
