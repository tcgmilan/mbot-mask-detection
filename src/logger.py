import datetime
import os
class Logger:
    def __init__(self):
        self.path = "/home/pi/mbot-mask-detection"
        self.current_time = "[" + datetime.datetime.now().strftime("%Y/%m/%d - %H:%M:%S") + "]"
    def init(self):
            open(os.path.join(self.path, self.current_time + ".txt"), "w", encoding = "utf-8")
            self.log_file = open(os.path.join(self.path, self.current_time + ".txt"), "a", encoding = "utf-8")
    def wrtie_log(self, text : str):
        self.log_file.write(text + "\n")
        
