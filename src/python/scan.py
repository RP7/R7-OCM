from config import config
from axi2s_c import axi2s_c
from axi2s_u import axi2s_u
from AD9361_c import AD9361_c
import numpy as np
import time
class scan:
	FFTSIZE = 3072
	OUTSIZE = 1000
	STEP = 10e6
	AGC_TAGET_MAX = 1024*1024/2
	AGC_TAGET_MIN = 1024*1024/512
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
		p = (np.dot(iq,np.conj(iq))/scan.FFTSIZE).real+1.
		d = 0
		if p>scan.AGC_TAGET_MAX and self.gain!=0:
			d=-int(np.log10(p/scan.AGC_TAGET_MAX)*10.)
		if p<scan.AGC_TAGET_MIN and self.gain!=0x4c:
			d=-int(np.log10(p/scan.AGC_TAGET_MAX)*10.)
		self.setGain(d)
		return d

	def setGain(self,d):
		if d!=0:
			dg = self.gain+d
			if dg<0 :
				print "too large"
				dg = 0
			if dg>0x4c:
				print "too small"
				dg = 0x4c
			self.ad.Set_Rx_Gain(dg,1)
			self.gain = dg
		#self.ad.Check_FDD()
		
	def agc(self):
		c = 10
		while c>0:
			d = self.agcOnce()
			time.sleep(0.01)
			if abs(d)<=1:
				return
			c -= 1
		print "agc not ok"

	def oneShot(self,next_f,r):
		self.ad.Set_Rx_freq(next_f)
		last_gain = self.gain
		self.agc()
		logd = np.zeros(scan.OUTSIZE)
		for i in range(16):
			fd = np.fft.fft(self.iq[i*scan.FFTSIZE:(i+1)*scan.FFTSIZE])
			sfd = np.fft.fftshift(fd)
			cutfd = sfd[scan.FFTSIZE/2-scan.OUTSIZE/2:scan.FFTSIZE/2+scan.OUTSIZE/2]
			d = (cutfd*np.conj(cutfd)).real
			logd += np.log10(d)*10.-last_gain
		logd = logd/16.
		self.iq = self.nowData(16)
		return zip(r.tolist(),logd.tolist())

	def spectrum(self,startf,endf):
		self.r = []
		s = int(startf/scan.STEP)
		e = int(endf/scan.STEP+1)
		for f in range(s,e):
			cf = f*scan.STEP
			r = np.arange(cf-scan.STEP*1.5,cf-scan.STEP*0.5,10e3)
			self.r += self.oneShot(cf,r)
		self.r = self.r[scan.OUTSIZE:]
		#ret = {a:b for (a,b) in self.r}
		return self.r
		
def main():
	g = config()
	s = scan(g)
	sp = s.spectrum(800e6,1000e6)
	print sp


if __name__ == '__main__':
	main()



