from FB import FB
from SB import SB
from NB import NB
from DB import DB
from Burst import Burst
import numpy as np
import struct
from ctypes import *

class burstFileHead(Structure):
	_pack_ = 1
	_fields_ =  [   ("name", c_char*2)
								, ("length", c_int32)
								, ("fn", c_int64)
						]
	
class burstfile:
	burst = {'FB':FB,'SB':SB,'NB':NB,'DB':DB}
	def __init__(self,fn):
		self.f = open(fn,'rb')
	def skip(self,l):
		self.f.seek(l*(sizeof(burstFileHead)+4*1460),1)

	def readBurst(self):
		t = self.f.read(sizeof(burstFileHead))
		bdh = self.stream2struct(t,burstFileHead)
		raw = self.f.read(1460*4)
		print bdh.name[:2],bdh.length,hex(bdh.fn)
		if bdh.name in burstfile.burst:
			b = burstfile.burst[bdh.name]()
			b.fn = bdh.fn
			recv_type = (c_short*(2*1460))
			recv = recv_type.from_buffer(bytearray(raw))
			b.recv = Burst.short2Complex(recv)
			return b
		else:
			#raw = self.f.read(1460*4)
			return None

	def struct2stream(self,s):
		length  = sizeof(s)
		p       = cast(pointer(s), POINTER(c_char * length))
		return p.contents.raw

	def stream2struct(self,string, stype):
		if not issubclass(stype, Structure):
			raise ValueError('The type of the struct is not a ctypes.Structure')
		length      = sizeof(stype)
		stream      = (c_char * length)()
		stream.raw  = string
		p           = cast(stream, POINTER(stype))
		return p.contents

	def close(self):
		self.f.close()


def findT(b):
	p = np.zeros(6)
	for i in range(6):
		b.training = i
		b.chnEst()
		peek = np.abs(b.chn)
		p[i]=peek[peek.argmax()]
	return p.argmax()
def main():
	import matplotlib.pyplot as plt
	from NB import NBTraining
	from SCH import SCH
	sch = SCH()

	fn = "../../../../temp/log"
	f = burstfile(fn)
	f.skip(8*51*26*2+8*1)
	co = ['r','b','y','g','r.','b.','y.','g.']
	for i in range(160):
		b = f.readBurst()
		if b == None:
			continue
		if b.__class__.__name__=='':
			for k in range(8):#if tlist[i%8]!=10:
				b.training = k #tlist[i%8]
				b.chnEst()
				#b.viterbi_detector()
				# np.savetxt("../../../../data/nbmafi",b.mafi)
				# np.savetxt("../../../../data/nbrhh",b.rhh)
				# np.savetxt("../../../../data/nbtraining",NBTraining.modulated[5,:])
				# break
				#print "0",b.nbm0
				#print "1",b.nbm1
				plt.subplot(8,1,k+1)
				p = np.abs(b.chn)
				plt.plot(p,co[i])
				pos = p.argmax()
				print "p",i,k,NB._chn_s+pos,p[pos]
		if b.__class__.__name__=='SB':
			p = b.peekS()
			b.setChEst()
			b.viterbi_detector()
			b.viterbi.outMsg(b.sbm0)
			b.viterbi.outMsg(b.sbm1)
			sch.msg = b.sbm0[3:]+b.sbm1[:-3]
			sch.decoded_data = sch.conv_decode()
			b.viterbi.outMsg(sch.decoded_data)
			print "check",sch.parity_check()
			print "info",sch.decode()
			
			#plt.subplot(8,1,i+1)
			p = np.abs(b.cut_chn)
			plt.plot(p)
			pos = p.argmax()
			print "p",i,pos,p[pos],b.cut_pos
	#print tlist
	plt.show()
	f.close()

if __name__ == '__main__':
	main()