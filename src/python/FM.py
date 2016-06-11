import aximem
import numpy as np
import threading
from ctypes import *
import time

class FM:
	def __init__(self,l=1024):
		self.l = l
		self.aximem = None
		self.rx_en = 0
		self.rx_stop = 1
		self.f = np.zeros(self.l)
		self.os = 4
		self.os2 = 10
		self.last = 1

		self.thread = threading.Thread(target = self.recv, name = 'fm')
		self.dem = []

	def config(self,c):
		self.aximem = aximem.aximem(c)

	def demod(self):
		d = np.frombuffer(string_at(self.aximem.dma.inp.data,self.l*4), dtype=np.int16, count=self.l*2, offset=0)
		iq = complex(1.,0.)*d[::2]+complex(0.,1.)*d[1::2]
		iq.shape = (self.l/self.os,self.os)
		s = iq.sum(1)
		ds = np.angle(s)
		phase = ds[1:]-ds[:-1]
		up = np.unwrap(phase)
		
		for k in range(0,len(up)-self.os2,self.os2):
			x = (up[k:k+self.os2]).sum()/self.os2/np.pi
			if len(self.dem)<44100*4:
				self.dem.append(x)

	def recv(self):
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
		r = [np.angle(x)/np.pi for x in self.dem]
		self.dem = []
		return r

			
