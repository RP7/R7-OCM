from fractions import Fraction
from SB import SB
from CH import CH
from config import *
from GSM import *

class SCH(CH):
	__burst__ = SB
	def __init__(self):
		CH.__init__(self)
		self.hit = {}
		self.osr = float(SampleRate/SymbolRate)

	def callback(self,b,fn):
		p = b.peek(self.osr)
		pos = p.argmax()
		print "find at",pos
		if pos in self.hit:
			self.hit[pos] += 1
		else:
			self.hit[pos] = 1
		return 1,p

	def frameStart(self):
		ov = SB.overhead()
		print "ov",ov
		p = 0
		h = 0
		for pos in self.hit:
			if self.hit[pos]>h:
				h=self.hit[pos]
				p = pos
		print "final find at",p
		p -= int(ov*self.osr)
		self.hit = {}
		return p



	
		