import dev_mem
from const import *
import sys
import numpy as np

class axi2s_u:
	def __init__(self):
		self.dev = dev_mem.dev_mem(OCM_BASE,OCM_SIZE)

	def dump(self,offset,length):
		iLen = (length+3)/4
		r = self.dev.memread(offset,iLen)
		for i in range(0,iLen,16):
			print 'R:',
			print "%04x"%(i+offset),
			for k in range(16):
				print "%08x"%(r[i+k]),
			print ""
	
	def idata(self):
		d = self.dev.memread(0,1024)
		x = []
		i = []
		for n in range(1024):
			x.append(n)
			z = d[n]&0xffff
			if z>32767:
				z -= 65536
			i.append(z)
		r = {'freq':x,'power':i}
		print 'ocm read',r['power'][:10]
		return r
	
	def rfdata(self):
		self.dev.SetOffset(0)
		d = np.frombuffer(self.dev.mmap, dtype=np.int16, count=1920*2, offset=0)
		iq = complex(1.,0.)*d[::2]+complex(0.,1.)*d[1::2]
		f = np.fft.fft(iq)
		f = np.fft.fftshift(f)
		f = np.log10(np.abs(f))*20.
		fl = f.tolist()
		i = d[::2]
		q = d[1::2]
		r = {'freq':range(-500,501),'power':fl[960-500:960+501],'i':i.tolist(),'q':q.tolist()}
		return r
		
	def deinit(self):
		self.dev.deinit()

def main():
	uut = axi2s_u()
	uut.dump(int(sys.argv[1],16),int(sys.argv[2],16))

if __name__ == '__main__':
	main()