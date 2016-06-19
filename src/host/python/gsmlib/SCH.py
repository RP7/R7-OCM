from fractions import Fraction
from SB import SB
from CH import CH
from config import *
from GSM import *

class SCH(CH):
	__burst__ = SB
	def __init__(self):
		CH.__init__(self)

	def callback(self,b,fn):
		p = b.peek(SampleRate/SymbolRate)
		pos = p.argmax()
		print pos

	
		