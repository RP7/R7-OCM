from CCH import CCH
from config import *
from GSM import *
import numpy as np


class BCCH(CCH):
	
	def __init__(self,slot):
		CCH.__init__(self)
		self.config = (range(2,6),slot)
		self.name = "BCCH"
		
	def callback(self,b,fn,state):
		b.training = state.bcc
		return CCH.callback(self,b,fn,state)



