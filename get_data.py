#!/usr/bin/env python

import time
from picamera import PiCamera

def camara():
   
    with PiCamera() as camera:
        #camera.resolution = (2592, 1944) # camera max
        #camera.resolution = (1920, 1080) # 1080p
        camera.resolution = (1280, 720)   # 720p
        #camera.resolution = (320, 240)
        # Camera warm-up time
        time.sleep(0)
        camera.capture('image.jpg')

    print('Picture taken')

camara()
        
