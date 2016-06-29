from CCH import CCH

class SDCCH(CCH):
	
	def __init__(self,n,slot):
		CCH.__init__(self)
		self.name = "SDCCCH"
		if slot==0: 
			n += 4
			s = n/2
			s *= 10
			s += 2
			s += (n%2)*4
			print "config SDCCH",n,range(s,s+4)
			self.config = (range(s,s+4),0)
		elif slot==1:
			s = n*4
			print "config SDCCH",n,range(s,s+4)
			self.config = (range(s,s+4),1)
		


