import splibs
import numpy as np
from Burst import *

class FBFix(item):
	length = 142
	bits = [0]*142

class FB(Burst):

	__field__ = [TB,FBFix,TB,NGP]
	__name__ = "FB"

	def __init__(self):
		Burst.__init__(self)

	def freqEst(self):
		r0 = splibs.autocorrelation(self.recv[Burst.small_overlap:-Burst.small_overlap],1)
		omg = np.angle(r0)/(2.*np.pi)
		return omg

	def freqEstFFT(self,fs):
		t = np.zeros(fs,dtype=complex)
		t[:len(self.recv)]=self.recv
		ft = np.abs(np.fft.fft(t))
		p = ft.argmax()
		if p>fs/2:
			p-=fs
		return p



def main():
	a = FB()
	a.dump()
	print a.getLen()

if __name__ == '__main__':
	main()
