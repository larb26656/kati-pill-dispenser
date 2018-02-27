import logging
from logging import FileHandler
from logging import Formatter
import datetime

def get_file_name_as_date(log_type):
    file_name = "log/"+log_type+"/"+str(datetime.date.today())+".log"
    return file_name

class Main_log():
    log_format = log_format = (
            "%(asctime)s [%(levelname)s]: %(message)s")
    log_level = logging.INFO
    log_file = get_file_name_as_date("main")
    logger = logging.getLogger("main_log")

    logger.setLevel(log_level)
    file_handler = FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(Formatter(log_format))
    logger.addHandler(file_handler)

class Socket_log():
    log_format = log_format = (
            "%(asctime)s [%(levelname)s]: %(message)s")
    log_level = logging.INFO
    log_file = get_file_name_as_date("socket")
    logger = logging.getLogger("socket_log")

    logger.setLevel(log_level)
    file_handler = FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(Formatter(log_format))
    logger.addHandler(file_handler)



