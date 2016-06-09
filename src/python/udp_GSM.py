import GSM
from ctypes import *

class udp_GSM(GSM.GSMChan):
	def __init__(self,rd):
		self.framerate = 1.92e6
		self.nframes = len(rd)
		GSM.GSMChan.__init__(self,rd)

	