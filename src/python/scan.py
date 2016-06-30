from config import config
from axi2s_c import axi2s_c
from axi2s_u import axi2s_u
from AD9361_c import AD9361_c
import numpy as np
class scan:
	FFTSIZE = 3072
	OUTSIZE = 2000
	AGC_TAGET = 1024*1024/2
	def __init__(self,g):
		self.g = g
		self.ram = axi2s_u(g.AXI2S_IBASE,g.AXI2S_ISIZE)
		self.config = g.todict()
		self.axi = axi2s_c()
		self.axi.status(self.config)
		self.ad = AD9361_c()
		self.gain = 0x4c
		self.ad.Set_Rx_Gain(self.gain,1)
		self.agc()
		self.iq = np.zeros(scan.FFTSIZE*16,dtype=complex)
	def init(self):
		self.gain = 0x4c
		self.ad.Set_Rx_Gain(self.gain,1)
		self.agc()
		self.iq = np.zeros(scan.FFTSIZE*16,dtype=complex)
		
	def nowData(self,k):
		self.axi.getCNT()
		pos = self.axi.cnt['AXI2S_IACNT']
		if pos<scan.FFTSIZE*4*k:
			pos = self.g.AXI2S_ISIZE
		pos -= scan.FFTSIZE*4*k
		iq = self.ram.npfrom(pos,scan.FFTSIZE*k)
		return iq

	def agcOnce(self):
		iq = self.nowData(1)
		p = (np.dot(iq,np.conj(iq))/scan.FFTSIZE).real
		print "power",p
		d=-int(np.log10(p/scan.AGC_TAGET)*10.)
		self.setGain(d)
		return d

	def setGain(self,d):
		dg = self.gain+d
		if dg<0 or dg>0x4c:
			print "out of agc range"
		else:
			self.ad.Set_Rx_Gain(dg,1)
			self.gain = dg

	def agc(self):
		c = 10
		while c>0:
			d = self.agcOnce()
			if abs(d)<=1:
				return
			c -= 1
		print "agc not ok"

	def oneShot(self,next_f,r):
		self.ad.Set_Rx_freq(next_f)
		last_gain = self.gain
		self.agc()
		d = np.zeros(scan.OUTSIZE)
		for i in range(16):
			fd = np.fft.fft(self.iq[i*scan.FFTSIZE:(i+1)*scan.FFTSIZE])
			sfd = np.fft.fftshift(fd)
			cutfd = sfd[scan.FFTSIZE/2-scan.OUTSIZE/2:scan.FFTSIZE/2+scan.OUTSIZE/2]
			d += (cutfd*np.conj(cutfd)).real
		logd = np.log10(d)*10.-last_gain
		self.iq = self.nowData(16)
		return zip(r.tolist(),logd.tolist())

	def spectrum(self,startf,endf):
		self.r = []
		s = int(startf/20e6)
		e = int(endf/20e6+1)
		for f in range(s-1,e):
			cf = f*20e6
			r = np.arange(cf-30e6,cf-10e6,10e3)
			self.r += self.oneShot(cf,r)
		self.r = self.r[2000:]
		return self.r
		
def main():
	g = config()
	s = scan(g)
	sp = s.spectrum(800e6,1000e6)
	print sp


if __name__ == '__main__':
	main()



