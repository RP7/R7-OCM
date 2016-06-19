from NB import NB
from Burst import item

class DB(NB):
	__name__ = "DB"
	cbits = "0001111101101110110000010100100111000001001000100000001111100011100010111000101110001010111010010100011001100111001111010011111000100101111101010000"
	bits = item.c2bits(cbits)

	def __init__(self):
		NB.__init__(self)


def main():
	a = DB()
	a.dump()
	print a.getLen()
	print a.__class__.bits

if __name__ == '__main__':
	main()

