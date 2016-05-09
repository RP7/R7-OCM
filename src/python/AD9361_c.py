import dev_mem
import reg_define as reg
from const import *
import time

class AD9361_c:
	def __init__(self):
		self.dev = dev_mem.dev_mem(AD9361_SPI_BASE,AD9361_SPI_SIZE)

	def init(self):
		pass
		
	def read(self,regname):
		r = self.dev.ioread(reg.addr[regname])
		print 'R:',regname, hex(r)
		return r
	
	def write(self,regname,data):
		self.dev.iowrite(reg.addr[regname],data)
		print 'W:',regname, hex(data)

def main():
	uut = AD9361_c()
	uut.read('SPI_Config')

if __name__ == '__main__':
	main()