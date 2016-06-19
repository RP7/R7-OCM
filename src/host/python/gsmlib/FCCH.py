from fractions import Fraction
from FB import FB
from CH import CH
from config import *

class FCCH(CH):
	__burst__ = FB
	__freq__ = Fraction(6500000,24)
	def __init__(self):
		CH.__init__(self)

	def callback(self,b,fn):
		if b.__class__!=FCCH.__burst__:
			raise BurstError
			return
		omg = b.freqEst()
		freq = omg * SampleRate
		print "FCCH freq = ",freq

