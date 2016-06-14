import GSM
from ctypes import *

class udp_GSM(GSM.GSMChan):
	def __init__(self,rd):
		self.framerate = 1.92e6
		self.nframes = len(rd)
		GSM.GSMChan.__init__(self,rd)

def main():
	frd = open('../../temp/rd.dat','rb')
	buf = frd.read(1920000*4)
	ty = c_uint*1920000
	d = ty.from_buffer(bytearray(buf))
	gsm = udp_GSM(d)
	fMap,fpos,fm = gsm.fbsearch()
	print fMap,fpos,fm
	return fMap,fpos,fm

if __name__ == '__main__':
	fMap,fpos,fm = main()	