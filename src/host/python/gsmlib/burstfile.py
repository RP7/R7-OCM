from FB import FB
from SB import SB
from NB import NB
from DB import DB
from Burst import Burst
import numpy as np

class burstfile:
	burst = {'FB':FB,'SB':SB,'NB':NB,'DB':DB}
	def __init__(self,fn):
		self.f = open(fn)
	def readBurst(self):
		t = self.f.readline()
		t = t.split()
		b = burstfile.burst[t[1]]()
		b.fn = int(t[0])
		d = self.f.readline()
		d = d.replace('[','')
		d = d.replace(']','')
		r = [int(x) for x in d.split(',')]
		b.recv = Burst.short2Complex(r)
		return b

	def close(self):
		self.f.close()


def findT(b):
	p = np.zeros(6)
	for i in range(6):
		b.training = i
		b.chnEst()
		peek = np.abs(b.chn)
		p[i]=peek[peek.argmax()]
	return p.argmax()
def main():
	import matplotlib.pyplot as plt
	from NB import NBTraining
	fn = "../../../../temp/log"
	f = burstfile(fn)
	tlist = [1,5,2,5,0,2,2,2]
	for i in range(8):
		b = f.readBurst()
		if b.__class__.__name__=='NB':
			if tlist[i%8]==5:
				b.training = tlist[i%8]
				b.chnEst()
				b.viterbi_detector()
				# np.savetxt("../../../../data/nbmafi",b.mafi)
				# np.savetxt("../../../../data/nbrhh",b.rhh)
				# np.savetxt("../../../../data/nbtraining",NBTraining.modulated[5,:])
				# break
				print "0",b.nbm0
				print "1",b.nbm1
				plt.plot(np.abs(b.cut_chn))
		if b.__class__.__name__=='SB':
			p = b.peekS()
			#plt.plot(p)
	print tlist
	plt.show()
	f.close()

if __name__ == '__main__':
	main()