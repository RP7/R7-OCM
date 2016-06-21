import numpy as np
from Burst import *
import splibs

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
		0,1,0,0,0,1,0,1,
		0,1,1,1,0,1,1,0,
		0,0,0,1,1,0,1,1]
	unmodulated = np.array(bits)*2 - 1
	modulated = item.gmsk_mapper(bits,complex(0.,-1.))
		
class SB(Burst):

	__field__ = [TB,SBM0,SBTraining,SBM1,TB,NGP]
	__name__ = "SB"

	def __init__(self):
		Burst.__init__(self)

	def peekL(self,ovs):
		f = self.mapLData()
		return np.abs(self.channelEst(f,SBTraining.modulated,ovs))
	
	def peekS(self,ovs):
		self.ovs = ovs
		self.chn = self.channelEst(self.recv,SBTraining.modulated,ovs)
		return np.abs(self.chn)
	
	def setChEst(self,pos):
		self.trainingPos = pos
		self.chn_len = int(Burst.CHAN_IMP_RESP_LENGTH*self.ovs)
		self.cut_chn,self.cut_pos = splibs.maxwin(self.chn[pos-32:pos+32],self.chn_len)
		self.cut_pos += pos-32
		self.bs = self.cut_pos-int(TB.length+SBM0.length)*self.ovs
		self.ibs = int(self.bs)
		self.timing = self.bs-self.ibs
		self.be = self.ibs+int(Burst.length*self.ovs+self.chn_len+1)
		self.rhh = splibs.matchFilter(self.chn[self.cut_pos:self.cut_pos+self.chn_len*2],self.cut_chn,self.ovs,0.)
		self.mafi = splibs.matchFilter(self.recv[self.ibs:self.be],self.cut_chn,self.ovs,self.timing)
		
	@staticmethod
	def overheadL():
		return TB.length+SBM0.length+Burst.large_overlap
	@staticmethod
	def overheadS():
		return TB.length+SBM0.length+Burst.small_overlap

def main():
	a = SB()
	a.dump()
	print a.getLen()
	print len(SBTraining.modulated)

if __name__ == '__main__':
	main()

