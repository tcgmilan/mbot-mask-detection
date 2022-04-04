# M5 : masKey
# Fő program elindulásáért felelős python kód
# https://github.com/tcgmilan/mbot-mask-detection

# Arc, maszk érzékelésért felelős kód, valamint a logger előkészítése.
from src.detect import start_detecting
from src.logger import Logger

def main():
    logger = Logger()
    logger.init()
    start_detecting()

if __name__ == '__main__':
    main()