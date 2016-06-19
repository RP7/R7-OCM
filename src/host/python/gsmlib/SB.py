import numpy as np
from Burst import *

class SBMessage(item):
	length = 39

class SBM0(SBMessage):
	pass

class SBM1(SBMessage):
	pass

class SBTraining(item):
	length = 64
	bits = [
		1,0,1,1,1,0,0,1,
		0,1,1,0,0,0,1,0,
		0,0,0,0,0,1,0,0,
		0,0,0,0,1,1,1,1,
		0,0,1,0,1,1,0,1,
		1,0,1,0,0,1,0,1,
		0,1,1,1,0,1,1,0,
		0,0,0,1,1,0,1,1]
	modulated = item.gmsk_mapper(bits,complex(0.,-1.))
		
class SB(Burst):

	__field__ = [TB,SBM0,SBTraining,SBM1,TB,NGP]
	__name__ = "SB"

	def __init__(self):
		Burst.__init__(self)

	def peek(self,ovs):
		f = self.mapLData()
		return np.abs(self.channelEst(f,modulated,ovs))

def main():
	a = SB()
	a.dump()
	print a.getLen()
	print len(SBTraining.modulated)

if __name__ == '__main__':
	main()

