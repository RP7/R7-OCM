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

class CCH(CH):
	__burst__ = NB
	def __init__(self):
		CH.__init__(self)
		self.msg = [[]]*4
		self.il = interleave(57*8,57*2) 
		self.codec = convCode(convCode.cch_config)
		self.tap = gsmtap()
		self.lib = None
	
	def setLib(self,lib):
		self.lib = clib(lib)

	def callback(self,b,fn,state):
		if self.lib != None:
			return self.callback_c(b,fn,state)
		if state.timingSyncState.state==2:
			b.chnEst()
			b.viterbi_detector()
			(r,s) = self.config
			sfn = fn % MultiFrameC
			if sfn in r:
				self.msg[sfn-r[0]]=b.msg
			if sfn == r[-1]:
				self.decode(state)
				if self.codec.parity_check(self.decoded_data)!=0:
					print "fn %d(%d)"%(b.fn,fn),"sn",b.sn,"error",self.codec.last_error
				else:
					self.data = (c_int8*23)()
					self.data[:] = self.compress_bits(self.decoded_data[:184])
					#print state.t1,state.t2,state.t3,self.name,"ok","msg",self.data
					self.tap.send(self,self._fn(state,fn-sfn+r[0]))
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
	def decode(self,state):
		if state.bcch_log!=None:
			print >>state.bcch_log,self.msg
		self.coded = np.array(self.msg[0]+self.msg[1]+self.msg[2]+self.msg[3])
		self.deil = self.il.decode(self.coded)
		self.decoded_data = self.codec.conv_decode(self.deil)

	"""
	static int compress_bits(unsigned char *dbuf, unsigned int dbuf_len,
		unsigned char *sbuf, unsigned int sbuf_len) {

		unsigned int i, j, c, pos = 0;

		if(dbuf_len < ((sbuf_len + 7) >> 3))
			return -1;

		for(i = 0; i < sbuf_len; i += 8) {
			for(j = 0, c = 0; (j < 8) && (i + j < sbuf_len); j++)
				c |= (!!sbuf[i + j]) << j;
			dbuf[pos++] = c & 0xff;
		}
		return pos;
	}
	"""
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