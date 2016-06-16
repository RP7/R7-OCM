import Q7Mem
from ctypes import *
import GSMChan
import GSM
import time
from host.curlwrapper import curlwrapper

class GSMRoughSync:
	def __init__(self):
		self.rx = Q7Mem.rx()
		self.data = self.rx.appData(GSM.GSMAppData)
		self.chipRate = 1.92e6
		self.frame = 0.12/26.
		self.multiframe = 0.12/26.*51.
		self.fl = int(self.chipRate*self.frame)
		self.mfl = int(self.chipRate*self.multiframe)
		self.fp = long(0)
		#print "mfl",self.mfl


	def waitClockStable( self ):
		while self.rx.clkRate()<5:
			print "clock not stable",self.rx.clkRate()
			time.sleep(5)

	def once( self ):
		now = self.rx.now()
		last = long(self.data.frame_start_point)
		if last>now:
			last = now
			print "resync:"
		mfs = (now-last)/self.mfl
		newStart = mfs*self.mfl+last
		#print "newStart",newStart
		while self.rx.now()<newStart+self.mfl:
			time.sleep(self.multiframe)
		rfd = self.rx.mmap(self.mfl*4,newStart*4)
		gsm = GSMChan.GSMChan(rfd)
		fMap,fpos,fm = gsm.fbsearch()
		maxa = 0
		for (p,f,a) in fpos:
			if a>maxa:
				fp,ff,fa = p,f,a
		pp = fp*self.fl/16
		return pp,newStart+pp,ff,fa

	def sync(self):
		self.waitClockStable()
		fp,new_frame,ff,fa = self.once()
		#print fp,ff,fa
		self.data.frame_start_point = long(new_frame)
		#self.fp = long(new_frame)
		return ff

def main():
	rs = GSMRoughSync()
	cnt = curlwrapper('http://192.168.1.110:8080/')
	cnt.set_afc(0x1f)
	f0 = rs.sync()
	f1 = 0.
	while abs(f1-f0)>1e3:
		f1 = f0
		f0 = rs.sync()
		print "rough sync:"

	f = 1625e3/24
	f = f0-f

	rxf = cnt.get_rx_freq()
	print rxf['data']['freq'],f
	cnt.set_rx_freq(rxf['data']['freq']+f)

if __name__ == '__main__':
	main()


