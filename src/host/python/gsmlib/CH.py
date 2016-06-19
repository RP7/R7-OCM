class CH:
	def __init__(self):
		pass
	def attach(self,C):
		for x in C.multiframe:
			if x.__class__==self.__class__.__brust__:
				x.attach(self)
	def deattach(self,C):
		for x in C.multiframe:
			if x.__class__==self.__class__.__brust__:
				x.deattach()
