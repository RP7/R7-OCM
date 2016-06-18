from fractions import Fraction
import numpy as np

class item:
	def getLen(self):
		if hasattr(self,"field"):
			l = 0
			for x in self.field:
				l += x.getLen()
			return l
		else:
			return self.__class__.length

	@staticmethod
	def gmsk_mapper( inp, start_point ):
		inpb = np.array(inp)*2 - 1
		o = start_point
		out = [o]
		previous_symbol = inpb[0]
		for current_symbol in inpb[1:]:
			encoded_symbol = current_symbol * previous_symbol
			o = complex(0,1)*encoded_symbol*o
			out.append(o)
			previous_symbol = current_symbol
		return np.array(out)

class TB(item):
	length = 3
	bits = [0,0,0]

class ATB(item):
	length = 8
	bits = [0]*length

class NGP(item):
	length = Fraction(33,4)

class AGP(item):
	length = Fraction(273,4)

class Burst:
	length = Fraction(625,4)
	def __init__(self):
		if hasattr(self.__class__,"__field__"):
			self.field = [ x() for x in self.__class__.__field__]
		else:
			self.field = []

	def getLen(self):
		if hasattr(self,"field"):
			l = 0
			for x in self.field:
				l += x.getLen()
			return l
		else:
			return self.__class__.length

	def dump(self):
		name = [n.__name__ for n in self.__class__.__field__]
		print name


		
		
