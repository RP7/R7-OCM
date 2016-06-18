from Burst import Burst
import numpy as np

class SB(Burst):
	def __init__(self):
		self.syncbits = [
0x01, 0x00, 0x01, 0x01, 0x01, 0x00, 0x00, 0x01,
0x00, 0x01, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01,
0x00, 0x00, 0x01, 0x00, 0x01, 0x01, 0x00, 0x01,
0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01,
0x00, 0x01, 0x01, 0x01, 0x00, 0x01, 0x01, 0x00,
0x00, 0x00, 0x00, 0x01, 0x01, 0x00, 0x01, 0x01 ]
		self.bits = [
		1,0,1,1,1,0,0,1,
		0,1,1,0,0,0,1,0,
		0,0,0,0,0,1,0,0,
		0,0,0,0,1,1,1,1,
		0,0,1,0,1,1,0,1,
		1,0,1,0,0,1,0,1,
		0,1,1,1,0,1,1,0,
		0,0,0,1,1,0,1,1]
		s = np.array(self.syncbits)*2-1
		self.sync = []
		for x in s:
			self.sync += [x,x,x,x] 

		self.training_seq = self.gmsk_mapper(s,complex(0.,-1.))
	
	def demodu(self,s):
		self.dem = self.diff(s)
		s = np.zeros(len(self.dem),dtype=complex)
		s[:len(self.sync)]=self.sync[:]
		fs = np.fft.fft(s)
		fd = np.fft.fft(self.dem)
		tr = np.abs(np.fft.ifft(fd*np.conj(fs)))
		return tr

	def channelEst( self, frame, osr ):
		inx = np.floor(np.arange(len(self.training_seq))*osr)
		last = int(inx[-1]+1)
		print len(frame)-last
		out = np.zeros(len(frame)-last,dtype=complex)
		for k in range(len(out)):
			slc = frame[k:]
			s = slc[inx.astype(int)]
			r = np.dot(s,self.training_seq)
			out[k] = r
		return out

		







