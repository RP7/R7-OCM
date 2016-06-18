from ctypes import *
import GSM
import time
from sptools import findFreq

from GSMSync import GSMSync


class GSMFineSync(GSMSync):
	def __init__(self,f,url='http://192.168.1.110:8080/'):
		GSMSync.__init__(self,f,url)

	def once( self ):
		blk = self.fl/16
		rfd,start = self.getRfData(-blk,blk*3)
		f = findFreq.findFreq(rfd,6500e3/96,1000,1.92e6)
		# for i in range(4):
		# 	newStart = self.fl*10*i
		# 	rfd,start = self.getRfData(newStart-blk,blk*3)
		# 	f += findFreq.findFreq(rfd,6500e3/96,1000,1.92e6)
		inx = f.argmax()
		return inx+int(6500e3/96-1000)

	def sync(self):
		self.waitClockStable()
		ff = self.once()
		ppm = self.calcPPM(ff)
		self.AFC(ppm)
		#print "freq error",ppm,"ppm"
		return ppm

def main():
	fs = GSMFineSync(939.6e6)
	f0 = fs.sync()
	print "fine sync ppm:",f0
	while abs(f0)>0.5:
		time.sleep(1)
		f0 = fs.sync()
		print "fine sync ppm:",f0

if __name__ == '__main__':
	main()

