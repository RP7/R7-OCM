from ctypes import *
import numpy as np
from SB import SB,SBTraining
from NB import NB,NBTraining
import config
import GSM as gsm
def c2cf(x):
	cx = (c_float*(len(x)*2))()
	cx[::2]=x.real[:]
	cx[1::2]=x.imag[:]
	return cx
	
def cf2c(output):
	return np.array([complex(output[i],output[i+1]) for i in range(0,len(output),2)])
"""
typedef struct burst_s {
  int bl;
  float osr;
  short *recv;
  gr_complex frame[1500];
  gr_complex chn[3*10];
  gr_complex rh[3];
  int cut_pos;
  gr_complex mafi[148];
  int demoduled[148];
} burst_t;
"""
class cburst(Structure):
	_fields_ = [
		  ("bl"         , c_int)
		, ("osr"        , c_float)
		, ("recv"       , c_void_p)
		, ("frame"      , c_float*3000)
		, ("chn"        , c_float*120)
		, ("rh"         , c_float*6)
		, ("cut_pos"    , c_int)
		, ("mafi"       , c_float*296)
		, ("demodulated", c_int*148)
		, ("msg"        , c_int*148)
		, ("stolen"     , c_int*2)
	]

	def __init__(self):
		self.osr = float(config.SampleRate/gsm.SymbolRate)
	def mmap(self,r):
		self.recv = addressof(r)
class Trainings(Structure):
	_fields_ = [
		  ("sb", c_float*128)
		, ("nb", c_float*52*len(NBTraining.bits))
		, ("sb_chn_s", c_int)
		, ("sb_chn_e", c_int)
		, ("nb_chn_s", c_int)
		, ("nb_chn_e", c_int)
	]
	def __init__(self):
		cut = 145
		self.sb[:] = c2cf(SBTraining.modulated)[:]
		for i in range(len(NBTraining.bits)):
			self.nb[i][:] = c2cf(NBTraining.modulated[i,:])[:]
		self.sb_chn_s = SB._chn_s+cut
		self.sb_chn_e = SB._chn_s+cut+30
		self.nb_chn_s = NB._chn_s+cut
		self.nb_chn_e = NB._chn_s+cut+30
		print self.sb_chn_s
class clib:
	trainings = Trainings()
	def __init__(self,lib):
		self.lib = lib
	
	def newBurst(self,r):
		b = cburst()
		b.bl = len(r)/2
		b.mmap(r)
		return b
	def demodu(self,b,t):
		self.lib.demodu(byref(b),byref(clib.trainings),c_int(t))

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
	
	def matchFilter(self,d,h,osr,timing):
		cd = c2cf(d)
		ch = c2cf(h)
		l = int((len(d)-len(h)-1)/osr)
		cout = (c_float*(l*2))()
		self.lib.matchFilter( 
			  byref(cd), byref(ch)
			, c_int(l), c_int(len(h))
			, byref(cout)
			, c_float(osr), c_float(timing)) 
		return cf2c(cout)		
		
	def maxwin(self,b,l):
		cb = c2cf(b)
		p = self.lib.maxwin(byref(cb),c_int(len(b)),c_int(l))
		return p

	def channelEst(self,frame,training,osr):
		cf = c2cf(frame)
		ct = c2cf(training)
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
		return cf2c(cout)

