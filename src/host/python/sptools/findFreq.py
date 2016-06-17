import numpy as np

def findFreq(s,fc,df,fs):
	frame = [complex(s[2*i],s[2*i+1]) for i in range(len(s)/2)]
	fftlen = int(fs)
	npf = np.zeros(fftlen,dtype=complex)
	npf[:len(frame)]=frame[:]
	fnpf = np.abs(np.fft.fft(npf))
	slif = fnpf[int(fc-df):int(fc+df)]
	return slif