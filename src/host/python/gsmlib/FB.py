from Burst import *

class FBFix(item):
	length = 142
	bits = [0]*142

class FB(Burst):

	__field__ = [TB,FBFix,TB,NGP]
	__name__ = "FB"

	def __init__(self):
		Burst.__init__(self)

def main():
	a = FB()
	a.dump()
	print a.getLen()

if __name__ == '__main__':
	main()
