import Q7Mem
from ctypes import *
import GSMChan
import GSM
import time
from sptools import findFreq
from host.curlwrapper import curlwrapper
import matplotlib.pyplot as plt

class GSMFineSync:
	def __init__(self):
		self.rx = Q7Mem.rx()
		self.data = self.rx.appData(GSM.GSMAppData)
		self.chipRate = 1.92e6
		self.frame = 0.12/26.
		self.multiframe = 0.12/26.*51.
		self.fl = int(self.chipRate*self.frame)
		self.mfl = int(self.chipRate*self.multiframe)
		self.fp = long(0)


	def waitClockStable( self ):
		while self.rx.clkRate()<5:
			print "clock not stable",self.rx.clkRate()
			time.sleep(5)

	def once( self ):
		now = self.rx.now()
		last = long(self.data.frame_start_point)
		if last>now:
			print "resync:"
			return None
		mfs = (now-last)/self.mfl
		blk = self.fl/16
		newStart = mfs*self.mfl+last-blk
		myLen = blk*3/2
		while self.rx.now()<newStart+self.mfl:
			time.sleep(self.frame)
		rfd = self.rx.mmap(myLen*4,newStart*4)

		f = findFreq.findFreq(rfd,6500e3/96,1000,1.92e6)
		for i in range(4):
			newStart += self.fl*10
			rfd = self.rx.mmap(myLen*4,newStart*4)
			f += findFreq.findFreq(rfd,6500e3/96,1000,1.92e6)
		plt.plot(f)
		inx = f.argmax()
		return inx+int(6500e3/96-1000),f

	def sync(self):
		self.waitClockStable()
		ff = self.once()
		return ff

if __name__ == '__main__':
	fs = GSMFineSync()
	cnt = curlwrapper('http://192.168.1.110:8080/')
	f0,t = fs.sync()
	f1 = 0.
	while abs(f1-f0)>5:
		f1 = f0
		f0,t = fs.sync()
		print "fine sync:",f0

	f = 1625e3/24
	f = f0-f

	rxf = cnt.get_rx_freq()
	print rxf['data']['freq'],f
	cnt.set_rx_freq(rxf['data']['freq']+f)
	


