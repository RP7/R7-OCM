from Burst import *

class ABMessage(item):
	length = 36

class ABTraining(item):
	"""
	const BitVector2 GSM::gRACHSynchSequence("01001011011111111001100110101010001111000");
	"""
	length = 41
	cbits = "01001011011111111001100110101010001111000"
	bits = item.c2bits(cbits)


class AB(Burst):

	__field__ = [ATB,ABTraining,ABMessage,TB,AGP]
	__name__ = "AB"

	def __init__(self):
		Burst.__init__(self)

def main():
	a = AB()
	a.dump()
	print a.getLen()
	print ABTraining.bits

if __name__ == '__main__':
	main()

