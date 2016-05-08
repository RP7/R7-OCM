import dev_mem
import reg_define as reg
from const import *
import time

class axi2s_c:
	def __init__(self):
		self.dev = dev_mem.dev_mem(FPGA_BASE,FPGA_SIZE)

	def init(self):
		self.read('AXI2S_STATE')
		self.write('AXI2S_IBASE',0xfffc0000)
		self.write('AXI2S_ISIZE',0x10000)
		self.write('AXI2S_OBASE',0xfffd0000)
		self.write('AXI2S_OSIZE',0x10000)
		self.write('AXI2S_EN',IEN|OEN)
		self.read('AXI2S_STATE')
		time.sleep(1)
		self.read('AXI2S_IACNT')
		self.read('AXI2S_IBCNT')
		self.read('AXI2S_OACNT')
		self.read('AXI2S_OBCNT')
		
	def read(self,regname):
		r = self.dev.ioread(reg.addr[regname])
		print 'R:',regname, hex(r)
		return r
	
	def write(self,regname,data):
		self.dev.iowrite(reg.addr[regname],data)
		print 'W:',regname, hex(data)

def main():
	uut = axi2s_c()
	uut.init()

if __name__ == '__main__':
	main()