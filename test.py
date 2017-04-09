
#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import time
import subprocess

def main(args=None):
#
    #subprocess.call(['python', 'sendmail.py', 'capture.jpg'])
    #subprocess.call(['mpg123', 'welcome.mp3'])
    #subprocess.call(['mpg123', 'script_test.mp3'])
    #subprocess.call(['python', 'alert.py'])
    #subprocess.call(['mpg123', 'internet_test.mp3'])
    #subprocess.call(['mpg123', 'internet_test_success.mp3'])

    try:
        while True:
            time.sleep(1)
            print(time.strftime('%Y-%m-%d %H:%M:%S'))
    except (KeyboardInterrupt):
        print('')
    finally:
        sys.exit()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)

