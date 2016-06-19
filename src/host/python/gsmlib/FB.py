import splibs
from Burst import *

class FBFix(item):
	length = 142
	bits = [0]*142

class FB(Burst):

	__field__ = [TB,FBFix,TB,NGP]
	__name__ = "FB"

	def __init__(self,sf=0):
		Burst.__init__(self,sf)

	def freqEst(self):
		r0 = splibs.autocorrelation(self.recv,1)
		omg = r0.angle()/2.*np.pi
		return omg

def main():
	a = FB()
	a.dump()
	print a.getLen()

if __name__ == '__main__':
	main()
