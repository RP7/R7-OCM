from ctypes import *
from c_lib import lib

class c_aximem(Structure):
	_fields_ = [  ("u_map", c_void_p)
							, ("c_map", c_void_p)
							]
class axi_config(Structure):
	_fields_ = [  ("in", c_uint)
							, ("is", c_uint)
							, ("out", c_uint)
							, ("os", c_uint)
							, ("point",c_void_p)
							]

class aximem:
	def __init__(self):
		self.handle = c_aximem()
		self.config = axi_config(0,0x100000,0x1f00000,0x100000)
		lib.axi_init(byref(self.handle))

	def dump(self):
		reg = c_uint*32
		reg_p = cast(self.handle.c_map, POINTER(reg))
		i = 0
		for x in reg_p.contents[:]:
			print "%04x:0x%08x"%(i,x)
			i += 4

	def get(self,s,l):
		r = lib.axi_get(s,l,byref(self.config))
		if r==l:
			return self.config.point
		else:
			return None

	def put(self,s,l):
		pass

def main():
	a = aximem()
	a.dump()

if __name__ == '__main__':
	main()