import GSM
from ctypes import *
import Q7Mem

class GSMChan(GSM.GSMChan):
	def __init__(self,rd):
		self.framerate = 1.92e6
		GSM.GSMChan.__init__(self,rd)

def main():
	rx = Q7Mem.rx()
	now = rx.now()
	#print now
	length = long(1920000.*0.480)
	start = now - length
	data = rx.mmap(length*4,start*4)
	gsm = GSMChan(data)
	fMap,fpos,fm = gsm.fbsearch()
	#print fMap,fpos,fm
	return fMap,fpos,fm

if __name__ == '__main__':
	fMap,fpos,fm = main()	