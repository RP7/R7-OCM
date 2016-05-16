import c_lib
import sys
import ctypes

class spi:
	def __init__(self):
		pass
	def writeByte(self,a,d):
		c_lib.lib.ad9361_spi_write(a,d)
	
	def readByte(self,a):
		return c_lib.lib.ad9361_spi_read(a)&0xff

	def writeByteNW(self,a,d):
		buf = (ctypes.c_int*3)()
		a = a&0x3ff
		buf[0] = a>>8
		buf[0] |= 0x80
		buf[1] = a&0xff
		buf[2] = d&0xff
		c_lib.lib.writeNoWait(ctypes.byref(buf),3)

	def readByteNW(self,a):
		return c_lib.lib.readNoWait(a)&0xff

	def readSPI_C(self,a):
		return c_lib.lib.readSPI_C(a);

	def writeSPI_C(self,a):
		return c_lib.lib.writeSPI_C(a);

def main_0():
	c_lib.init()
	#c_lib.lib.RESET_AD9361()
	uut = spi()
	if len(sys.argv)==2:
		print hex(uut.readSPI_C(int(sys.argv[1],16)))
	elif len(sys.argv)==3:
		uut.writeSPI_C(int(sys.argv[1],16),int(sys.argv[2],16))

def main_1():
	c_lib.init()
	#c_lib.lib.RESET_AD9361()
	uut = spi()
	if len(sys.argv)==2:
		print hex(uut.readByte(int(sys.argv[1],16)))
	elif len(sys.argv)==3:
		uut.writeByte(int(sys.argv[1],16),int(sys.argv[2],16))

def main():
	c_lib.init()
	#c_lib.lib.RESET_AD9361()
	uut = spi()
	if len(sys.argv)==2:
		print hex(uut.readByteNW(int(sys.argv[1],16)))
	elif len(sys.argv)==3:
		uut.writeByteNW(int(sys.argv[1],16),int(sys.argv[2],16))

if __name__ == '__main__':
	main()
	