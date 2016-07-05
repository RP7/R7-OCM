from fractions import Fraction
from FB import FB
from CH import CH
from config import *
import numpy as np
from Burst import Burst

class FCCH(CH):
	__burst__ = FB
	__freq__ = Fraction(6500000,24)
	def __init__(self):
		CH.__init__(self)
		self.name="FCCH"

	def callback(self,b,fn,state):
		if b.__class__!=FCCH.__burst__:
			raise BurstError
			return
		omg = b.freqEst()
		freq = omg * SampleRate
		#print "FCCH freq = ",freq
		#print "FFT method",b.freqEstFFT(int(SampleRate))
		return 1,b.recv

	def find(self,rawmf,osr):
		cc = 0
		c = []
		buf = np.frombuffer(rawmf,dtype=np.int16)
		c = np.zeros((len(buf)/2-1),dtype=int)

		for i in range(len(buf)/2-1):
			r = int(buf[i*2+2])*int(buf[i*2+1])-int(buf[i*2])*int(buf[i*2+3])
			if r>0:
				cc += 1
			else:
				cc -= 1
			c[i]=cc
		l = int(osr*Burst.length)
		nc = c[l:]-c[:-l]
		return nc

