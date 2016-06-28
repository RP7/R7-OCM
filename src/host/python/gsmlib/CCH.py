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
					self.data = self.compress_bits(self.decoded_data[:184])
					print state.t1,state.t2,state.t3,self.__name__,"ok",self.__type__[state.t1%8],"msg",self.data
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