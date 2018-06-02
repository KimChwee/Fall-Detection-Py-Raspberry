# Fall detection main

# 01-Jun-2018: Original version only detects Not Moving
# Modified the codes to detect fall
# Once fall is detected, alarm will be activated
# A couple of services can be enabled when alarm is set
# Available services: SMS, Email with screen shot of the fall moment

import video
import time
import sys
import numpy as np
import cv2
import time

video = video.Video()
time.sleep(1.0)   #let camera autofocus + autosaturation settle
video.nextFrame()
video.testBackgroundFrame()

while 1:
        #get next frame of video
        video.nextFrame()
        video.testBackgroundFrame() #press n to delete background?
        video.updateBackground()
        video.compare()
        video.showFrame()
        video.testSettings()
        k = cv2.waitKey(30) & 0xff
        #if video.testDestroy():
        if k == 27:
                break

#video.release()
cv2.destroyAllWindows()
sys.exit()
