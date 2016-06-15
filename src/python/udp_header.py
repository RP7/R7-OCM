from ctypes import *

class udp_header(Structure):
	_fields_ =  [  ("time", c_ulonglong)
							, ("offset", c_ulonglong)
						]

class udp_package(Structure):
	_fields_ =  [  ("header", udp_header)
							, ("data", c_char*1024)
						]
						
def struct2stream(s):
	length  = sizeof(s)
	p       = cast(pointer(s), POINTER(c_char * length))
	return p.contents.raw

def stream2struct(string, stype):
	if not issubclass(stype, Structure):
		raise ValueError('The type of the struct is not a ctypes.Structure')
	length      = sizeof(stype)
	stream      = (c_char * length)()
	stream.raw  = string
	p           = cast(stream, POINTER(stype))
	return p.contents
