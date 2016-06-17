import numpy as np
from FB import FB
import GSM

class GSMChan:
	fftsize = 240000

	def __init__(self,data):
		self.data  = data
		self.nframes = len(data)/2
		self.frame = [complex(self.data[2*i],self.data[2*i+1]) for i in range(self.nframes)]

	def channelPower(self):
		l = len(self.frame)
		self.chPower = []
		pos = 0
		slots = l/(100*100)
		self.fPower = np.zeros((slots,100))
		for k in range(slots):
			for i in range(100):
				d = self.frame[pos:pos+100]
				fd = np.fft.fft(d)
				self.fPower[k,:] = self.fPower[k,:]+np.abs(fd)
				pos += 100

	def _freq(self,f):
		of=float(f)/self.framerate*GSMChan.fftsize
		return int(of+0.49999)

	def _window(self,s):
		return np.ones(s)
		
	def channel(self,f,b,l=-1):
		if l==-1:
			l=self.nframes
		center = self._freq(f+self.framerate/2)
		size = self._freq(b)
		win = self._window(size)
		print 'center,size',center,size
		pos = 0
		rpos = 0
		ret = np.zeros(int(l*size/GSMChan.fftsize),dtype=complex)
		slots = int(l/GSMChan.fftsize*2-1)
		for k in range(slots):
			d = self.frame[pos:pos+GSMChan.fftsize]
			fd = np.fft.fft(d)
			fd = np.fft.fftshift(fd)
			print center-size/2,center+size/2
			fr = fd[center-size/2:center+size/2]*win
			fr = np.fft.fftshift(fr)
			r = np.fft.ifft(fr)
			ret[rpos:rpos+size/2]=r[size/4:size/4+size/2]
			rpos += size/2
			pos += GSMChan.fftsize/2
		return ret

	def channels(self,b):
		self.chs = {}
		self.fbs = {}
		n = int(self.framerate/200e3)
		fn = range(6-n/2,n/2-6,1)
		print fn
		aFB = FB()
		for f in fn:
			self.chs[f]=(self.channel(f*200e3,b,GSMChan.fftsize*5))
			self.fbs[f],o = aFB._maxf(self.chs[f])
		return self.chs,self.fbs
	def modu(self,p):
		h = 51*16
		return (p+h)%h
	def findM(self,fp,p):
		poss = [0,160,320,480,640]
		maxa = fp[p]
		#print "maxa",maxa
		hit = [0]*5
		for i in range(5):
			for dp in poss:
				ppp = self.modu(p+dp-i*160)
				#print i,dp,ppp,fp[ppp]
				if fp[ppp]>maxa/2:
					hit[i]+=1
		#print hit
		for i in range(5):
			if hit[i]==5:
				return self.modu(p-i*160)

	def fbsearch(self):
		aFB = FB()
		fMap = aFB.freqmap(self.frame,self.framerate)
		"""
		self.fbMap = np.zeros(fMap.shape)
		for i in range(16*51):
			for p in poss:
				self.fbMap[i,:]+=fMap[(i+p)%(16*51),:]
		"""
		self.fbMap = fMap
		band = int(GSM.channelspace/FB.rs)
		n = int(self.framerate/GSM.channelspace)
		self.fbpos=[]
		for i in range(n):
			fslice = fMap[:,i*band:i*band+band]
			pos = fslice.argmax()
			p = int(pos/band)
			f = pos%band
			#print "p,f",p,f
			a = np.log(fslice[p,f])
			p = self.findM(fslice[:,f],p)
			if p==None:
				continue
			f += i*band
			f *= FB.rs
			if f>self.framerate/2:
				f-=self.framerate
			self.fbpos.append((p,f,a))
			#print i,'p=%4d,f=%9d,a=%f'%(p,int(f),a)
		return self.fbMap,self.fbpos,fMap





        
        

    