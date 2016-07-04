from CCH import CCH

class CCCH(CCH):
	
	def __init__(self,n,slot):
		CCH.__init__(self)
		self.name = "CCCH"
		n += 1
		s = n/2
		s *= 10
		s += 2
		s += (n%2)*4
		print "config CCCH",n,range(s,s+4)
		self.config = (range(s,s+4),slot)
		
	def callback(self,b,fn,state):
		b.training = state.bcc
		return CCH.callback(self,b,fn,state)


