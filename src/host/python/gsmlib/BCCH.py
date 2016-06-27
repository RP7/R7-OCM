from NB import NB
from CH import CH
from config import *
from GSM import *
import numpy as np
class BCCH(CH):
	__burst__ = NB
	def __init__(self):
		CH.__init__(self)
		self.msg = [[]]*4
	
	def callback(self,b,fn,state):
		if state.timingSyncState.state==2:
			b.training = state.bcc
			b.chnEst()
			b.viterbi_detector()
			if fn>1 and fn<6:
				self.msg[fn-2]=b.msg
			if fn == 5:
				self.decode()
		return 'ok',None

	def decode(self):
		print "One Bcch"

	def attach(self,C):
		for i in range(2,6):
			f = C.frame[i]
			x = f[0]
			x.attach(self)
	
	def deattach(self,C):
		for i in range(2,6):
			f = C.frame[i]
			x = f[0]
			x.deattach()