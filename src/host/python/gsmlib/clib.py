from ctypes import *
import numpy as np
class clib:
	def __init__(self,lib):
		self.lib = lib

	def viterbi_detector(self,mafi,rhh,bs):
		filtered_burst = (c_float*(bs*2))()
		stop_states = (c_int*2)()
		stop_states[0]=1
		stop_states[1]=2
		output =(c_int*bs)()
		hard   =(c_int*bs)()
		filtered_burst[::2]=mafi[:bs].real/rhh[2].real
		filtered_burst[1::2]=mafi[:bs].imag/rhh[2].real
		xrhh =(c_float*6)()
		xrhh[::2]=rhh[1:4].real/rhh[2].real
		xrhh[1::2]=rhh[1:4].imag/rhh[2].real
		self.lib.viterbi_detector( 
			  byref(filtered_burst)
			, 148
			, byref(xrhh)
			, c_int(1)
			, byref(stop_states)
			, 2
			, byref(output)
			)
		return output[:]

	def viterbi_restore(self,x,rhh,bs):
		output = (c_float*(bs*2))()
		in_put =(c_int*bs)()
		in_put[:] = x[:bs]
		xrhh =(c_float*6)()
		xrhh[::2]=rhh[1:4].real
		xrhh[1::2]=rhh[1:4].imag
		self.lib.viterbi_restore( 
			  byref(in_put)
			, 148
			, byref(xrhh)
			, c_int(1)
			, c_int(0)
			, byref(output)
			)
		return np.array([complex(output[i],output[i+1]) for i in range(0,len(output),2)])

		
		
