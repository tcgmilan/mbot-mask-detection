# M5 : masKey
# Konzol kiíratásért felelős python kód
# https://github.com/tcgmilan/mbot-mask-detection

# Logger class beimportálása
from src.logger import Logger

# Színes konzolkimenet (colorama)
# Dátum lekéréséhez, formázásához szükséges könyvtár (datetime)
# .cfg fájl kezelő (configparser)
# Rendszerkezelő modul (os)
import colorama
import datetime
import configparser
import os

# Színes kimenet inicializálása
# Különböző elérési utak, globális változók deklarálása
# Beállítások betöltése
colorama.init()
path = "/home/pi/mbot-mask-detection"
config = configparser.ConfigParser()
config.read(os.path.join(path,"BEALLITASOK.cfg"), encoding = "utf-8")
logger = Logger()
logger.init()

def ctime(dtformat : str = "%H:%M:%S"):
    """
    A jelenlegi időt színesen visszaadó kódsor.
    Formátum a 'dtformat' megadásával változtatható.\n
    Alapértelmezett formátum: '%H:%M:%S'
    """
    return "[" + colorama.Fore.CYAN+ datetime.datetime.now().strftime(dtformat) + "]"

def face_counter(faces : list):
    """
    Érzékelt arcok számának logfájlba illetve konzolba való kiíratása.
    """
    logger.wrtie_log(config["BEALLITASOK"]["arcok_szama"].replace("!arcok", str(len(faces))))
    print(ctime() + colorama.Fore.MAGENTA + config["BEALLITASOK"]["arcok_szama"].replace("!arcok",colorama.Fore.YELLOW + (str(len(faces))))) 

def mask_found():
    """
    Maszk érzékelésnek logfájlba illetve konzolba való kiíratása.
    """
    logger.wrtie_log(config["BEALLITASOK"]["van_maszk"])
    print(ctime() + colorama.Fore.GREEN + config["BEALLITASOK"]["van_maszk"])

def mask_not_found():
    """
    Maszk érzékelés hiányának logfájlba illetve konzolba való kiíratása.
    """
    logger.wrtie_log(config["BEALLITASOK"]["nincs_maszk"])
    print(ctime() + colorama.Fore.RED + config["BEALLITASOK"]["nincs_maszk"])

