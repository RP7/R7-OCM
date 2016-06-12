import aximem
import numpy as np
import threading
from ctypes import *
import time
from c_lib import lib
"""
typedef struct fm_s {
	int16_t *buf;
	int16_t *result;
	int len;
	int16_t pre[2];
	int atan_lut[131072];
} fm_t;
"""

class h_FM(Structure):
	_fields_ = [  ("buf", c_void_p)
							, ("result", c_void_p)
							, ("os1", c_uint)
							, ("os2", c_uint)
							, ("len", c_uint)
							, ("pre", c_short*2)
							, ("atan_lut", c_int*131072)
							]
	def dump(self):
		return {
			  "os1": self.os1
			, "os2": self.os2
			, "len": self.len
		}


class FM:
	def __init__(self,l=2560):
		self.l = l
		self.aximem = None
		self.rx_en = 0
		self.rx_stop = 1
		self.f = np.zeros(self.l)
		self.os1 = 4
		self.os2 = 10
		self.last = 1

		self.thread = threading.Thread(target = self.recv, name = 'fm')
		self.dem = []
		self.h = h_FM()
		self.h.os1 = self.os1
		self.h.os2 = self.os2
		self.h.len = self.l
		self.rlen = self.l/self.os1/self.os2
		self.rbuflen = self.rlen*48*128
		self.result = (c_short*self.rlen)()
		self.h.result = addressof(self.result)
		self.dems = 0
		self.outs = 0
		lib.fm_init(byref(self.h))

	def config(self,c):
		self.aximem = aximem.aximem(c)

	def demod(self):
		if self.aximem.dma.inp.data==0:
			print "error 64"
		self.h.buf = self.aximem.dma.inp.data
		self.h.result = addressof(self.result)+self.dems*2
		r = lib.fm_demod(byref(self.h))
		if r!=self.rlen:
			print "error 67"

		self.dems += self.rlen
		if self.dems>= self.rbuflen:
			self.dems -= self.rbuflen
			print "128s pass"

	def demod_p(self):
		d = np.frombuffer(string_at(self.aximem.dma.inp.data,self.l*4), dtype=np.int16, count=self.l*2, offset=0)
		iq = complex(1.,0.)*d[::self.os*2]+complex(0.,1.)*d[1::self.os*2]
		ds = np.angle(iq)
		phase = ds[1:]-ds[:-1]
		up = np.unwrap(phase)
		
		for k in range(0,len(up)-self.os2,self.os2):
			x = (up[k:k+self.os2]).sum()/self.os2/np.pi
			if len(self.dem)<480000*10:
				self.dem.append(x)

	def recv(self):
		self.dems = 0
		self.outs = 0
		self.aximem.reset("inp")
		while(True):
			if self.rx_en==0:
				time.sleep(0.1)
			else:
				start = self.aximem.dma.inp.end
				r = self.aximem.get(start,self.l*4)
				if r<0:
					self.aximem.reset("inp")
				elif r==0:
					time.sleep(0.01)
				else:
					if r!=self.l*4:
						print "error 102"
					else:
						self.demod()
			if self.rx_stop==1:
				break

	def stop(self):
		self.rx_stop = 1
		time.sleep(0.1)
	
	def en(self):
		self.rx_stop = 0
		self.rx_en = 1
		
	def exit(self):
		self.stop()
		

	def run(self):
		if self.aximem == None:
			return
		self.stop()
		self.en()
		self.thread.start()
		
	def dump(self):
		end = self.dems
		start = self.outs
		l = end-start
		if l<0:
			l += self.rbuflen
		if l>48000*10:
			self.outs = end
			return []

		if end==start:
			r = []
		elif end>start:
			r = self.result[start:end]
			self.outs = end
		else:
			r = self.result[start:self.rbuflen]
			self.outs = 0
		return r
	
	def out(self):
		end = self.dems
		start = self.outs
		self.outs = end
		l = end-start
		if l<0:
			l = self.rbuflen - start
			self.outs = 0

		if l>48000*10:
			return ''

		#r = string_at(addressof(self.result)+start*2,l*2)
		r  = "abc"
		return r


	def info(self):
		return {
			  "dem" : self.dems
			, "out" : self.outs
		}

			
