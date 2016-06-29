import numpy as np

def findFreq(s,fc,df,fs):
	frame = [complex(s[2*i],s[2*i+1]) for i in range(len(s)/2)]
	fftlen = int(fs)
	npf = np.zeros(fftlen,dtype=complex)
	npf[:len(frame)]=frame[:]
	fnpf = np.abs(np.fft.fft(npf))
	slif = fnpf[int(fc-df):int(fc+df)]
	return slif

def autocorrelation(s,k):
	return np.dot(s[k:],np.conj(s[:-k]))

def matchFilter(d,h,osr,timing):
	rh = np.conj(h)
	s = 0.
	l = int((len(d)-len(h)-1)/osr)
	#print len(d),len(h),l,osr
	ret = np.zeros(l,dtype=complex)
	for k in range(l):
		s = k*osr+timing
		p = int(s)
		f = s-p
		a = np.dot(d[p:p+len(rh)],rh)
		b = np.dot(d[p+1:p+1+len(rh)],rh)
		ret[k]=a*(1.-f)+b*f
	return ret

def maxwin(d,l):
	pd = d*np.conj(d)
	sump = np.zeros(len(pd))
	s = 0.
	for k in range(len(sump)):
		s += pd[k].real
		sump[k]=s
	#print "len",len(d),l
	dsump = sump[l:]-sump[:-l]
	p = dsump.argmax()
	return d[p:p+l],p

def filter(a,b):
	rb = b[::-1]
	c = np.zeros((len(a)+len(b)-1),dtype=complex)
	ae = np.zeros((len(a)+2*len(b)-1),dtype=complex)
	ae[len(b)-1:len(a)+len(b)-1]=a
	for i in range(len(c)):
		c[i]=np.dot(rb,ae[i:i+len(b)])
	return c

def viterbi():
	pass

