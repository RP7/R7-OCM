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
import gsmlib.NB as NB
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
c0.initCCCH(range(0,9))
c0.initSDCCH(range(1),[1])

file = "../../../temp/log"
lib = CDLL(constant.c_temp_dir+'libcgsm.so')
acc = clib.clib(lib)

bf = burstfile.burstfile(file)
c0.state.timingSyncState.to("fine")
for i in range(3):
	c0.state.timingSyncState.once()
#bf.skip(8+8+8)
for i in range(8*4):
	b,_F = bf.toC0(c0)
	if b.ch!=None:
		print b.ch.name,b.__name__,_F
		ok,data = b.ch.callback(b,_F,c0.state)
		ub = acc.newBurst(b.srecv)
		if b.__class__==NB.NB:
			acc.demodu(ub,b.training+1)
			print "dif",np.sum(np.array(ub.msg[:114])-np.array(b.msg))
		elif b.__class__==SB.SB:
			acc.demodu(ub,0)
			print "dif",np.sum(np.array(ub.msg[:78])-np.array(b.sbm0[3:]+b.sbm1[:-3]))
# power = [0.]*(51*8)
# for i in range(51*8*26):
# 	f = bf.readBurst().recv
# 	power[i%(51*8)] +=(np.dot(f,np.conj(f)).real)
# p = np.array(power)
# p.shape = (51,8)
# #print p
# plt.imshow(p,aspect='auto')
# plt.show()

# for i in range(4):
# 	b = c0.C0.frame[i][3]
# 	ub = acc.newBurst(b.srecv)
# 	acc.demodu(ub,2)
# 	frame = clib.cf2c(ub.frame)	
# 	print np.dot(frame,np.conj(frame))

# b = c0.C0.frame[0][1]
# color = ['r','b','y','g','c','m','k','w']
# for t in range(1,10):
# 	acc.demodu(ub,t)
# 	chn = clib.cf2c(ub.chn)
# 	plt.plot(np.abs(chn),color[t%8])

# plt.show()
	# mafi = clib.cf2c(ub.mafi)
	# rhh = clib.cf2c(ub.rh)
	
	#plt.plot(mafi.real,'r')
	#plt.plot(b.mafi.real/b.rhh[2].real,'b')
	#plt.show()
	
	
	
