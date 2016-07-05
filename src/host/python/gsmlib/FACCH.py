from TCH import TCH

class FACCH(TCH):
	
	def __init__(self,slot):
		TCH.__init__(self)
		self.name = "FACCH"
		self.config = (range(0,26),slot)
		
	def callback(self,b,fn,state):
		b.training = state.bcc
		return TCH.callback(self,b,fn,state)


