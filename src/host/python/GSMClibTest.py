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
import gsmlib.convCode as convCode
import gsmlib.interleave as interleave
import time

class GSMClibTest:
	def __init__(self):
		self.c0 = C0.GSMC0()
		self.c0.initSCH()
		#self.c0.initBCCH()
		#self.c0.initCCCH(range(0,9))
		self.c0.initFACCH([5,6,7])
		#c0.initSDCCH(range(1),[1])

		self.lib = CDLL(constant.c_temp_dir+'libcgsm.so')
		self.acc = clib.clib(self.lib)
		for bcch in self.c0.bcch:
			bcch.setLib(self.lib)
		for ccch in self.c0.ccch:
			ccch.setLib(self.lib)
		
		file = "../../../temp/log"
		self.bf = burstfile.burstfile(file)
		self.c0.state.timingSyncState.to("fine")
		for i in range(3):
			self.c0.state.timingSyncState.once()
		self.frameC = 0
		self.color = ['r','b','y','g','c','m','k','g-']
		
	def testSchFun(self,b):
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
		plt.figure(1)
		plt.plot(yr.real[1:],'r')
		plt.plot(yg.real[1:],'g')
		plt.plot(b.mafi.real,'b')
		plt.figure(2)
		plt.plot(yr.imag[1:],'r')
		plt.plot(yg.imag[1:],'g')
		plt.plot(b.mafi.imag,'b')
		plt.show()

	def powerGraph(self,mf1,mf2):
		power = [0.]*(mf1*8)
		for i in range(mf1*8*mf2):
			f = self.bf.readBurst().recv
			power[i%(mf1*8)] +=(np.dot(f,np.conj(f)).real)
		p = np.array(power)
		p.shape = (mf1,8)
		plt.imshow(p,aspect='auto')

	def oneSDCCH(self):
		for i in range(4):
			b = self.c0.C0.frame[i][3]
			ub = self.acc.newBurst(b.srecv)
			self.acc.demodu(ub,2)
			frame = clib.cf2c(ub.frame)	
			print np.dot(frame,np.conj(frame))

	def oneSDCCH_nb(self):
		b = c0.C0.frame[0][1]
		for t in range(1,10):
			acc.demodu(ub,t)
			chn = clib.cf2c(ub.chn)
			plt.plot(np.abs(chn),color[t%8])

			mafi = clib.cf2c(ub.mafi)
			rhh = clib.cf2c(ub.rh)
			
			plt.plot(mafi.real,'r')
			plt.plot(b.mafi.real/b.rhh[2].real,'b')
	def parity_check(self,decoded_data):
		buf = []
		buf = np.array(decoded_data[:35])
		for i in range(25):
			if buf[i]==1:
				buf[i:i+10+1]^=convCode.convCode.sch_config['parity_polynomial']
			print i,hex(clib.buf2uint64(clib.compress_bits(buf[i+1:])))

	def oneSch_nb(self):
		self.bf.skip(8)
		b,_F = self.bf.toC0(self.c0)
		ok,data = b.ch.callback(b,_F,self.c0.state)
		self.sch = b.ch
		ub = self.acc.newBurst(b.srecv)
		e,aSch = self.acc.doSch(ub)
		self.parity_check(b.ch.decoded_data)
		print "python ",b.sbm0[3:]+b.sbm1[:-3]
		print "python ",b.ch.decoded_data
		print b.ch.info
		print hex(aSch.out[0])
		b.ch.decodeBin(aSch.out[0])
		print b.ch.info
	
	def oneBcch(self):
		bcch_nb = []
		bs = []
		for i in range(4):
			self.bf.skip(7)
			b,_F = self.bf.toC0(self.c0)
			ub = self.acc.newBurst(b.srecv)
			bcch_nb.append(ub)
			bs.append(b)	
			ok,data = b.ch.callback(b,_F,self.c0.state)
			print ok
		e,aCch = self.acc.doCch(bcch_nb,self.sch.info['bcc'])
		print "pc",e
		# chn = clib.cf2c(bcch_nb[0].chn)
		# plt.plot(np.abs(chn))
		# plt.show()
		print bcch_nb[0].msg[:]
		print bs[0].msg
		return bcch_nb

	def testInterleave(self,bcch_nb):
		c = 0
		for b in bcch_nb:
			for i in range(57*2):
				b.msg[i]=c
				c+=1
		self.acc.cch_deinterleave(bcch_nb)
		print clib.clib.cch_dec.ilT[:]
		il = interleave.interleave(114*4,114)
		in_b = np.array(range(57*8))
		outb = il.decode(in_b)
		print outb[:]
	def whatinslot(self,slot):
		p = np.zeros((9,51*26))
		ts = range(8,9)
		for i in range(51*26):
			b = self.c0.C0.frame[i][slot]
			for j in range(len(ts)):
				ub = self.acc.newBurst(b.srecv)
				self.acc.demodu(ub,ts[j])
				power = float(ub.chpower)
				p[j,i] = power
		for j in range(len(ts)):
			plt.plot(p[j,:],self.color[j%8])

	def testDemodu(self):
		frameC = 0
		startT = time.time()

		for i in range(51*26*8*10):
			b,_F = self.bf.toC0(self.c0)
			if b.ch!=None:
				if b.ch.name!='FCCH':
				#print b.ch.name,b.__name__,_F
					ok,data = b.ch.callback(b,_F,self.c0.state)
					# ub = acc.newBurst(b.srecv)
					# if b.__class__==NB.NB:
					# 	acc.demodu(ub,b.training+1)
					# elif b.__class__==SB.SB:
					# 	acc.demodu(ub,0)
					frameC+=1
		endT = time.time()
		print "pre burst time:",(endT-startT)/frameC

def main():
	"""
	slot 0 FCCH,SCH,BCCH,CCCH
	slot 2,4 BCCH,CCCH
	slot 6 26 frames struct
	"""
	uut = GSMClibTest()
	# uut.oneSch_nb()
	# plt.figure(1)
	# uut.bf.reset()
	# uut.powerGraph(52,51)
	# plt.figure(2)
	# uut.bf.reset()
	# uut.powerGraph(51,52)
	uut.testDemodu()
	# uut.whatinslot(5)
	# plt.show()

if __name__ == '__main__':
	main()