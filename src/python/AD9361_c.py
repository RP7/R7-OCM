import dev_mem
import reg_define as reg
from const import *
import time
import sys


class AD9361_c:
	def __init__(self):
		self.dev = dev_mem.dev_mem(AD9361_SPI_BASE,AD9361_SPI_SIZE)

	def init(self):
		pass
		
	def readreg(self,regname):
		r = self.dev.ioread(reg.addr[regname])
		print 'R:',regname, hex(r)
		return r
	
	def writereg(self,regname,data):
		self.dev.iowrite(reg.addr[regname],data)
		print 'W:',regname, hex(data)

	def spi_op(self,addr,data,wop):
		H8 = addr>>8
		H8 = H8 & 0x3
		b = len(data)
		l = (b-1)&0x7
		H8 = H8 | (l<<4)
		if wop==1:
			H8 = H8 | 0x80
		HL = addr & 0xff
		self.writereg('SPI_Config',0x4015)
		self.writereg('SPI_Tx_data',H8)
		self.writereg('SPI_Tx_data',HL)
		for i in range(b):
			self.writereg('SPI_Tx_data',data[i])
		r = 0
		#while(r==0):
		r = self.readreg('SPI_Intr_status')&0x2
		#	print "Tx FIFO underflow:",r
		self.writereg('SPI_Config',0x7c15)
		RH = self.readreg('SPI_Rx_data')
		RL = self.readreg('SPI_Rx_data')
		for i in range(b):
			data[i] = self.readreg('SPI_Rx_data')
		print "Read:",RH,RL,data[:]
		return data
		
	def readByte(self,addr):
		data=[0xff]
		data = self.spi_op(addr,data,0)
		print "R: [0x%04x]:0x%02x"%(addr,data[0])

	def writeByte(self,addr,d):
		data = [d]
		data = self.spi_op(addr,data,1)
		print "W: [0x%04x]:0x%02x"%(addr,d)

def main():
	uut = AD9361_c()
	#uut.writereg('SPI_Intrpt_en',0x3f)
	#uut.writereg('SPI_En',0)
	#uut.writereg('SPI_En',1)
	
	if len(sys.argv)>1:
		if sys.argv[1]=='S':
			if len(sys.argv)==3:
				uut.readreg(sys.argv[2])
			elif len(sys.argv)==4:
				uut.writereg(sys.argv[2],int(sys.argv[3],16))
		elif sys.argv[1]=='R':
			if len(sys.argv)==3:
				uut.readByte(int(sys.argv[2],16))
			elif len(sys.argv)==4:
				uut.writeByte(int(sys.argv[2],16),int(sys.argv[3],16))
	else:
		uut.read('SPI_Config')

if __name__ == '__main__':
	main()