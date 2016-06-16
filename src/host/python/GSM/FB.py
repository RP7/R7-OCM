from Burst import Burst
import numpy as np
import GSM

class FB(Burst):
	rs = 0.1e3
	def __init__(self):
		pass
	
	def _maxf(self,frame):
		r = []
		o = []
		fftsize = Burst.slot
		n = len(frame)/fftsize*5
		pos = 0
		for i in range(n):
			fd = np.abs(np.fft.fft(frame[pos:pos+fftsize]))
			pos += fftsize/5
			inx = fd.argmax()
			m = fd[inx]
			r.append(m)
			o.append(inx)
		return r,o

	def rough(self,frame):
		fftsize = Burst.slot
		r,o = self._maxf(frame)
		inx = np.array(r).argmax()
		peek = r[inx]
		freq = o[inx]
		return inx*fftsize/5,peek,freq

	def find(self,frame,pos,freq):
		fftsize = Burst.slot
		d = frame[pos-fftsize:pos+2*fftsize]
		r = np.arange(fftsize)*freq*2.*np.pi/float(fftsize)
		r = np.exp(1j*r)
		z = np.zeros(len(d),dtype=complex)
		z[:len(r)]=r
		fd = np.fft.fft(d)
		fz = np.fft.fft(z)
		r = fd*np.conj(fz)
		tr = np.abs(np.fft.ifft(r))
		inx = tr.argmax()
		return inx+pos-fftsize

	def freqmap(self,frame,samplerate):
		fftpoint = int(samplerate/FB.rs)
		slots = int(GSM.ts*GSM.samplepreslot*samplerate)
		step = GSM.ts*GSM.samplepreslot*samplerate/2.
		fMap = np.zeros((16*51,fftpoint))
		k = 0
		while k*step+slots<len(frame):
			pos = int(k*step)
			d = np.zeros(fftpoint,dtype=complex)
			d[:slots]=frame[pos:pos+slots]
			fd = np.fft.fft(d)
			fMap[k%(16*51),:]+=np.abs(fd)
			k+=1
		#print "process",k,step,len(frame)
		return fMap

		


	



