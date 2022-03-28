from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
from src.alert import Alert

import numpy as np
import imutils
import time
import cv2
import os

proto_txt_path = "/home/pi/mbot-mask-detection/dataset/deploy.prototxt"
weights_path = "/home/pi/mbot-mask-detection/dataset/res10_300x300_ssd_iter_140000.caffemodel"
mask_detector_model = "/home/pi/mbot-mask-detection/dataset/mask_detector.model"
face_net = cv2.dnn.readNet(proto_txt_path, weights_path)
mask_net = load_model(mask_detector_model)

def calculate_mask(frame, face_net, mask_net):
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
    face_net.setInput(blob)
    detections = face_net.forward()

    faces = []
    locs = []
    preds = []
    print(faces)
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
    if len(faces):
        faces = np.array(faces, dtype = "float32")
        preds = mask_net.predict(faces, batch_size = 32)

    return (locs, preds)

def start_detecting():
    alert = Alert()
    alert.init()
    vs = VideoStream(src = 0).start()
    time.sleep(2.0)
    i=1
    while True:
        print("Frame "+ str(i))
        i += 1
        frame = vs.read()
        frame = imutils.resize(frame, width = 400)

        (locs, preds) = calculate_mask(frame, face_net, mask_net)

        for (box, pred) in zip(locs, preds):
            (start_x, start_y, end_x, end_y) = box
            (mask, without_mask) = pred

            if without_mask > mask:
                print("Nincs maszk!")
                alert.read_warning()
                time.sleep(3.0)
                
        #cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
