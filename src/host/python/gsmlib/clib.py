from ctypes import *
import numpy as np
from SB import SB,SBTraining
from NB import NB,NBTraining
import config
import GSM as gsm
from convCode import convCode
from interleave import interleave

def c2cf(x):
	cx = (c_float*(len(x)*2))()
	cx[::2]=x.real[:]
	cx[1::2]=x.imag[:]
	return cx
	
def cf2c(output):
	return np.array([complex(output[i],output[i+1]) for i in range(0,len(output),2)])

def compress_bits(sbuf):
	dbuf = []
	for i in range(0,len(sbuf)-7,8):
		c = 0
		k = 1
		for x in sbuf[i:i+8]:
			c += k*x
			k *= 2
		dbuf.append(c)
	if i+8<len(sbuf):
		c = 0
		k = 1
		for x in sbuf[i+8:]:
			c += k*x
			k *= 2
		dbuf.append(c)
	return dbuf

def buf2uint64(buf):
	r = long(0)
	for x in buf[::-1]:
		r<<=8
		r+=long(x)
	#print [hex(x) for x in buf],hex(r)
	return r

"""
typedef struct burst_s {
  int bl;
  float osr;
  short *recv;
  gr_complex frame[1500];
  gr_complex chn[3*10];
  gr_complex rh[3];
  int cut_pos;
  float chpower;
  gr_complex mafi[148];
  int demoduled[148];
  int msg[148];
  int stolen[2];
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
		, ("chpower"    , c_float)
		, ("mafi"       , c_float*296)
		, ("demodulated", c_int*148)
		, ("msg"        , c_int*148)
		, ("stolen"     , c_int*2)
	]

	def __init__(self):
		self.osr = float(config.SampleRate/gsm.SymbolRate)
	def mmap(self,r):
		self.recv = addressof(r)
"""
typedef struct sch_s {
  burst_t *sb;
  unsigned char in_buf[78];
  unsigned char outbuf[35];
  uint64_t out[2];
} sch_t;
"""
class cSch(Structure):
	_fields_ = [
		  ("sb"     ,c_void_p)
		, ("in_buf" ,c_char*78)
		, ("outbuf" ,c_char*35)
		, ("out"    ,c_uint64*2)
	]
	def __init__(self,b):
		self.sb = addressof(b)
"""
typedef struct cch_s {
  burst_t *nb[4];
  unsigned char in_buf[1024];
  unsigned char outbuf[1024];
  uint64_t out[4];
} cch_t;
"""
class cCch(Structure):
	_fields_ = [
		  ("nb"     ,c_void_p*4)
		, ("in_buf" ,c_char*1024)
		, ("outbuf" ,c_char*1024)
		, ("out"    ,c_uint64*4)
	]
	def __init__(self,bs):
		for i in range(len(bs)):
			self.nb[i] = addressof(bs[i]) 
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
		self.sb_chn_e = SB._chn_s+cut+60
		self.nb_chn_s = NB._chn_s+cut
		self.nb_chn_e = NB._chn_s+cut+60
"""
	typedef struct CC_s {
      uint64_t pp;
      uint64_t pr;
      int bs;
      int ps;
      int ts;
      int maxE;
   	} CC_t;
"""
class ConvCodeHandle(Structure):
	_fields_ = [
		  ("pp"  , c_uint64)
		, ("pr"  , c_uint64)
		, ("bs"  , c_int)
		, ("ps"  , c_int)
		, ("ts"  , c_int)
		, ("ins" , c_int)
		, ("maxE", c_int)
		, ("ilT" , c_int*(57*8))
	]
	def __init__(self,config):
		self.pp = c_uint64(buf2uint64(compress_bits(config['parity_polynomial'])))
		self.pr = c_uint64(buf2uint64(compress_bits(config['parity_remainder'])))
		self.bs = c_int(config['DATA_BLOCK_SIZE'])
		self.ps = c_int(config['PARITY_SIZE'])
		self.ts = c_int(config['TAIL_BITS_SIZE'])
		self.ins = self.bs+self.ps+self.ts
		self.maxE = self.ins*2+1
		il = interleave(57*8,57*2)
		self.ilT[:]=il.trans[:]
class clib:
	trainings = Trainings()
	sch_dec = ConvCodeHandle(convCode.sch_config)
	cch_dec = ConvCodeHandle(convCode.cch_config)
	def __init__(self,lib):
		self.lib = lib
	
	def newBurst(self,r):
		b = cburst()
		b.bl = len(r)/2
		b.mmap(r)
		return b
	
	def demodu(self,b,t):
		self.lib.demodu(byref(b),byref(clib.trainings),c_int(t))
	
	def doSch(self,b):
		aSch = cSch(b)
		return self.lib.doSch(byref(aSch),byref(clib.trainings),byref(clib.sch_dec),0),aSch

	def doCch(self,b,t):
		aCch = cCch(b)
		return self.lib.doCch(byref(aCch),byref(clib.trainings),byref(clib.cch_dec),c_int(t+1)),aCch
	
	def cch_deinterleave(self,b):
		self.aCch = cCch(b)
		self.lib.cch_deinterleave(byref(self.aCch),byref(clib.cch_dec))
	
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

