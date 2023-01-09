from scene import *
import math
import random
import console

class TextError(Exception):
	pass

class textEngine(Node):
	def __init__(self, defaultPos = (0,0), defaultFont = ('Avenir'), defaultSize = 20, defaultEndWait = 3, defaultInterval = 1, defaultZ_Position = 1, *args, **kwargs):
		Node.__init__(self, *args, **kwargs)
		self.defaultPos = defaultPos
		self.defaultFont = defaultFont
		self.defaultSize = defaultSize
		self.defaultEndWait = defaultEndWait
		self.defaultInterval = defaultInterval
		self.defaultZ_Position = defaultZ_Position
		
			#all parents that are needed
		#used for text images, everything that is related to images, excluding the images of text itself
		self.textImgs = Node(parent = self)
		#used for the images of the text itself
		self.textParent = Node(parent = self)
		#used for questions
		self.askParent = Node(parent = self)
		
			#all sprites that need to kept thoughtout the program
		self.textBox = SpriteNode(position = self.defaultPos, parent = self.textImgs, alpha = 0)
		self.textBox.anchor_point = (0, 1)
		
			#important lists
		#contains all default values
		self.defaults = {}
		#holds the actual infomation of the text
		self.ALLTEXTINFO = []
		#a dictionary with all names and their coresponding textbox images
		self.TEXTBOXDIC = {}
		#a dictionary with dictionaries that are the presets the user made
		self.TEXTPRESETS = {}
	
			#general important vars
		self.counter = 0
		self.touchActive = False
		self.textReceiver = (False, "")
		self.touchPos = (-10,-10)
		self.prevTouchPos = (-10, -10)
		self.doSelection = False
		
			#vars used for the writing
		self.writingIndex = 0
		self.writePos = self.defaultPos
		self.endWaitTimer = 0
		
			#some last setup stuff
		self.defaults = {"endWait": self.defaultEndWait, "position": self.defaultPos, "font": self.defaultFont, "size": self.defaultSize, "interval": self.defaultInterval,  "addToParent": self.textParent, "textWrap": 500}
		self.error = TextError
		
	def addTextBox(self, name, textBox):
		self.TEXTBOXDIC.update({name: textBox})
	
	def createPreset(self, name, preset):
		self.TEXTPRESETS.update({name: preset})
	
	def touch_b(self, touch):
		self.touchActive = True
		self.touchPos = touch.location
		self.prevTouchPos = touch.location
		self.doSelection = False
	
	def touch_m(self, touch):
		self.touchPos = touch.location
		self.prevTouchPos = touch.prev_location
	
	def touch_e(self, touch):
		self.touchActive = False
		self.touchPos = (-10, -10)
		self.doSelection = True
	
		#functions for questions
	def ask(self, default = None, askTime = "tap", heading = "-", **kwargs):
		#function used to get all needed values ready
			#asign answers to questions
		qaHolder, qHolder = [], []
		qS, aS = 0, 0
		for key, value in kwargs.items():
			if key[0] == "q":
				qS += 1
				qaHolder.append({value: None})
				qHolder = [key, value]
			elif key[0] == "a":
				index = 0
				aS += 1
				for pair in qaHolder:
					for pairKey in pair:
						if pair.get(pairKey) == None:
							index = 1
							pair.update({pairKey: value})
				if index == 0: raise self.error('Unmatched answer "%s = %s"' % (key, value))
			else:
				raise self.error('Unknown kwarg "%s"' % (key))
		if qS > aS:
			raise self.error('Unmatched question "%s = %s"' % (qHolder[0], qHolder[1]))
		if len(qaHolder) == 0:
			raise self.error('No question/answer arguments provided')
		
			#test for errors
		try:
			#is an integer
			askTime + 1
			if askTime <= 0:
				raise self.error('Invalid askTime: "%s"' % (askTime))
			if default == None:
				raise self.error('askTime given, but no default given')
		except:
			#is a string
			if askTime != "tap":
				raise self.error('Unknown askTime: "%s"' % (askTime))
		
		#package the question/answer values so they can be used
		QA = {}
		for qa in qaHolder:
			QA.update(qa)
		#put all ask values into ALLTEXTINFO
		askInfo = {"qa": QA, "default": default, "askTime": askTime, "heading": heading}
		try:
			self.ALLTEXTINFO[-1].update({"pairedAsk": askInfo})
		except:
			raise self.error('Missing "write" function to pair "ask" function to')
			
		#functions for the regular writing, without quesitons
	def write(self, speaker, text, endWait = -1, interval = -1, font = -1, size = -1, position = -1, startFunction = "False", endFunction = "False", addToParent = -1, textWrap = -1, preset = {}):
			#find the default values, and use them if need be
		textBoxTexture = self.TEXTBOXDIC.get(speaker)
		info = {"text": text, "speaker": speaker, "endWait": endWait, "interval": interval, "font": font, "size": size, "position": position, "textBoxTexture": textBoxTexture, "startFunction": startFunction, "endFunction": endFunction, "addToParent": addToParent, "textWrap": textWrap, "pairedAsk": None}
		info.update(self.setupWritingValues(info, preset))
		self.ALLTEXTINFO.append(info)
	
	def setupWritingValues(self, info, preset):
		returnDic = dict(info)
		regValues = {}
		#get default values for values not used
		for key in returnDic:
			if returnDic.get(key) == -1:
				returnDic.update({key: self.defaults.get(key)})
			else:
				regValues.update({key: info.get(key)})
		#set presets
		try:
			acutalPreset = self.TEXTPRESETS.get(preset)
		except:
			acutalPreset = {}
		#problem, NoneType object is not iterable
		try:
			returnDic.update(acutalPreset)
		except:
			pass
		#set said values
		returnDic.update(regValues)
		return returnDic
		
	def actuallyWrite(self):
		if len(self.ALLTEXTINFO) == 0:
			return
		t = self.ALLTEXTINFO[0]
		if self.writingIndex == 0:
			self.setupImages(t)
			self.textReceiver = (True, str(t.get("startFunction")))
		if self.writingIndex != len(str(t.get("text"))):
			#code runs if there is still some stuff to write
			if t.get("interval") != 0:
				if self.counter % t.get("interval") == 0 or self.writingIndex == 0 or self.touchActive == True:
					writeInstantly = False
				else:
					return
			elif t.get("interval") == 0:
				writeInstantly = True
			if self.touchActive == True:
				writeInstantly = True
			while True:	
				character = LabelNode(str(t.get("text"))[self.writingIndex], parent = t.get("addToParent"), font = (t.get("font"), t.get("size")))
				character.anchor_point = (0, 1)
				self.getPosition(t)
				character.position = self.writePos
				self.writingIndex += 1
				if writeInstantly is False or self.writingIndex == len(str(t.get("text"))):
					break
		else:
			#used to bypass the timer at end, used by ask
			#code runs if the writing stuff is over, and it is time for the end stuff
			if self.endWaitTimer == 1: #Ehhhhhh dont like this, fix- the endwaittimer increase by one before this check happens, which is the problem- maybe change the position of the endwait to happen before everything is reset?
				self.textReceiver = (True, str(t.get("endFunction")))
				#ASK STUFF, DO STUFF HERE
				if t.get("pairedAsk") == None:
					pass
				else:
					a = t.get("pairedAsk")
					#setup when to end the ask function
					self.ALLTEXTINFO[0].update({"endWait": a.get("askTime")})
					self.writePos = (self.writePos[0], self.writePos[1] - t.get("size") - 2)
					for i in a.get("qa").keys():
						print(a.get("qa").keys()) #removing causes bugs
						console.clear()
						questionParent = Node(parent = self.askParent)#, position = (t.get("position")[0], self.writePos[1] - (t.get("size") - 2)*2))
						#have newInfo default to current info, with an update
						newInfo = dict(t)
						#endWait is never called
						#font, size, and textWrap and set by default
						newInfo.update({"text": " " + str(a.get("heading")) + str(i), "speaker": None, "interval": 0, "position": (t.get("position")[0], self.writePos[1] - (t.get("size") - 2)*2), "textBoxTexture": None, "startFunction": "True", "endFunction": str(" " + str(a.get("heading"))), "addToParent": questionParent, "pairedAsk": None})
						#manually call actuallyWrite()
						self.ALLTEXTINFO.insert(0, newInfo)
						self.writingIndex = 0
						self.actuallyWrite()
						#setup position for next iter
						self.ALLTEXTINFO.pop(0)
					self.writingIndex = len(str(t.get("text")))
			
			if t.get("pairedAsk") == None: #determines if a it is a write ending or an ask ending
				#if it is a write ending
				if (self.endWaitTimer == t.get("endWait") * 60) or (self.touchActive == True and t.get("endWait") == "tap"):
					#if either the timer has expired or the creator wants the user to tap through
					self.writeEnd(t)
			else:
				#if it is an ask ending
				a = t.get("pairedAsk")
				index = 0
				for parent in self.askParent.children:
					for child in parent.children: #currently very crude, fix later
						if child.frame.contains_point(self.prevTouchPos): #and self.touchPos = (-10, -10):
							if self.doSelection == True:
								self.doSelection = False
								answers = a.get("qa").values()
								tempList = []
								for i in answers:	
									tempList.append(i)									
								self.textReceiver = (True, str(tempList[index]))
								self.askEnd(t, a)
								return
							else:
								parent.x_scale = 1.1
								return
					parent.x_scale = 1
					index += 1		
					#if the user must choose an answer
				if a.get("askTime") != "tap":
					if a.get("askTime") * 60 == self.endWaitTimer:
						self.askEnd(t, a)
						self.textReceiver = (True, str(a.get("default")))
					#if the user must choose an answer before the time runs out
					
			self.endWaitTimer += 1 #hmmmmm problem?
	
	def askEnd(self, t, a):
		self.writeEnd(t)
		for child in self.askParent.children:
			child.run_action(Action.remove())
	
	def writeEnd(self, t):
		self.endWaitTimer = 0
		self.ALLTEXTINFO.pop(0)
		self.writingIndex = 0
		if t.get("addToParent") == self.textParent:
			for child in self.textParent.children:
				child.run_action(Action.remove())
		if len(self.ALLTEXTINFO) > 0:
			if self.TEXTBOXDIC.get(self.ALLTEXTINFO[0].get("speaker")) == None:
				self.textBox.alpha = 0
		else:
			self.textBox.alpha = 0

	def setupImages(self, info):
		#check to make sure that the user wants a textbox
		if self.TEXTBOXDIC.get(info.get("speaker")) == None:
			return
		self.textBox.texture = Texture(self.TEXTBOXDIC.get(info.get("speaker")))
		self.textBox.position = (info.get("position")[0] - info.get("size"), info.get("position")[1] + info.get("size")/2)
		self.textBox.alpha = 1
		
	def getPosition(self, t):
		if self.writingIndex == 0:
			self.writePos = t.get("position")
		else:
			if self.writePos[0] > t.get("textWrap"): #changing the number changes where the text wrap starts
				if t.get('text')[self.writingIndex] != " ": #tests whether the line starts with a space
					tempList = []
					#for text wrap					
					for i in range(1, 11):
						if t.get("addToParent").children[-i].text == " ":
							#used to find which letters need to be put on the next line
							break
						else:
							tempList.append(t.get("addToParent").children[-i])
							if i == 10:
								tempList = [] #deletes the stuff inside from the parent?
					#if the list is empty, then add a hypen
					if len(tempList) == 0:
						newPos = (self.writePos[0] + t.get("addToParent").children[-2].frame.w - 0.5, self.writePos[1])
						character = LabelNode("-", parent = t.get("addToParent"), font = (t.get("font"), t.get("size")), position = newPos)
						character.anchor_point = (0, 1)
						#START FROM POSITION OF THE INDENT
						if t.get("startFunction") == "True":
							self.writePos = (t.get("position")[0] + self.getLength(t.get("endFunction"), t.get("size"), t.get("font")), self.writePos[1] - t.get("size") - 2)
							b = self.ALLTEXTINFO[0].get("text")
							self.ALLTEXTINFO[0].update({"text": b[:self.writingIndex + 1] + " " + b[self.writingIndex + 1:]}) 
						else:
							self.writePos = (t.get("position")[0], self.writePos[1] - t.get("size") - 2)
					#otherwise throw the words down a line
					else:
						if t.get("startFunction") == "True":
							self.writePos = (t.get("position")[0] + self.getLength(t.get("endFunction"), t.get("size"), t.get("font")), self.writePos[1] - t.get("size") - 2)
						else:
							self.writePos = (t.get("position")[0], self.writePos[1] - t.get("size") - 2)
						tempList.reverse()
						tempList.pop(-1)
						for character in tempList:
							character.position = self.writePos
							self.writePos = (self.writePos[0] + character.frame.w - 0.5, self.writePos[1])
			else:
				self.writePos = (self.writePos[0] + t.get("addToParent").children[-2].frame.w - 0.5, self.writePos[1])		

	def getLength(self, text, size, font):
		#a function that lets me get the length of a line of text
		length = 0
		testText = LabelNode("", font = (font, size))
		for character in text:
			testText.text = character
			length += testText.frame.w - 0.5
		return length
		
	def update(self):
		try:
			if self.counter == self.ALLTEXTINFO[0].get("interval"):
				self.counter = 0
			self.counter += 1
		except:
			self.counter = 0
		self.actuallyWrite()
		if self.touchActive == True:
			# so you cant hold down and skip all text
			self.touchActive = False
		if self.doSelection == True:
			self.doSelection = False
	#used to test textEngine class
'''
class testClass(Scene):
	def setup(self):
		self.text = textEngine(parent = self)
		self.text.addTextBox("leo", None)
		self.text.createPreset("test", {"interval": 0, "endFunction": "print('yeet')"})
		self.text.write("leo", "we've got text wrap. we've got variable speeds. this is so much better then my first version of a text engine. however, there is still a long ways to go.", position = (10, 500), startFunction = "print('hi')", endFunction = 'print("done")', preset = "test", endWait = "tap")
		self.text.write("leo", "heloooooooooooooooooooo abcdefg hijklmno", position = (10, 500), textWrap = 600, endWait = 10)
		self.text.ask(heading = "-", q3 = "say that you are sorry because this is tired and theprogram better work now", a3 = "self.test()", q = "aghksfjkhj", a = "self.yeet()", q1 = 2, a1 = "self.peet()", askTime = 3, default = "self.test()")
		#self.text.write("leo", "yeet", position = (300,500), size = 20)
		
	def update(self):
		self.text.update()
		if self.text.textReceiver[0] == True:
			eval(str(self.text.textReceiver[1]))
			self.text.textReceiver = (False, "")
	def touch_began(self, touch):
		self.text.touchActive = True
		self.text.touchPos = touch.location
		self.text.prevTouchPos = touch.location
		self.text.doSelection = False
	
	def touch_moved(self, touch):
		self.text.touchPos = touch.location
		self.text.prevTouchPos = touch.prev_location
	
	def touch_ended(self, touch):
		self.text.touchActive = False
		self.text.touchPos = (-10, -10)
		self.text.doSelection = True
	
	def test(self):
		self.text.write("leo", "first option", position = (10, 500), textWrap = 600)
	
	def yeet(self):
		print("yeet")
	
	def peet(self):
		print("peet")
run(testClass())
'''
