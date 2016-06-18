import Q7Mem
from ctypes import *
import GSMChan
import GSM
import time
from host.curlwrapper import curlwrapper

from GSMSync import GSMSync
class GSMRoughSync(GSMSync):
	def __init__(self,f,url='http://192.168.1.110:8080/'):
		GSMSync.__init__(self,f,url)

	def once( self ):
		rfd,start = self.getRfData(0,self.mfl)
		gsm = GSMChan.GSMChan(rfd)
		fMap,fpos,fm = gsm.fbsearch()
		maxa = 0
		for (p,f,a) in fpos:
			if a>maxa:
				fp,ff,fa = p,f,a
				maxa=a
		pp = fp*self.fl/16
		return pp,start+pp,ff,fa

	def sync(self):
		self.waitClockStable()
		fp,new_frame,ff,fa = self.once()
		self.setFrameStart(new_frame)
		ppm = self.calcPPM(ff)
		self.AFC(ppm)
		print "freq error",ppm,"ppm"
		return ff

def main():
	rs = GSMRoughSync(939.8e6)
	
	f0 = rs.sync()
	f1 = 0.
	while abs(f1-f0)>1e3:
		f1 = f0
		f0 = rs.sync()
		print "rough sync:",f0
		time.sleep(1)

if __name__ == '__main__':
	main()


