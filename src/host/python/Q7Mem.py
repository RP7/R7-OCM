from ctypes import *
from constant import c_temp_dir
import sys
import time

class Q7Mem:

	def __init__(self):
		fn = c_temp_dir + 'libQ7.so'
		self.lib = CDLL(fn)
		self.blk = 4096
		self.offset = 0L
		self.cnt = 0

		c_int64_funcs = [
			  "chipNow"  #int64_t chipNow( Q7Mem *h );
  			, "cpuNow"   #int64_t cpuNow( Q7Mem *h );
			, "cpu2chip" #int64_t cpu2chip( Q7Mem *h, int64_t c );
		]
		
		self.lib.chipNow.restype = c_int64
		self.lib.cpuNow.restype = c_int64
		self.lib.cpu2chip.restype = c_int64
				
		self.lib.getAddr.restype = c_void_p
		self.lib.appData.restype = c_void_p

	def _off( self ):
		t_offset = (c_long*1)()
		self.lib.offset( self.h, t_offset )
		return long(t_offset[0])
	
	def dump( self ):
		self.lib.dumpQ7Mem( self.h )

	def mmap( self, l, off ):
		addr = self.lib.getAddr( self.h, c_long(off) )
		vbuf = cast( addr, POINTER(c_short*(l/2)) )
		return vbuf.contents
 
	def appData(self,types):
		addr = self.lib.appData(self.h)
		vbuf = cast( addr, POINTER(types) )
		return vbuf.contents

class rx(Q7Mem):
	def __init__(self):
		Q7Mem.__init__(self)
		self.h = self.lib.attachQ7Mem('rx_udp.d')
		#self.lib.dumpQ7Mem( self.h )
		self.cap_size = self.lib.mSize( self.h )
		#print "Capture Mem Size",self.cap_size
		self.start = self._off()
		
	def read( self, l, off ):
		pos = long(self.start+off)
		while self._off()<long(pos+self.blk*2):
			time.sleep(0.001)
			self.cnt += 1
			if (self.cnt%1000)==0:
				print "time out, no packet recv",self._off(),pos
				break
		return self.mmap( l, pos )
 
	def get( self ):
		self.offset += self.blk
		buf = self.read( self.blk, self.offset )
		return buf

	def now( self ):
		n = long(self.lib.chipNow( self.h ))
		return n/4

	def clkRate( self ):
		return self.lib.clkRate( self.h )

class tx(Q7Mem):
	def __init__(self):
		Q7Mem.__init__(self)
		self.h = self.lib.attachQ7Mem('tx_udp.d')
		#self.lib.dumpQ7Mem( self.h )

		self.sendbuf_size = self.lib.mSize( self.h )
		#print "Send Mem Size",self.sendbuf_size
		self.start = self._off()
		
	def put( self, buf ):
		self.write( buf, len(buf)*2, self.offset )
		self.offset += len(buf)*2
		
	def write( self, buf, l, off ):
		pos = long(self.start+off)
		read_head = long(self._off())
		while read_head<long(pos-self.blk*30):
			time.sleep(0.001)
			read_head = long(self._off())
			self.cnt += 1
			if (self.cnt%1000)==0:
				print "time out, no packet send",self._off(),pos
				break
		self.lib.Q7write( self.h, byref(buf), l, c_long(pos) )

def main():
	rxmem = rx()
	s = rxmem.now()
	f = open("../../../temp/rd.dat","wb")
	a = rxmem.mmap(1024*1024*2,s*4-1024*1024*2)
	f.write(string_at(addressof(a),1024*1024*2))
	f.close()
	for i in range(10):
		e = rxmem.now()
		print e-s,":"
		s = e
		rxmem.dump()
		time.sleep(1)

if __name__ == '__main__':
	main()