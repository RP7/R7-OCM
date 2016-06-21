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
		self.ovL = int(SB.overheadL()*self.osr)
		self.ovS = int(SB.overheadS()*self.osr)
	def callback(self,b,fn,state):
		if state.timingSyncState.state==1:
			p = b.peekL(self.osr)
			pos = p.argmax()-self.ovL
		elif state.timingSyncState.state==2:
			p = b.peekS(self.osr)
			pos = p.argmax()

			b.setChEst(pos)

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

		for x in [p-1,p,p+1]:
			if x in self.hit:
				r += self.hit[x]

		self.hit = {}
		return p,r



	
		