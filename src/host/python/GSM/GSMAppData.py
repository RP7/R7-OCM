from ctypes import *
class GSMAppData(Structure):
	_fields_ =  [   ("frame_start_point", c_ulonglong)
								, ("offset", c_ulonglong)
						]
