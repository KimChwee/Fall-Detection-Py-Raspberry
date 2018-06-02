# Fall detector
# Kim Salmi, kim.salmi(at)iki(dot)fi
# http://tunn.us/arduino/falldetector.php
# License: GPLv3

debug = 1
import cv2
import numpy as np
import time


def convertFrame (frame):
  r = 750.0 / frame.shape[1]
  dim = (750, int(frame.shape[0] * r))
  frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  if useGaussian:
    gray = cv2.GaussianBlur(gray, (gaussianPixels, gaussianPixels), 0)
  return frame, gray


# Video or camera
camera = cv2.VideoCapture(0)
# camera = cv2.VideoCapture("file.mov")
time.sleep(1.0)

firstFrame = None
start = time.time()
i = 0
lastH = [0]*100
lastW = [0]*100


# Detect parameters
minArea = 30*30
thresholdLimit = 20
dilationPixels = 20 # 10
useGaussian = 1
gaussianPixels = 31

# loop for each frame in video
while (1):
  detectStatus = "Empty"
  grabbed, frame = camera.read()
  frame, gray = convertFrame(frame)

  # eof
  if not grabbed:
    break
 
  # firstFrame (this should updated every time light conditions change)
  if firstFrame is None:
    time.sleep(1.0) # let camera autofocus + autosaturation settle
    grabbed, frame = camera.read()
    frame, gray = convertFrame(frame)
    firstFrame = gray
    continue

  # difference between the current frame and firstFrame
  frameDelta = cv2.absdiff(firstFrame, gray)
  thresh = cv2.threshold(frameDelta, thresholdLimit, 255, cv2.THRESH_BINARY)[1]
  thresh = cv2.dilate(thresh, None, iterations=dilationPixels) # dilate thresh
  _, contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, 
    cv2.CHAIN_APPROX_SIMPLE) #find contours
 
  for contour in contours:
    if cv2.contourArea(contour) < minArea:
      continue

    # Drawing rect over contour
    (x, y, w, h) = cv2.boundingRect(contour)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    if w > lastW[i]*3.0:
      print("Alarm: " + format(time.time()))
    #if lastH < h*1.20:
        #print("Alarm!")
    lastW[i] = w
    lastH[i] = h
#   cv2.putText(frame, "{}".format(cv2.contourArea(contour)), (x, y+h+20), 
#   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)
    cv2.putText(frame, "{}".format(i), (x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 
      (0, 140, 255), 1)
    detectStatus = "Ok"
    i+=1
  # Hud + fps
  if debug:
    end = time.time()
    seconds = end - start
    fps  = round((1 / seconds), 1)
    start = time.time()

    cv2.putText(frame, "Detect: {}".format(detectStatus), (10, 20), 
      cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 140, 255), 1)
    cv2.putText(frame, "FPS: {}".format(fps), (400, 20), 
      cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 140, 255), 1)
    cv2.imshow("frameDelta", frameDelta)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("firstFrame", firstFrame)

  cv2.imshow("Feed", frame)
  
  i = 0
  

  key = cv2.waitKey(1) & 0xFF
  if key == ord("q"):
    break
  if key == ord("n"):
    firstFrame = None
    

# Release and destroy
camera.release()
cv2.destroyAllWindows()
