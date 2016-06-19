class CH:
	def __init__(self):
		pass
	def attach(self,C):
		for f in C.frame:
			for x in f:
				if x.__class__==self.__class__.__burst__:
					x.attach(self)
	def deattach(self,C):
		for f in C.frame:
			for x in f:
				if x.__class__==self.__class__.__burst__:
					x.deattach()
