from NB import NB
from CH import CH
from config import *
from GSM import *
import numpy as np
from interleave import interleave
from convCode import convCode
from gsmtap import gsmtap
from clib import clib
from ctypes import *

class TCH(CH):
	__burst__ = NB
	def __init__(self):
		CH.__init__(self)
		self.msg = [[]]*8
		self.il = interleave(57*8,57*2,"TCH") 
		self.codec = convCode(convCode.cch_config)
		self.tap = gsmtap()
		self.lib = None
	
	def setLib(self,lib):
		self.lib = clib(lib)

	def callback(self,b,fn,state):
		if self.lib != None:
			return self.callback_c(b,fn,state)
		if state.timingSyncState.state==2:
			sfn = fn % MultiFrameT
			sfn8 = sfn
			if sfn8==12:
				return 'SACCH',None
			if sfn8>12:
				sfn8 -= 1
			sfn8 %=8
			b.chnEst()
			b.viterbi_detector()
			self.msg[sfn8]=b.msg
			if (sfn8%4) == 3:
				suc = self.decode(state,sfn8)
				if suc==0:
					return 'nodata',None
				if self.codec.parity_check(self.decoded_data)!=0:
					print "fn %d(%d)"%(b.fn,fn),"sn",b.sn,"error",self.codec.last_error
				else:
					self.data = (c_int8*23)()
					self.data[:] = self.compress_bits(self.decoded_data[:184])
					#print state.t1,state.t2,state.t3,self.name,"ok","msg",self.data
					self.tap.send(self,self._fn(state,fn-sfn8%4))
					return "newdata",self.data
		return 'ok',None

	def callback_c(self,b,fn,state):
		if state.timingSyncState.state==2:
			(r,s) = self.config
			sfn = fn % MultiFrameC
			if sfn in r:
				self.msg[sfn-r[0]]=self.lib.newBurst(b.srecv)
			if sfn == r[-1]:
				pc,aCch = self.lib.doCch(self.msg,b.training)
				if pc!=0:
					print "fn %d(%d)"%(b.fn,fn),"sn",b.sn,"error"
				else:
					self.data = aCch.out
					self.tap.send(self,self._fn(state,fn-sfn+r[0]))
					return "newdata",self.data
		return 'ok',None
	def decode(self,state,off):
		self.coded = np.array(self.msg[0]+self.msg[1]+self.msg[2]+self.msg[3]+self.msg[4]+self.msg[5]+self.msg[6]+self.msg[7])
		if len(self.coded)!=8*114:
			return 0
		if off==3:
			self.deil = self.il.decodeTCH(self.coded,1)
		else:
			self.deil = self.il.decodeTCH(self.coded,0)
		self.decoded_data = self.codec.conv_decode(self.deil)
		return 1
	
	def attach(self,C,p):
		(r,s) = self.config
		for fs in range(0,len(C.frame),p):
			for i in r:
				f = C.frame[i+fs]
				x = f[s]
				x.attach(self)
	
	def deattach(self,C,p):
		(r,s) = self.config
		for fs in range(0,len(C.frame),p):
			for i in r:
				f = C.frame[i+fs]
				x = f[s]
				x.deattach()

	def _fn(self,state,fn):
		#tt = ((state.t3 + 26) - state.t2) % 26
		lfn = (51 * state.t1) + fn
		#print state.t1,state.t2,state.t3,fn,tt,lfn
		return lfn