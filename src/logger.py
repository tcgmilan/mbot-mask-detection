# M5 : masKey
# Logoláslért felelős python kód
# https://github.com/tcgmilan/mbot-mask-detection

# Idővel, rendszerkezeléssel kapcsolatos modulok
import datetime
import os

class Logger:
    """
    Logfájlba valamint a konzolkimenetre való kiíratás.
    Színes betűk elérhetőek!
    Az üzenetek minden esetben pontos dátummal vannak ellátva.
    A logfájlok a /logs mappában találhatóak, a létrehozás dátumaival címkézve.
    .txt formátumban kezelve az egyszerű elérhetőségért, olvasásért, kezelésért.
    """
    def __init__(self):
        self.path = "/home/pi/mbot-mask-detection/"
        self.current_time = "[" + datetime.datetime.now().strftime("%Y:%m:%d-%H:%M:%S") + "]"
    def init(self):
            open(os.path.join(self.path, self.current_time + ".txt"), "w+", encoding = "utf-8")
            self.log_file = open(os.path.join(self.path, self.current_time + ".txt"), "a", encoding = "utf-8")
    def wrtie_log(self, text : str):
        self.log_file.write(text + "\n")
        
