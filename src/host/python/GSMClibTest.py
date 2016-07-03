import gsmlib.GSMC0 as C0
import matplotlib.pyplot as plt

import numpy as np
import gsmlib.splibs as sp
import gsmlib.Burst as Burst
import gsmlib.burstfile as burstfile
from ctypes import *
import constant
import gsmlib.clib as clib
import gsmlib.SB as SB
def testFun(b):
	chn = acc.channelEst(b.recv,SB.SBTraining.modulated,Burst.Burst.fosr)
	inx = np.floor(np.arange(64)*Burst.Burst.fosr)
	print inx[:]
	print "clib chn",len(chn),chn[:3]
	print "python chn",len(b.chn),b.chn[:3]	
	rhh = acc.matchFilter( 
			  b.chn[b.cut_pos:b.cut_pos+Burst.Burst.chnMatchLength]
			, b.cut_chn
			, Burst.Burst.fosr
			, 0. )
	print rhh/64.
	print b.rhh
	p = acc.maxwin(b.chn[SB.SB._chn_s:SB.SB._chn_e],Burst.Burst.chn_len)
	print "clib p",p+SB.SB._chn_s,"python p",b.cut_pos
	print b.a
	print b.b	
	o = acc.viterbi_detector(b.mafi,np.conj(b.rhh),148)
	print o
	yy = b.viterbi.t2b(b.mafi,0)
	yr = acc.viterbi_restore(yy,np.conj(b.rhh),148) #maybe right
	yg = acc.viterbi_restore(yy,b.rhh,148)
	print yy
	print np.array(yy[:147])-np.array(o[1:148])
	# plt.figure(1)
	# plt.plot(yr.real[1:],'r')
	# plt.plot(yg.real[1:],'g')
	# plt.plot(b.mafi.real,'b')
	# plt.figure(2)
	# plt.plot(yr.imag[1:],'r')
	# plt.plot(yg.imag[1:],'g')
	# plt.plot(b.mafi.imag,'b')
	# plt.show()
c0 = C0.GSMC0()

c0.initSCH()
c0.initBCCH()

file = "../../../temp/gsm.log"
lib = CDLL(constant.c_temp_dir+'libcgsm.so')
acc = clib.clib(lib)

bf = burstfile.burstfile(file)
c0.state.timingSyncState.to("fine")
for i in range(3):
	c0.state.timingSyncState.once()
bf.skip(8+8+8)
b,_F = bf.toC0(c0)
print b,_F
if b.ch!=None:
	ok,data = b.ch.callback(b,_F,c0.state)
	#testFun(b)
	ub = acc.newBurst(b.srecv)
	acc.demodu(ub,b.training+1)
	chn = clib.cf2c(ub.chn)
	mafi = clib.cf2c(ub.mafi)
	rhh = clib.cf2c(ub.rh)
	print ub.msg[:114]
	print b.nbm0
	print np.array(ub.msg[:114])-np.array(b.msg)
	plt.plot(mafi.real,'r')
	plt.plot(b.mafi.real/b.rhh[2].real,'b')
	#plt.plot(np.abs(chn))
	plt.show()
	print ub.demodulated[:]
	# print b.a
	print b.b

	
	
