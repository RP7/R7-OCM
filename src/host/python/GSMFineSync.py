from ctypes import *
import GSM
import time
from sptools import findFreq

from GSMSync import GSMSync
class GSMFineSync(GSMSync):
	def __init__(self,f,url='http://192.168.1.110:8080/'):
		GSMSync.__init__(self,f,url)


	def once( self ):
		now = self.rx.now()
		last = self.getFrameStart()
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
		inx = f.argmax()
		return inx+int(6500e3/96-1000)

	def sync(self):
		self.waitClockStable()
		ff = self.once()
		ppm = self.calcPPM(ff)
		self.AFC(ppm)
		print "freq error",ppm,"ppm"
		return ff

def main():
	fs = GSMFineSync(939.6e6)
	f0 = fs.sync()
	f1 = 0.
	while abs(f1-f0)>5:
		f1 = f0
		f0 = fs.sync()
		print "fine sync:",f0
		time.sleep(1)

if __name__ == '__main__':
	main()

