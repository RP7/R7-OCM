import dev_mem
from const import *

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
				


def main():
	uut = axi()
	uut.reset()
	uut.dump()

if __name__ == '__main__':
	main()
