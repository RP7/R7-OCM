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

