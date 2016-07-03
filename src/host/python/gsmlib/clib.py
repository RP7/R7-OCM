from ctypes import *
import numpy as np
class clib:
	def __init__(self,lib):
		self.lib = lib

	def viterbi_detector(self,mafi,rhh,bs):
		filtered_burst = (c_float*(bs*2))()
		stop_states = (c_int*2)()
		stop_states[0]=1
		stop_states[1]=2
		output =(c_int*bs)()
		hard   =(c_int*bs)()
		filtered_burst[::2]=mafi[:bs].real/rhh[2].real
		filtered_burst[1::2]=mafi[:bs].imag/rhh[2].real
		xrhh =(c_float*6)()
		xrhh[::2]=rhh[1:4].real/rhh[2].real
		xrhh[1::2]=rhh[1:4].imag/rhh[2].real
		self.lib.viterbi_detector( 
			  byref(filtered_burst)
			, 148
			, byref(xrhh)
			, c_int(2)
			, byref(stop_states)
			, 2
			, byref(output)
			)
		return output[:]

	def viterbi_restore(self,x,rhh,bs):
		output = (c_float*(bs*2))()
		in_put =(c_int*bs)()
		in_put[:] = x[:bs]
		xrhh =(c_float*6)()
		xrhh[::2]=rhh[1:4].real
		xrhh[1::2]=rhh[1:4].imag
		self.lib.viterbi_restore( 
			  byref(in_put)
			, 148
			, byref(xrhh)
			, c_int(1)
			, c_int(0)
			, byref(output)
			)
		return np.array([complex(output[i],output[i+1]) for i in range(0,len(output),2)])
	
	def c2cf(self,x):
		cx = (c_float*(len(x)*2))()
		cx[::2]=x.real[:]
		cx[1::2]=x.imag[:]
		return cx
	
	def cf2c(self,output):
		return np.array([complex(output[i],output[i+1]) for i in range(0,len(output),2)])
	
	def matchFilter(self,d,h,osr,timing):
		cd = self.c2cf(d)
		ch = self.c2cf(h)
		l = int((len(d)-len(h)-1)/osr)
		cout = (c_float*(l*2))()
		self.lib.matchFilter( 
			  byref(cd), byref(ch)
			, c_int(l), c_int(len(h))
			, byref(cout)
			, c_float(osr), c_float(timing)) 
		return self.cf2c(cout)		
		
	def maxwin(self,b,l):
		cb = self.c2cf(b)
		p = self.lib.maxwin(byref(cb),c_int(len(b)),c_int(l))
		return p

	def channelEst(self,frame,training,osr):
		cf = self.c2cf(frame)
		ct = self.c2cf(training)
		l = int(len(frame)-(len(training)-1)*osr)
		cout = (c_float*(l*2))()
		self.lib.channelEst(
			  byref(cf)
			, byref(ct)
			, c_int(len(frame))
			, c_int(len(training))
			, c_float(osr)
			, c_int(l)
			, byref(cout)
			)
		return self.cf2c(cout)

