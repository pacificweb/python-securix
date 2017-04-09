
#!/usr/bin/env python
#-*- coding: utf-8 -*-

import subprocess
import time

print(time.strftime('%Y-%m-%d %H:%M:%S'))
subprocess.call(['mpg123','-q', 'detection.mp3']) 
for index in range(0,0):
    subprocess.call(['aplay','-q' ,'/home/pi/sounds/alert.wav']) 
