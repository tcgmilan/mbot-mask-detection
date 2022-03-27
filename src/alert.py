import random
import pyttsx3

class Alert:

    def __init__(self):
        self.engine = pyttsx3.init()

    def init(self):
        self.warnings = [x for x in open("figyelmeztetesek.txt", "r")]
        self.engine.setProperty("voice", "hungarian")

    def read_warning(self):
        self.engine.say(random.choice(self.warnings))
        self.engine.runAndWait()
