#!/usr/bin/env python
#-*- coding: utf-8 -*-

import picamera
import time

filename = time.strftime('%Y%m%d%H%M%S') + '.jpg'
with picamera.PiCamera() as camera:
    #camera.resolution = (640, 480)
    camera.capture(filename)
    #camera.start_preview()
    #time.sleep(5)
    #camera.start_recording('foo.h264')
    #camera.wait_recording(10)
    #camera.stop_recording()
    #camera.stop_preview()
