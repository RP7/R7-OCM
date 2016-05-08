import dev_mem
from const import *
import sys

class axi2s_u:
	def __init__(self):
		self.dev = dev_mem.dev_mem(OCM_BASE,OCM_SIZE)

	def dump(self,offset,length):
		iLen = (length+3)/4
		r = self.dev.memread(offset,iLen)
		for i in range(0,iLen,16):
			print 'R:',
			print "%04x"%(i+offset),
			for k in range(16):
				print "%08x"%(r[i+k]),
			print ""
		
def main():
	uut = axi2s_u()
	uut.dump(int(sys.argv[1],16),int(sys.argv[2],16))

if __name__ == '__main__':
	main()