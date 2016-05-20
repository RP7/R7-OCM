import dev_mem
from const import *
import sys

class axi:
	def __init__(self):
		self.dev = dev_mem.dev_mem(AXIC_BASE,AXIC_SIZE)

	def dump(self):
		for i in range(0x8000,0x8028,4):
			r = self.dev.ioread(i)
			print '[0x%02x]=0x%08x'%(i,r)

	def reset(self):
		r = self.dev.ioread(0x240)
		print 'before reset',hex(r)
		b = r|2
		self.dev.iowrite(0x240,b)
		b = self.dev.ioread(0x240)
		print 'after reset',hex(b)
		b -= 2
		self.dev.iowrite(0x240,b)
		r = self.dev.ioread(0x240)
		print 'reset ok',hex(r)
				
	def read(self,reg):
		r = self.dev.ioread(reg)
		print 'R:',hex(reg), hex(r)
		return r
	
	def write(self,reg,data):
		self.dev.iowrite(reg,data)
		print 'W:',hex(reg), hex(data)

	def ocm_tz(self):
		self.write(0x400,0xffffffff)
		self.write(0x404,0xffffffff)

def main():
	uut = axi()
	#uut.ocm_tz()
	if len(sys.argv)==2:
		uut.read(int(sys.argv[1],16))
	elif len(sys.argv)==3:
		uut.write(int(sys.argv[1],16),int(sys.argv[2],16))
	else:
		main_0()

def main_0():
	uut = axi()
	uut.reset()
	uut.dump()

if __name__ == '__main__':
	main()
