from Burst import *

class ABMessage(item):
	length = 36

class ABTraining(item):
	length = 41

class AB(Burst):

	__field__ = [ATB,ABTraining,ABMessage,TB,AGP]
	__name__ = "AB"

	def __init__(self):
		Burst.__init__(self)

def main():
	a = AB()
	a.dump()
	print a.getLen()

if __name__ == '__main__':
	main()

