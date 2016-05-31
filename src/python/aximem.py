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
							, ("data", c_void_p)
							]
	
class axi_dma(Structure):
	_fields_ = [  ("inp", e_aximem)
							, ("out", e_aximem)
						]

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
			self.dma.inp.base = config['AXI_IBASE']-base
			self.dma.inp.size = config['AXI_ISIZE']
			self.dma.out.base = config['AXI_OBASE']-base
			self.dma.out.size = config['AXI_OSIZE']

		lib.axi_init(byref(self.handle))
		self.last_inp_end = c_ulonglong(0)
		self.last_out_end = c_ulonglong(0)
		
	def dump(self):
		reg = c_uint*32
		reg_p = cast(self.handle.c_map, POINTER(reg))
		i = 0
		for x in reg_p.contents[:]:
			print "%04x:0x%08x"%(i,x)
			i += 4

	def get(self,s,l):
		r = lib.axi_get(s,l,byref(self.dma))
		if r==l:
			self.last_inp_end = s+l
			return self.dma.inp.data
		else:
			err = {    0:"data not ready"
							, -1:"data out of date"}
			if r in err:
				print err[r]
			else:
				print "unknow reason"
			return None

	def put(self,s,l):
		r = lib.axi_put(s,l,byref(self.dma))
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
		if who=="inp":
			lib.axi_now(byref(self.dma))
			self.last_inp_end = self.dma.inp.size*self.dma.inp.bcnt

def main():
	a = aximem()
	a.dump()

if __name__ == '__main__':
	main()