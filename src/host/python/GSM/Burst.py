import numpy as np

class Burst:
	slot = 625
	def __init__(self):
		pass
	def diff(self,s):
		r = []
		for i in range(len(s)-4):
			a = s[i+4]*np.conj(s[i])
			r.append(a.imag)
		return r
