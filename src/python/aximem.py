from ctypes import *
from c_lib import lib

class h_aximem(Structure):
	_fields_ = [  ("u_map", c_void_p)
							, ("c_map", c_void_p)
							]

class e_aximem(Structure):
	_fields_ = [  ("base", c_uint)
							, ("size", c_uint)
							, ("acnt", c_uint)
							, ("bcnt", c_uint)
							, ("time", c_ulonglong)
							, ("start", c_ulonglong)
							, ("length", c_uint)
							, ("data", c_void_p)
							]
	def dump(self):
		return {  "base": long(self.base)
						, "size": long(self.size)
						, "acnt": long(self.acnt)
						, "bcnt": long(self.bcnt)
						, "time": long(self.time)
						, "start": long(self.start)
						, "length": long(self.length)
					}
	
class axi_dma(Structure):
	_fields_ = [  ("inp", e_aximem)
							, ("out", e_aximem)
						]
	def dump(self):
		return {  "inp":self.inp.dump()
						, "out":self.out.dump()
						}

class aximem:
	def __init__(self,config=None):
		self.handle = h_aximem()
		self.dma = axi_dma()
		if config==None:
			self.dma.inp.base = 0
			self.dma.inp.size = 0x100000
			self.dma.out.base = 0x1f00000
			self.dma.out.size = 0x100000
		else:
			base = lib.axi_base()
			self.init()

		lib.axi_init(byref(self.handle))
		self.last_inp_end = c_ulonglong(0)
		self.last_out_end = c_ulonglong(0)
		self.errcnt = {0:0,-1:0}

	def init(self,config):
			self.dma.inp.base = config['AXI2S_IBASE']-base
			self.dma.inp.size = config['AXI2S_ISIZE']
			self.dma.out.base = config['AXI2S_OBASE']-base
			self.dma.out.size = config['AXI2S_OSIZE']
		
	def dump(self):
		reg = c_uint*32
		reg_p = cast(self.handle.c_map, POINTER(reg))
		i = 0
		for x in reg_p.contents[:]:
			print "%04x:0x%08x"%(i,x)
			i += 4

	def get(self,s,l):
		self.dma.inp.start = s
		self.dma.inp.length = l
		r = lib.axi_get(byref(self.dma))
		if r==l:
			self.last_inp_end = s+l
			return self.dma.inp.data
		else:
			err = {    0:"data not ready"
							, -1:"data out of date"}
			if r in err:
				self.errcnt[r] += 1
			else:
				print "unknow reason"
			return None

	def put(self,s,l):
		self.dma.out.start = s
		self.dma.out.length = l
		r = lib.axi_put(byref(self.dma))
		if r==l:
			self.last_out_end = s+l
		else:
			err = {    0:"buffer full"
							, -1:"buffer overrun"
							, -2:"data unaligned"
							}
			if r in err:
				print err[r]
			else:
				print "unknow reason"

	def reset(self,who):
		#print "axi mem device reset:",who
		if who=="inp":
			lib.axi_now(byref(self.dma))
			self.last_inp_end = c_ulonglong(long(self.dma.inp.size)*long(self.dma.inp.bcnt))

def main():
	a = aximem()
	a.dump()

if __name__ == '__main__':
	main()