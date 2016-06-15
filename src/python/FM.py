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
							, ("atan_lut", c_int*131072)
							, ("pre", c_short*2)
							]
	def dump(self):
		return {
			  "os1": self.os1
			, "os2": self.os2
			, "len": self.len
			, "buf": hex(self.buf)
			, "result" : hex(self.result)
			, "pre" : self.pre[:]
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
		self.h = h_FM()
		self.h.os1 = self.os1
		self.h.os2 = self.os2
		self.h.len = self.l
		self.rlen = self.l/self.os1/self.os2
		self.rbuflen = self.rlen*48*128
		self.result = (c_float*(self.rbuflen+1024))()
		self.h.result = addressof(self.result)
		self.dems = 0
		self.outs = 0
		lib.fm_init(byref(self.h))

	def config(self,c):
		self.aximem = aximem.aximem(c)

	def demod(self):
		self.h.buf = self.aximem.dma.inp.data
		self.h.result = addressof(self.result) + self.dems*sizeof(c_float)
		r = lib.fm_demod(byref(self.h))
		
		self.dems += self.rlen
		if self.dems>= self.rbuflen:
			self.dems -= self.rbuflen
			print "128s pass"

	def recv(self):
		self.dems = 0
		self.outs = 0
		self.aximem.reset("inp")
		while(True):
			if self.rx_en==0:
				time.sleep(0.1)
			else:
				start = long(self.aximem.dma.inp.end)
				r = self.aximem.get(start,self.l*4)
				if r<0:
					self.aximem.reset("inp")
				elif r==0:
					time.sleep(0.01)
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

		r = string_at(addressof(self.result)+start*sizeof(c_float),l*sizeof(c_float))
		return r


	def info(self):
		return {
			  "dem" : self.dems
			, "out" : self.outs
			, "fm"  : self.h.dump()
			, "result" : hex(addressof(self.result))
			, "slice" : self.result[:3]
		}

			
