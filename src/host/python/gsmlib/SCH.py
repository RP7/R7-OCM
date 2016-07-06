from fractions import Fraction
from SB import SB
from CH import CH
from config import *
from GSM import *
import numpy as np
from convCode import convCode

class SCH(CH):
	__burst__ = SB
	
	"""
	  ncc =
	    (decoded_data[ 7] << 2)  |
	    (decoded_data[ 6] << 1)  |
	    (decoded_data[ 5] << 0);
	  bcc = 
	    (decoded_data[ 4] << 2)  |
	    (decoded_data[ 3] << 1)  |
	    (decoded_data[ 2] << 0);
	  t1 =
	    (decoded_data[ 1] << 10) |
	    (decoded_data[ 0] << 9)  |
	    (decoded_data[15] << 8)  |
	    (decoded_data[14] << 7)  |
	    (decoded_data[13] << 6)  |
	    (decoded_data[12] << 5)  |
	    (decoded_data[11] << 4)  |
	    (decoded_data[10] << 3)  |
	    (decoded_data[ 9] << 2)  |
	    (decoded_data[ 8] << 1)  |
	    (decoded_data[23] << 0);
	  t2 =
	    (decoded_data[22] << 4)  |
	    (decoded_data[21] << 3)  |
	    (decoded_data[20] << 2)  |
	    (decoded_data[19] << 1)  |
	    (decoded_data[18] << 0);
	  t3p =
	    (decoded_data[17] << 2)  |
	    (decoded_data[16] << 1)  |
	    (decoded_data[24] << 0);

	  t3 = 10 * t3p + 1;
	"""
	_fields_ = {"ncc":[7,6,5],"bcc":[4,3,2],"t1":[1,0,15,14,13,12,11,10,9,8,23],"t2":[22,21,20,19,18],"t3p":[17,16,24]}
	def __init__(self):
		CH.__init__(self)
		self.name = "SCH"
		self.hit = {}
		self.osr = float(SampleRate/SymbolRate)
		self.ovL = int(SB.overheadL()*self.osr)
		self.ovS = int(SB.overheadS()*self.osr)
		self.codec = convCode(convCode.sch_config)

	def callback(self,b,fn,state):
		if state.timingSyncState.state==1:
			p = b.peekL()
			pos = p.argmax()-self.ovL
		elif state.timingSyncState.state==2:
			p = b.peekS()
			pos = p.argmax()

			b.setChEst()
			b.viterbi_detector()
			self.msg = b.sbm0[3:]+b.sbm1[:-3]
			"""
			self.decoded_data = self.conv_decode()
			self.decode()
			if self.parity_check()!=0:
				print "fn",b.fn,"sn",b.sn,"error",self.last_error
			else:
				state.bcc = self.info['bcc']
			"""
			self.decoded_data = self.codec.conv_decode(self.msg)
			self.decode()
			if self.codec.parity_check(self.decoded_data)!=0:
				print "fn",b.fn,"sn",b.sn,"error",self.codec.last_error
			else:
				state.bcc = self.info['bcc']
				state.ncc = self.info['ncc']
				state.t1 = self.info['t1']
				state.t2 = self.info['t2']
				state.t3 = self.info['t3']
				sys_fn = self.sysLongFN()
				state.diff_fn = sys_fn - fn
				#print state.t1,state.t2,state.t3,state.diff_fn,sys_fn
				
			pos -= self.ovS

			
		if pos in self.hit:
			self.hit[pos] += 1
		else:
			self.hit[pos] = 1
		return 1,p

	def frameStart(self):
		p = 0
		h = 0
		for pos in self.hit:
			if self.hit[pos]>h:
				h=self.hit[pos]
				p = pos
		r = 0

		for x in range(p-2,p+3):
			if x in self.hit:
				r += self.hit[x]

		self.hit = {}
		return p,r

	def sysLongFN(self):
		tt = ((self.info['t3'] + 26) - self.info['t2']) % 26
		fn = self.info['t1']*51*26 + tt*51 + self.info['t3']
		self.info['lfn'] = fn
		return fn
 

	def decode(self):
		self.info = {}
		for d in SCH._fields_:
			l = SCH._fields_[d]
			m = 0
			for p in l:
				m *= 2
				m += self.decoded_data[p]
			self.info[d]=m
		self.info['t3']=self.info['t3p']*10+1
		return self.info

	def decodeBin(self,bin):
		self.info = {}
		for d in SCH._fields_:
			l = SCH._fields_[d]
			m = 0
			for p in l:
				m *= 2
				m += (bin>>p)&1
			self.info[d]=m
		self.info['t3']=self.info['t3p']*10+1
		return self.info
