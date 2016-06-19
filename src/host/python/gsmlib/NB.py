from Burst import *

class NBMessage(item):
	length = 57

class NBM0(NBMessage):
	pass

class NBM1(NBMessage):
	pass

class LoanFlag(item):
	length = 1

class LF0(LoanFlag):
	pass

class LF1(LoanFlag):
	pass

class NBTraining(item):
	"""
	const BitVector2 GSM::gTrainingSequence[] = {
    BitVector2("00100101110000100010010111"),
    BitVector2("00101101110111100010110111"),
    BitVector2("01000011101110100100001110"),
    BitVector2("01000111101101000100011110"),
    BitVector2("00011010111001000001101011"),
    BitVector2("01001110101100000100111010"),
    BitVector2("10100111110110001010011111"),
    BitVector2("11101111000100101110111100"),
	};
	"""
	length = 26
	bits = [
	  [0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1],
	  [0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1],
	  [0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0],
	  [0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0],
	  [0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1],
	  [0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0],
	  [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1],
	  [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0],
	  [0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1] ## DUMMY
	]
	modulated = np.zeros((len(bits),length),dtype=complex)
	for i in range(len(bits)):
		modulated[i,:] = item.gmsk_mapper(bits[i],complex(0,-1)) 


class NB(Burst):

	__field__ = [TB,NBM0,LF0,NBTraining,LF1,NBM1,TB,NGP]
	__name__ = "NB"

	def __init__(self):
		Burst.__init__(self)

def main():
	a = NB()
	a.dump()
	print a.getLen()

if __name__ == '__main__':
	main()

