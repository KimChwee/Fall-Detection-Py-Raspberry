# Fall detector settings class
#
#
# Kim Salmi, kim.salmi(at)iki(dot)fi
# http://tunn.us/arduino/falldetector.php
# License: GPLv3

# 01-Jun-2018: Original version only detects Not Moving
# Modified the codes to detect fall
# Once fall is detected, alarm will be activated
# A couple of services can be enabled when alarm is set
# Available services: SMS, Email with screen shot of the fall moment

class Settings(object):
	
	def __init__(self):
		self.debug = 1 # boolean
		self.source = './storedvideos/fallc009b.avi'#0 # camera source
		#self.source = './storedvideos/fall.avi'#0 # camera source
		#self.source = './storedvideos/fall3.avi'#0 # camera source
		#self.source = './storedvideos/stand.avi'#0 # camera source
		#self.source = './storedvideos/sit2.avi'#0 # camera source
		self.bsMethod = 1 #1 # listed in bs.py
		self.MOG2learningRate = 0.1 #0.001 #0 means that the background model is not updated at all, 1 means that the background model is completely reinitialized from the last frame.
		self.MOG2shadow = 0 #shadow detection boolean
		self.MOG2history = 100 #the number of last frames that affect the background model.
		self.MOG2thresh = 20 #the variance threshold for the pixel-model match.
		self.minArea = 150*150 # 50*50 minimum area to be considered as a person
		self.thresholdLimit = 100 #50 the higher the number, the less sensitive to movements
		self.dilationPixels = 30 # dilate thresh
		self.useGaussian = 0 # boolean
		self.useBw = 1 # 1 means use Grayscale
		self.useResize = 1 # boolean
		self.gaussianPixels = 31
		self.movementMaximum = 500 # amount to move to still be the same person
		self.movementMinimum = 3 # minimum amount to move to not trigger alarm
		self.movementTime = 50 # number of frames after the alarm is triggered
		self.location = 'Living Room'
		self.phone = '01010101010'
		#self.email = 'steve.tan.chee.wei@gmail.com'
		self.email = 'testing@gmail.com'
		self.apiKey = ""   #update your API here
		self.alarmImagesFolder = "alarms"
