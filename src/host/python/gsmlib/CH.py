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

	def compress_bits(self,sbuf):
		dbuf = []
		for i in range(0,len(sbuf),8):
			c = 0
			k = 1
			for x in sbuf[i:i+8]:
				c += k*x
				k *= 2
			dbuf.append(c)
		return dbuf
