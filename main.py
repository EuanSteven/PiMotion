#!/usr/bin/python3
#----------------------------------------------------------------------------
# Created By   : Euan Steven
# Created Date : September 2022
# Version      : 1.5
# ---------------------------------------------------------------------------

import time
from gpiozero import MotionSensor
import RPi.GPIO as GPIO
from PIL import Image, ImageOps
import numpy as np
from picamera2 import Picamera2

print("Importing Tensorflow...")
import tensorflow 
from tensorflow import keras
print("Imported Tensorflow!")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
servoPIN = 17
GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 50)

sensor = MotionSensor(4)

picam2 = Picamera2()
preview_config = picam2.create_preview_configuration()
picam2.configure(preview_config)
picam2.start()

def servo():
    p.start(2.5) 
    p.ChangeDutyCycle(5)
    time.sleep(0.5)
    p.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    p.ChangeDutyCycle(10)
    time.sleep(0.5)
    p.ChangeDutyCycle(12.5)
    time.sleep(0.5)
    p.ChangeDutyCycle(10)
    time.sleep(0.5)
    p.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    p.ChangeDutyCycle(5)
    time.sleep(0.5)
    p.ChangeDutyCycle(2.5)
    time.sleep(0.5)

def process():
    tensorflow.get_logger().setLevel('INFO')
    model = tensorflow.keras.models.load_model('./model/model.h5', compile=False)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open('./image/motion.jpg')
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    if float(prediction[0][1]) > 0.5:
        print("No Pigeon")
    else:
        print("Pigeon")
        servo()

def motion():
    print("Motion Detected!")
    picam2.capture_file("./image/motion.jpg")
    process()
    time.sleep(20)
    print("Paused...")

print("Detecting...")

try:
    while True:
      sensor.wait_for_motion()
      motion()
except KeyboardInterrupt:
      print("")
      print("Exiting...")
      exit(0)



