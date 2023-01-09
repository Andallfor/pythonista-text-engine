import textEngine
from scene import *

class main(Scene):
	def setup(self):
		self.text = textEngine.textEngine(defaultFont = 'Fira Mono', parent = self)
		self.text.addTextBox("com", None)
		self.text.addTextBox("maf", None)
		self.text.createPreset("reg", {"position": (10, 550), "textWrap": 700})
		self.text.createPreset("mafia", {"position": (10, 550), "textWrap": 700, "font": 'Marker Felt'})
		self.text.write("com", "Hi there, this is a quick demonstration of a text engine that I created in python. All code used is my own (in the sense no line of code is copied, but certain commands, such as eval() where found online), and in total the text engine is about 360 lines long.", preset = "reg", interval = 2, endWait = "tap")
		self.start()
		
	def start(self):
		self.text.write("com", "The darkness closes in, and the voices grow louder. The sounds in your head are only compounded by the heavy footsteps of the Mafia racing behind you.", preset = "reg")
		self.text.write("maf", "THERE! I SEE HIM!", preset = "mafia")
		self.text.write("com", "The footsteps grow louder, then silent. Now, instead of footsteps, their panting breaths can be heard. They are right behind you.", preset = "reg")
		self.text.ask(q1 = "Attempt to fight the Mafia.", a1 = "self.fight()", q2 = "Attempt to plead with the Mafia.", a2 = "self.plead()", q3 = "Attempt to escape.", a3 = "self.escape()")	
		
		
	def fight(self):
		self.text.write("com", "You choose to fight. A foolish choice perhaps, but a choice neverless.", preset = "reg")
		self.text.write("com", "You lunge at them, fists already in motion. But your efforts are futile. A bullet is fired through your head, instantly killing you.", preset = "reg")	
		self.text.write("com", "You are dead. What did you expect?", preset = "reg")
		self.text.ask(q1 = "Start over.", a1 = "self.start()")
		
	def plead(self):
		self.text.write("maf", "So, finally come to your senses? Finally feeling some regret for deciving us?", preset = "mafia")
		self.text.write("maf", "I'll give you one last chance. Run away now and never come back, and you just might live.", preset = "mafia")
		self.text.ask(q1 = "Run.", a1 = 0)
		self.text.write("com", "You bolt away, your legs carrying you as fast as they can. The Mafia member laughs, and pulls out his gun.", preset = "reg")
		self.text.write("maf", "Too bad for you, but the Mafia really doesn't like traitors walking free.", preset = "mafia")
		self.text.write("com", "A bullet slams into your body, and you collapse, bleeding to death.", preset = "reg")
		self.text.ask(q0 = "Start over.", a5 = "self.start()")

	def escape(self):
		self.text.write("com", "You high tail it out of there, and just barely manage to escape.", preset = "reg")
		self.text.write("com", "Not a lot of content, but that's because its 4am and I still have 50k bugs to fix, and this is not meant for text games either.", preset = "reg")
		self.text.write("com", "Anyways, thanks.", preset = "reg")
	
		
		
		
	def update(self):
		self.text.update()
		if self.text.textReceiver[0] == True:
			eval(str(self.text.textReceiver[1]))
			self.text.textReceiver = (False, "")
			
	def touch_began(self, touch):
		self.text.touch_b(touch)
	
	def touch_moved(self, touch):
		self.text.touch_m(touch)
	
	def touch_ended(self, touch):
		self.text.touch_e(touch)

run(main())
