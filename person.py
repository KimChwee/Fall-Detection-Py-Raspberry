# Fall detector Person class
#
# Kim Salmi, kim.salmi(at)iki(dot)fi
# http://tunn.us/arduino/falldetector.php
# License: GPLv3

# 01-Jun-2018: Original version only detects Not Moving
# Modified the codes to detect fall
# Once fall is detected, alarm will be activated
# A couple of services can be enabled when alarm is set
# Available services: SMS, Email with screen shot of the fall moment

class Person(object):
	"""Person"""
	amount = 0

	def __init__(self, x, y, w, h, movementMaximum, movementMinimum, movementTime):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.movementTime = movementTime
		self.movementMaximum = movementMaximum
		self.movementMinimum = movementMinimum
		self.lastmoveTime = 0
		self.alert = 0
		self.alarmReported = 0
		self.lastseenTime = 0
		self.remove = 0
		Person.amount += 1
		if Person.amount > 1000:
			Person.amount = 0
		self.id = Person.amount
		x = 0
		h = 0

	def samePerson(self, x, y, w, h):
		same = 0
		if x+self.movementMaximum > self.x and x-self.movementMaximum < self.x:
			if y+self.movementMaximum > self.y and y-self.movementMaximum < self.y:
				same = 1
		return same

	def editPerson(self, x, y, w, h):
		if abs(x-self.x) > self.movementMinimum or abs(y-self.y) > \
		self.movementMinimum or abs(w-self.w) > self.movementMinimum or \
		abs(h-self.h) > self.movementMinimum:
			self.lastmoveTime = 0
		#debug
		#print(self.id, self.w, w, self.h, h)
		if x != 0:
                        if abs(w/self.w) >= 1.5 and abs(h/self.h) <= 1.2:
                                self.alert = 1

		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.lastseenTime = 0

	def getId(self):
		return self.id

	def tick(self):
		self.lastmoveTime += 1
		self.lastseenTime += 1
		#Not moving alert is only triggered after a fall is detected
		if self.lastmoveTime > self.movementTime and self.alert == 1: #50:
			self.alert = 2
			#debug
			#print("Not Moving")
		if self.lastseenTime > 4: # how many frames ago last seen
			self.remove = 1
			
	def getAlert(self):
		return self.alert

	def getRemove(self):
		return self.remove


class Persons:
	def __init__(self, movementMaximum, movementMinimum, movementTime):
		self.persons = []
		self.movementMaximum = movementMaximum
		self.movementMinimum = movementMinimum
		self.movementTime = movementTime
		Person.amount = 0

	def addPerson(self, x, y, w, h):
		person = self.familiarPerson(x, y, w, h)
		if person:
			person.editPerson(x, y, w, h)
			return person
		else:
			person = Person(x ,y ,w ,h , self.movementMaximum, 
				self.movementMinimum, self.movementTime)
			self.persons.append(person)
			return person
		
	def familiarPerson(self, x, y, w, h):
		for person in self.persons:
			if person.samePerson(x, y, w, h):
				return person
		return None

	def tick(self):
		for person in self.persons:
			person.tick()
			if person.getRemove():
				self.persons.remove(person)
