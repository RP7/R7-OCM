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
bf.skip(8)
b,_F = bf.toC0(c0)
print b,_F
if b.ch!=None:
	ok,data = b.ch.callback(b,_F,c0.state)
	print b.a
	print b.b	
	o = acc.viterbi_detector(b.mafi,np.conj(b.rhh),148)
	print o
	yy = b.viterbi.t2b(b.mafi,0)
	yr = acc.viterbi_restore(yy,np.conj(b.rhh),148) #maybe right
	yg = acc.viterbi_restore(yy,b.rhh,148)
	#print yy
	print np.array(yy[0:20])-np.array(o[0:20])
	# plt.figure(1)
	# plt.plot(yr.real[1:],'r')
	# plt.plot(yg.real[1:],'g')
	# plt.plot(b.mafi.real,'b')
	# plt.figure(2)
	# plt.plot(yr.imag[1:],'r')
	# plt.plot(yg.imag[1:],'g')
	# plt.plot(b.mafi.imag,'b')
	# plt.show()