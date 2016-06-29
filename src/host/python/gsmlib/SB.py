import numpy as np
from Burst import *
import splibs
import viterbi_detector

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
	__viterbi_cut = 2	
	__viterbi_f = TB.length+SBM0.length+SBTraining.length - __viterbi_cut
	_chn_s = int((TB.length+SBM0.length)*Burst.osr)
	_chn_e = int((TB.length+SBM0.length+2*Burst.small_overlap)*Burst.osr)

	def __init__(self):
		Burst.__init__(self)
		self.viterbi = viterbi_detector.viterbi_detector(5,44,SBTraining.modulated)
		self.viterbi.setTraining(SBTraining.modulated,0,0)
	
		
	def peekL(self):
		f = self.mapLData()
		return np.abs(self.channelEst(f,SBTraining.modulated))
	
	def peekS(self):
		self.chn = self.channelEst(self.recv,SBTraining.modulated)
		return np.abs(self.chn)
	
	def setChEst(self):
		self.cut_chn,self.cut_pos = splibs.maxwin(self.chn[SB._chn_s:SB._chn_e],Burst.chn_len)
		self.cut_pos += SB._chn_s
		self.bs = self.cut_pos-int(TB.length+SBM0.length)*Burst.fosr #maybe wrony
		self.ibs = int(self.bs)
		self.timing = self.bs-self.ibs
		self.be = self.ibs+int(Burst.length*Burst.fosr+Burst.chn_len+1)
		if self.be>len(self.recv):
			print "----------------,channel bug","_chn_s",SB._chn_s,"_chn_e",SB._chn_e,"cut_pos",self.cut_pos,"s",self.ibs,"e",self.be,
			print "len",len(self.recv),"fn",self.fn,"sn",self.sn
	
	def viterbi_detector(self):
		rhh = splibs.matchFilter( 
			  self.chn[self.cut_pos:self.cut_pos+Burst.chnMatchLength]
			, self.cut_chn
			, Burst.fosr
			, 0. )/float(SBTraining.length)


		self.rhh = np.zeros(len(rhh)*2-1,dtype=complex)
		self.rhh[:len(rhh)]=np.conj(rhh[::-1])
		self.rhh[len(rhh):]=rhh[1:]

		self.mafi = splibs.matchFilter(self.recv[self.ibs:self.be],self.cut_chn,Burst.fosr,self.timing)
		self.viterbi.table(self.rhh)
		self.a = self.viterbi.forward(self.mafi[42+62:])
		self.b = self.viterbi.backward(self.mafi[:44])
		self.sbm0 = self.viterbi.dediff_backward(self.b,0,SBTraining.bits[3])[2:-4]
		self.sbm1 = self.viterbi.dediff_forward(self.a,0,SBTraining.bits[-4])[4:-2]
		#print "cut_pos",self.cut_pos,self.rhh[:]
		

	def tofile(self,p):
		self.save = { 'rhh':self.rhh
					, 'mafi':self.mafi
					, 'training':SBTraining.modulated
				}
		for f in self.save:
			np.savetxt(p+f,self.save[f])
	
	def fromfile(self,p):
		for f in self.save:
			self.save[f]=np.savetxt(p+f)
	

	@staticmethod
	def overheadL():
		# Bugs TB.length+SBM0.length Unit is Symbol, Burst.large_overlap Unit is Sample
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

