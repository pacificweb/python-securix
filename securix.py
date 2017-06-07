#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import logging
import os
import time
import subprocess
import picamera
from gpiozero import MotionSensor
from datetime import datetime

log = logging.getLogger(__name__)

class MotionLogic:

    def __init__(self, pin):

        # Constantes
        self.captureWidth = 1920                # The video file will be scaled down using "Width" and "Height" to reduce noise.
        self.captureHeight = 1440               # Setting these to more than 1920x1440 seems to cause slowdown (records at a lower framerate)
        self.framerate = 15                     # Video file framerate.
        self.bitrate = 0                        # default is 17000000
        self.quantization = 20                  # 10 is very high quality, 40 is very low. Use bitrate = 0 if quantization is non-zero.
        self.filepath = "/tmp/"                 # Local file path for video files
        self.convertToMp4 = False               # Requires GPAC to be installed. Removes original .h264 file
        self.useDateAsFolders = True            # Creates folders with current year, month and day, then saves file in the day folder.
        self.isRecording = False                # Is the camera currently recording? Prevents stopping a camera that is not recording.
        self.filename = ""
        self.mp4name = ""
        self.folderPath = ""

        # Reduction
        self.videoReduction = 3
        self.Width = int(self.captureWidth / self.videoReduction)
        self.Height = int(self.captureHeight / self.videoReduction)

        # Camera
        self.Camera = picamera.PiCamera()
        time.sleep(2)
        self.Camera.exposure_mode = "auto"
        self.Camera.image_effect = "none"
        self.Camera.exposure_compensation = 0
        self.Camera.ISO = 0
        self.Camera.brightness = 50
        self.Camera.contrast = 0
        self.Camera.resolution = ( self.captureWidth, self.captureHeight )
        self.Camera.framerate = self.framerate
        self.Camera.meter_mode = "average"      # Values are: average, spot, matrix, backlit

        # Detecteur de mouvement
        self.Sensor = MotionSensor(pin)

	# Methods -------------------------------------------------------------------------------------------------
    def Notify(self):
        _filename = time.strftime('%Y%m%d%H%M%S') + '.jpg'
        self.Camera.capture(_filename, resize=(self.Width/2, self.Height/2))
        subprocess.Popen(['sudo', 'python', 'notify.py', _filename])

    def Dispose(self):
        if self.isRecording:
            self.Camera.stop_recording()
            self.Camera.stop_preview()
            self.Camera.close()
        del self.Camera
        del self.Sensor

	# Camera ------------------------------------------------------------------------------------------------------

    def StartRecording(self):
        if not self.isRecording:

            current_hour = datetime.now().hour
            if current_hour >= 21 and current_hour <= 5:
                self.Camera.exposure_mode = "night"
            else:
                self.Camera.exposure_mode = "auto"

            self.Notify()

            ts = datetime.now()
            if self.useDateAsFolders:
                self.folderPath = self.filepath +"%04d%02d%02d" % ( ts.year, ts.month, ts.day )
                if not os.path.exists(self.folderPath):
                    os.makedirs(self.folderPath)
                self.filename = self.folderPath + "/" + "%02d%02d%02d.h264" % ( ts.hour, ts.minute, ts.second )
            else:
                self.filename = self.filepath + "%04d%02d%02d%02d%02d%02d.h264" % (ts.year,ts.month,ts.day,ts.hour,ts.minute,ts.second)

            self.mp4name = self.filename[:-4] + "mp4"
            self.Camera.start_preview()
            self.Camera.start_recording(self.filename, resize=(self.Width, self.Height), quantization=self.quantization, bitrate=self.bitrate)
            self.isRecording = True

    def StopRecording(self):
        if self.isRecording:
            self.Camera.stop_preview()
            self.Camera.stop_recording()
            self.isRecording = False
            self.ToMP4()

	# Output video Converter
    def ToMP4(self):
        subprocess.Popen([ "sh", "mp4box.sh", str(self.framerate), self.filename, self.mp4name])

	# CAMERA END ---------------------------------------------------------------------------------------------------------------
        
	# Sensor -----------------------------------------
    def StartSensor(self):
        self.Sensor.when_motion = self.OnMotionStart
        self.Sensor.when_no_motion = self.OnMotionStop

	# Sensor Events
    def OnMotionStart(self):
        log.info("OnMotionStart")
        self.StartRecording()
	
    def OnMotionStop(self):
        log.info("OnMotionStop")
        self.StopRecording()
	# Sensor -----------------------------------------

##################################################################################################################################################
#
# TODO - GET OPTIONS
# TODO - PIR CLASS, CAMERA CLASS, MAIN THREAD CLASS, NOTIFY CLASS
#

def main(args=None):

    logging.basicConfig(filename='securix.log',datefmt='%Y-%m-%d %I:%M:%S',format='%(levelname)s : %(asctime)s %(message)s',level=logging.DEBUG)

    logic = MotionLogic(7)
    logic.StartSensor()

    print "Securix (CTRL+C to exit)"
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt):
        print('exit(0)')
    finally:
        logic.Dispose()
        del logic
        log.info("Shutdown")
        sys.exit()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
