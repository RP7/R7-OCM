from NB import NB
from CH import CH
from config import *
from GSM import *
import numpy as np
from interleave import interleave
from convCode import convCode

class CCH(CH):
	__burst__ = NB
	def __init__(self):
		CH.__init__(self)
		self.msg = [[]]*4
		self.il = interleave(57*8,57*2) 
		self.codec = convCode(convCode.cch_config)
	
	def callback(self,b,fn,state):
		if state.timingSyncState.state==2:
			b.training = state.bcc
			b.chnEst()
			b.viterbi_detector()
			if fn>1 and fn<6:
				self.msg[fn-2]=b.msg
			if fn == 5:
				self.decode(state)
				if self.codec.parity_check(self.decoded_data)!=0:
					print "fn",b.fn,"sn",b.sn,"error",self.codec.last_error
				else:
					print "Bcch ok"
		return 'ok',None

	def decode(self,state):
		if state.bcch_log!=None:
			print >>state.bcch_log,self.msg
		self.coded = np.array(self.msg[0]+self.msg[1]+self.msg[2]+self.msg[3])
		self.deil = self.il.decode(self.coded)
		self.decoded_data = self.codec.conv_decode(self.deil)

	