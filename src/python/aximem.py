from ctypes import *
from c_lib import lib

class c_aximem(Structure):
	_fields_ = [  ("u_map", c_void_p)
							, ("c_map", c_void_p)
							]

class aximem:
	def __init__(self):
		self.handle = c_aximem()
		lib.axi_init(byref(self.handle))

	def dump(self):
		reg = c_uint*32
		reg_p = cast(self.handle.c_map, POINTER(reg))
		i = 0
		for x in reg_p.contents[:]:
			print "%04x:0x%08x"%(i,x)
			i += 4

def main():
	a = aximem()
	a.dump()

if __name__ == '__main__':
	main()