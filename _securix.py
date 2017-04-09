#!/usr/bin/env python
#-*- coding: utf-8 -*-

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    subprocess.call(['mpg123','-q', 'gpio_failed.mp3'])

import sys
import time
import subprocess
import picamera

def OnDetection(channel):
    filename = time.strftime('%Y%m%d%H%M%S') + '.jpg'
    Camera.capture(filename)
    subprocess.Popen(['python', 'alert.py'])
    subprocess.Popen(['python', 'sendmail.py', filename])

def main(args=None):

    subprocess.call(['mpg123','-q', 'welcome.mp3'])
    subprocess.call(['mpg123','-q', 'script_test.mp3'])
    subprocess.call(['python', 'alert.py'])
    subprocess.call(['mpg123','-q', 'internet_test.mp3'])
    subprocess.call(['mpg123','-q', 'internet_test_success.mp3'])


    GPIO.setmode(GPIO.BCM)
    channel = 7
    try:
        GPIO.setup(channel, GPIO.IN)
        GPIO.add_event_detect(channel, GPIO.RISING)
        GPIO.add_event_callback(channel, OnDetection)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    global Camera
    Camera = picamera.PiCamera()
    Camera.resolution = (640, 480)
    time.sleep(2)   #camera warmup

    subprocess.call(['mpg123','-q', 'ready.mp3'])

    print "Securix (CTRL+C to exit)" 
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt):
        print('')
    finally:
        GPIO.cleanup()
        del Camera
        sys.exit()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)

