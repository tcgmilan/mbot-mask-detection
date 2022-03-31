from src.logger import Logger

import colorama
import datetime
import configparser
import os

colorama.init()
path = "/home/pi/mbot-mask-detection"
config = configparser.ConfigParser()
config.read(os.path.join(path,"BEALLITASOK.cfg"), encoding = "utf-8")
logger = Logger()
logger.init()

def ctime():
    return "[" + colorama.Fore.CYAN+ datetime.datetime.now().strftime("%H:%M:%S") + "]"

def face_counter(faces : list):
    logger.wrtie_log(config["BEALLITASOK"]["arcok_szama"].replace("!arcok", str(len(faces))))
    print(ctime() + colorama.Fore.MAGENTA + config["BEALLITASOK"]["arcok_szama"].replace("!arcok",colorama.Fore.YELLOW + (str(len(faces))))) 

def mask_found():
    logger.wrtie_log(config["BEALLITASOK"]["van_maszk"])
    print(ctime() + colorama.Fore.GREEN + config["BEALLITASOK"]["van_maszk"])

def mask_not_found():
    logger.wrtie_log(config["BEALLITASOK"]["nincs_maszk"])
    print(ctime() + colorama.Fore.RED + config["BEALLITASOK"]["nincs_maszk"])

