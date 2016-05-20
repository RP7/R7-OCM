import dev_mem
import reg_define as reg
from const import *
import time
import sys

class axi2s_c:
	def __init__(self):
		self.dev = dev_mem.dev_mem(FPGA_BASE,FPGA_SIZE)

	def version(self):
		major = self.read('VER_MAJOR')
		minor_reg = reg.addr['VER_MINOR0']
		minor = []
		for i in range(5):
			regname = 'VER_MINOR%d'%i
			minor.append(self.read(regname))
			minor_reg += 4
		i = 4
		print 'git hash:'
		while i>=0:
			print '%08x'%(minor[i]),
			i -= 1
		print ''

	def check(self):
		time.sleep(1)
		self.read('AXI2S_IACNT')
		self.read('AXI2S_IBCNT')
		self.read('AXI2S_OACNT')
		self.read('AXI2S_OBCNT')
		self.read('AXI_RRESP')
		self.read('AXI_WRESP')
		self.read('AXI_STATUS')
		self.read('AXI_RADDR')
		self.read('AXI_WADDR')
		self.version()

	def init(self):
		self.read('AXI2S_STATE')
		self.write('AXI2S_IBASE',0xfffc0000)
		self.write('AXI2S_ISIZE',0x10000)
		self.write('AXI2S_OBASE',0xfffd0000)
		self.write('AXI2S_OSIZE',0x10000)
		self.write('AXI2S_EN',IEN|OEN)
		self.read('AXI2S_STATE')
		
	def initDRAM(self):
		self.read('AXI2S_STATE')
		self.write('AXI2S_IBASE',0x1ffc0000)
		self.write('AXI2S_ISIZE',0x10000)
		self.write('AXI2S_OBASE',0x1ffd0000)
		self.write('AXI2S_OSIZE',0x10000)
		self.write('AXI2S_EN',IEN|OEN)
		self.read('AXI2S_STATE')

	def read(self,regname):
		r = self.dev.ioread(reg.addr[regname])
		print 'R:',regname, hex(r)
		return r
	
	def write(self,regname,data):
		self.dev.iowrite(reg.addr[regname],data)
		print 'W:',regname, hex(data)
	def deinit(self):
		self.dev.deinit()
		
def main():
	uut = axi2s_c()
	uut.write('AXI2S_EN',0)
	if sys.argv[1]=='DRAM':
		uut.initDRAM()
	else:
		uut.init()
	uut.check()

if __name__ == '__main__':
	main()