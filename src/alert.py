import random
import pyttsx3

class Alert:

    def __init__(self):
        self.engine = pyttsx3.init()

    def init(self):
        self.warnings = [x for x in open("figyelmeztetesek.txt", "r")]
        for x in self.engine.getProperty("voices"):
            print(x)
        self.engine.setProperty("voice", "com.apple.speech.synthesis.voice.mariska")

    def read_warning(self):
        self.engine.say(random.choice(self.warnings))
        self.engine.runAndWait()

a = Alert()
a.init()
