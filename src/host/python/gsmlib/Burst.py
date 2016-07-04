from fractions import Fraction
import numpy as np
import config
import GSM as gsm
import struct
from ctypes import *

class item:
	def getLen(self):
		if hasattr(self,"field"):
			l = 0
			for x in self.field:
				l += x.getLen()
			return l
		else:
			return self.__class__.length

	@staticmethod
	def gmsk_mapper( inp, start_point ):
		inpb = np.array(inp)*2 - 1
		o = start_point
		out = [o]
		previous_symbol = inpb[0]
		for current_symbol in inpb[1:]:
			encoded_symbol = current_symbol * previous_symbol
			o = complex(0,1)*encoded_symbol*o
			out.append(o)
			previous_symbol = current_symbol
		return np.array(out)

	@staticmethod
	def c2bits(cbits):
		r = []
		for x in cbits:
			r.append(int(x))
		return r

class TB(item):
	length = 3
	bits = [0,0,0]

class ATB(item):
	length = 8
	bits = [0]*length

class NGP(item):
	length = Fraction(33,4)

class AGP(item):
	length = Fraction(273,4)

class Burst:
	length = Fraction(625,4)
	small_overlap = 25
	large_overlap = length
	mmap = None
	CHAN_IMP_RESP_LENGTH = 5
	osr = config.SampleRate/gsm.SymbolRate
	fosr = float(osr)
	chn_len = int(CHAN_IMP_RESP_LENGTH*osr)
	chnMatchLength = int(chn_len+(CHAN_IMP_RESP_LENGTH+2)/2.*fosr)
	
	small_overlap_sample = int(small_overlap*osr)
	large_overlap_sample = int(large_overlap*osr)
	
	log = None
	
	def __init__(self):
		if hasattr(self.__class__,"__field__"):
			self.field = [ x() for x in self.__class__.__field__]
		else:
			self.field = []
		self.fn = 0
		self.sn = 0
		self.ch = None
	
	def set(self,fn,sn):
		self.fn = fn
		self.sn = sn
		self.pos = Burst.length*(fn*8+sn)

	def getLen(self):
		if hasattr(self,"field"):
			l = 0
			for x in self.field:
				l += x.getLen()
			return l
		else:
			return self.__class__.length

	def dump(self):
		name = [n.__name__ for n in self.__class__.__field__]
		print name

	def attach(self,CH):
		self.ch = CH

	def deattach(self):
		self.ch = None

	def channelEst( self, frame, training):
		t = np.conj(training)
		inx = np.floor(np.arange(len(training))*Burst.fosr)
		last = int(inx[-1]+1)
		out = np.zeros(len(frame)-last,dtype=complex)
		for k in range(len(out)):
			slc = frame[k:]
			s = slc[inx.astype(int)]
			r = np.dot(s,t)
			out[k] = r
		return out
	
	@staticmethod
	def short2Complex(data):
		nframes = len(data)/2
		frame = np.array([complex(data[2*i],data[2*i+1]) for i in range(nframes)])
		return frame
	
	def mapRfData(self):
		if mmap==None:
			raise NoInstall
			return
		s = int(self.pos-Burst.small_overlap)
		l = int(Burst.length+2*Burst.small_overlap)
		self.srecv = mmap(s,l)
		self.recv = Burst.short2Complex(self.srecv)

	def mapLData(self):
		if mmap==None:
			raise NoInstall
			return
		s = int(self.pos-Burst.large_overlap)
		l = int(Burst.length+2*Burst.large_overlap)
		return Burst.short2Complex(mmap(s,l))

	def default_callback(self,fn,state):
		if Burst.log != None:
			self.toFile(Burst.log,fn)
	def toFile(self,f,fn):
		f.write(self.__class__.__name__)
		if mmap==None:
			raise NoInstall
			return
		s = int(self.pos-Burst.small_overlap)
		l = int(Burst.length+2*Burst.small_overlap)
		r = mmap(s,l)
		f.write(struct.pack('<hhhq',len(r)/2,self.sn,self.fn,fn))
		f.write(string_at(addressof(r),len(r)*2))
