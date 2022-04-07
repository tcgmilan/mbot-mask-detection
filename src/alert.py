# M5 : masKey
# Figyelmeztetésért felelős python kód
# https://github.com/tcgmilan/mbot-mask-detection


# Véletlenszerű számok, elemek kiválasztásáért felelős modul (random)
# Szöveg felolvasásáért felelős modul (pyttsx3)
import random
import pyttsx3

class Alert:
    """
    Figyelmezetetést véghezvivő class. Létrehozáskor betölti a lehetséges figyelmeztetéseket,
    mellőzve a többszöri, felesleges beolvasást. A hang illetve nyelvkód az alapértelmezet Linux hangoknak
    felel meg.
    """
    def __init__(self):
        self.engine = pyttsx3.init()
    def init(self):
        self.warnings = [x for x in open("/home/pi/mbot-mask-detection/figyelmeztetesek.txt", "r")]        
        self.awards = [x for x in open("/home/pi/mbot-mask-detection/dicseretek.txt", "r")]
        self.engine.setProperty("voice", "hungarian")
    def read_warning(self):
        self.engine.say(random.choice(self.warnings))
        self.engine.runAndWait()
    def read_award(self):
        self.engine.say(random.choice(self.awards))
        self.engine.runAndWait()
    def read(self, text : str):
        self.engine.say(text)
        self.engine.runAndWait()
