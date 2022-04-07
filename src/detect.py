# M5 : masKey
# Érzékelésért felelős python kód
# https://github.com/tcgmilan/mbot-mask-detection

# Tensorflow mesterséges inteligencia szükséges elemeinek betöltése
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

# Kamera képét visszaadó modul
from imutils.video import VideoStream

# Egyéb, saját kódok (figyelmeztetés, beállításkezelő, logoló)
from src.alert import Alert
from src.confconvert import to_bool, to_int
from src.clogger import mask_found, mask_not_found, face_counter

# Bonyolultabb tömbök, listák kezelésére hivatott könyvtár (numpy)
# Kamera képének feldolgozásához szükséges könyvtár (imutils)
# Program várakoztatásához szükséges könyvtár (time)
# Kamera kezelő modul (cv2)
# Rendszerkezelő modul (os)
# Színes konzolkimenet (colorama)
# .cfg fájl kezelő (configparser)
import numpy as np
import imutils
import time
import cv2
import os
import colorama
import configparser

# Színes kimenet inicializálása
# Különböző elérési utak, globális változók deklarálása
# Az arc és maszk érzékeléshez szükséges model fájlok, beállítások elérési útjának meghatározása
# Beállítások betöltése
colorama.init(autoreset = True)
path = "/home/pi/mbot-mask-detection/"
proto_txt_path = os.path.join(path, "dataset", "deploy.prototxt")
weights_path = os.path.join(path, "dataset", "res10_300x300_ssd_iter_140000.caffemodel")
mask_detector_model = os.path.join(path, "dataset", "mask_detector.model")
face_net = cv2.dnn.readNet(proto_txt_path, weights_path)
mask_net = load_model(mask_detector_model)
config = configparser.ConfigParser()
config.read(os.path.join(path,"BEALLITASOK.cfg"), encoding = "utf-8")

def calculate_mask(frame, face_net, mask_net):
    """
    Az adott képkockából való arc kinyerése, egy facenet segítségével,
    maszk keresés, majd az arcok illetve érzékelések visszaadása.
    A függvény két tömböt ad vissza magából melyek a pontos értékeket, arc pozíciókat,
    maszk detektálásának arányait tartalmazza. Segédfüggvény a program blokkokba való 
    osztására. A függvény kezdéskor bekér egy adott képkockát, egy archálót, és egy maszk
    hálót.
    """
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
    face_net.setInput(blob)
    detections = face_net.forward()

    faces = []
    locs = []
    preds = []
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3 : 7] * np.array([w, h, w, h])
            (start_x, start_y, end_x, end_y) = box.astype("int")
            (start_x, start_y,) = (max(0, start_x), max(0, start_y))
            (end_x, end_y,) = (max(0, end_x), max(0, end_y))
            face = frame[start_y : end_y, start_x : end_x]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)
            faces.append(face)
            locs.append((start_x, start_y, end_x, end_y))
    face_counter(faces)
    if len(faces):
        faces = np.array(faces, dtype = "float32")
        preds = mask_net.predict(faces, batch_size = 32)

    return (locs, preds)

def start_detecting():
    """
    A program fő részeként szolgáló függvény. Kezdéskor előkészíti a figyelmeztető részét
    a programnak, illetve a kamera képének feldolgozásáért felelős modulokat.
    Egy végtelen cikluson belüli ciklust, amely az adott képkocka arcainak pozícióját,
    és az adott arcokon lévő maszkok esélyeit tartalmazza, valamint a videókimenet állítását
    tartalmazza.
    """
    alert = Alert()
    alert.init()
    alert.read("A program elindult!")
    results = []
    vs = VideoStream(src = 0).start()
    time.sleep(2.0)
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width = 400)

        (locs, preds) = calculate_mask(frame, face_net, mask_net)

        for (box, pred) in zip(locs, preds):
            (mask, without_mask) = pred
            print("results: ", results)
            print("mask: "+ str(mask) + "\n womask: " + str(without_mask))
            if without_mask > mask:
                results.append(False)
                alert.read_warning()
                mask_not_found()
                time.sleep(to_int(config["BEALLITASOK"]["figyelmeztetes_varakozas"]))
            elif mask > without_mask:
                if results[-1] is False:
                    alert.read_award()
                    results.clear()
                results.append(True)
                mask_found()
            else: pass
        if to_bool(config["BEALLITASOK"]["video_kimenet"]):
            cv2.imshow("m5 maskey | maszk érzékelés", frame)
            
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break