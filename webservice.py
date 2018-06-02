# Fall detector webservice
#
# Kim Salmi, kim.salmi(at)iki(dot)fi
# http://tunn.us/arduino/falldetector.php
# License: GPLv3
import requests
import os

class Webservice(object):
	
	def __init__(self, place, phone, email, apiKey):
		#self.url = 'http://tunn.us/tools/healthservice/add.php?place='+place+'&phone='+phone
		#self.url = 'http://salmi.pro/ject/fall/add.php?place='+place+'&phone='+phone
		self.url = 'https://api.mailgun.net/v3/sandbox09688ba028104ae0bec1d690ebc67a37.mailgun.org/messages'
		self.recipients = email
		self.apiKey = apiKey
		self.mailbody = "Help!!"
		#self.data = '' #attach the image to be shown in the body

	def send_email(self, subject, attachment):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		file_path = os.path.join(dir_path,attachment)

		return requests.post(
			self.url,
			auth=("api", self.apiKey),
			files=[("attachment", (attachment, open(file_path, "rb").read()))],
			data={"from": "Mailgun Sandbox <postmaster@sandbox09688ba028104ae0bec1d690ebc67a37.mailgun.org>",
			      "to": self.recipients,
			      "subject": subject,
				  "text": self.mailbody})

	def alarm(self, detectiontype, personid, attachment):
		#tempurl = self.url
		#tempurl = tempurl+'&type=+'+detectiontype+'&personid='+str(personid)
		#response = requests.get(tempurl, data=self.data)
		#print response
		subject = 'Alarm triggered due to '+detectiontype+' by person id '+str(personid)
		print (subject + ' with attachment: ' + attachment)
		self.send_email(subject, attachment)


