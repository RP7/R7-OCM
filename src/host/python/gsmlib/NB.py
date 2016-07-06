from Burst import *
import splibs
import viterbi_detector

class NBMessage(item):
	length = 57

class NBM0(NBMessage):
	pass

class NBM1(NBMessage):
	pass

class LoanFlag(item):
	length = 1

class LF0(LoanFlag):
	pass

class LF1(LoanFlag):
	pass

class NBTraining(item):
	"""
	const BitVector2 GSM::gTrainingSequence[] = {
    BitVector2("00100101110000100010010111"),
    BitVector2("00101101110111100010110111"),
    BitVector2("01000011101110100100001110"),
    BitVector2("01000111101101000100011110"),
    BitVector2("00011010111001000001101011"),
    BitVector2("01001110101100000100111010"),
    BitVector2("10100111110110001010011111"),
    BitVector2("11101111000100101110111100"),
	};
	"""
	length = 26
	bits = [
	  [0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1],
	  [0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1],
	  [0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0],
	  [0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0],
	  [0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1],
	  [0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0],
	  [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1],
	  [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0],
	  [0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1] ## DUMMY
	]
	modulated = np.zeros((len(bits),length),dtype=complex)
	for i in range(6):
		modulated[i,:] = item.gmsk_mapper(bits[i],complex(1,0)) 
	for i in range(6,len(bits)):
		modulated[i,:] = item.gmsk_mapper(bits[i],complex(-1,0)) 


class NB(Burst):

	__field__ = [TB,NBM0,LF0,NBTraining,LF1,NBM1,TB,NGP]
	__name__ = "NB"
	_chn_s = int((TB.length+NBM0.length+1)*Burst.osr)
	_chn_e = int((TB.length+NBM0.length+LF0.length+NBTraining.length+Burst.CHAN_IMP_RESP_LENGTH+2*Burst.small_overlap)*Burst.osr)

	def __init__(self):
		Burst.__init__(self)
		self.viterbi = viterbi_detector.viterbi_detector(5,2+TB.length+NBM0.length+LF0.length,NBTraining.modulated[0,:])

	def chnEst(self):
		self.chn = self.channelEst(self.recv[NB._chn_s:NB._chn_e],NBTraining.modulated[self.training,:])
		self.chn9 = self.channelEst(self.recv[NB._chn_s:NB._chn_e],NBTraining.modulated[8,:])
		if max(np.abs(self.chn9))>max(np.abs(self.chn)):
			return 0
		self.cut_chn,self.cut_pos = splibs.maxwin(self.chn,Burst.chn_len)
		pos = self.cut_pos+NB._chn_s
		#print "cut pos",self.cut_pos,"pos",pos,len(self.cut_chn),Burst.chnMatchLength,len(self.chn)
		self.bs = pos-float(TB.length+NBM0.length+LF0.length)*Burst.fosr #maybe wrony
		self.ibs = int(self.bs)
		self.timing = self.bs-self.ibs
		self.be = self.ibs+int(Burst.length*Burst.fosr+Burst.chn_len+1)
		return 1
	def viterbi_detector(self):
		self.viterbi.f_r_i = 1
		self.viterbi.b_r_i = 0
		self.viterbi.setTraining(NBTraining.modulated[self.training,:],1,1)
		rhh = splibs.matchFilter( 
			  self.chn[self.cut_pos:self.cut_pos+Burst.chnMatchLength]
			, self.cut_chn
			, Burst.fosr
			, 0. )/float(NBTraining.length)

		self.rhh = np.zeros(3*2-1,dtype=complex)
		self.rhh[3-len(rhh):3]=np.conj(rhh[::-1])
		self.rhh[3:3+len(rhh)-1]=rhh[1:]

		self.mafi = splibs.matchFilter(self.recv[self.ibs:self.be],self.cut_chn,Burst.fosr,self.timing)
		self.viterbi.table(self.rhh)
		self.a = self.viterbi.forward(self.mafi[61+26-2:])
		self.b = self.viterbi.backward(self.mafi[:61+2])
		self.nbm0 = self.viterbi.dediff_backward(self.b,0,NBTraining.bits[self.training][3])[2:-4]
		self.nbm1 = self.viterbi.dediff_forward(self.a,1,NBTraining.bits[self.training][-4])[4:-2]
		self.msg = self.nbm0[3:-1]+self.nbm1[1:-3]
		self.stolen = [self.nbm0[-1],self.nbm1[0]]

def main():
	a = NB()
	a.dump()
	print a.getLen()

if __name__ == '__main__':
	main()

