from NB import NB

class DB(NB):
	__name__ = "DB"

	def __init__(self):
		NB.__init__(self)


def main():
	a = DB()
	a.dump()
	print a.getLen()

if __name__ == '__main__':
	main()

