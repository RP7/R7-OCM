from CCH import CCH
from config import *
from GSM import *
import numpy as np

class BCCH(CCH):
	def __init__(self):
		CCH.__init__(self)

	def attach(self,C):
		for i in range(2,6):
			f = C.frame[i]
			x = f[0]
			x.attach(self)
	
	def deattach(self,C):
		for i in range(2,6):
			f = C.frame[i]
			x = f[0]
			x.deattach()

