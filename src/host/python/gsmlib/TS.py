from FB import FB
from SB import SB
from NB import NB
from DB import DB

class TS0:
	__field__ = ([FB,SB]+[NB]*8)*5+[DB]

class TS1:
	__field__ = ([NB]*48+[DB]*3)*2

class TST:
	__field__ = ([NB]*12 + [DB])*2

class Frame:
	def __init__(self):
		self.ts0_off = 0
		self.ts1_off = 0
		self.tst_off = 0
	
	def config(self,fnum):
		ts0 = (self.ts0_off+fnum)%len(TS0.__field__)
		ts1 = (self.ts1_off+fnum)%len(TS1.__field__)
		tst = (self.tst_off+fnum)%len(TST.__field__)
		ret = []
		for i in len(self.__class__.__TS__):
			x = self.__class__.__TS__[i]
			if x==TS0:
				b = TS0.__field__[ts0]
			elif x==TS1:
				b = TS0.__field__[ts1]
			elif x==TST:
				b = TS0.__field__[tst]
			else:
				raise TSError
			b.set(fnum,i)
			ret.appen(b)

		return ret

	def build(self,frames):
		self.frame = []
		for i in range(frames):
			self.frame.append(self.config(i))

	def name(self,field):
		ret = [x.__name__ for x in field]
		return ret

	def getLen(self,field):
		l = 0
		for f in field:
			l += f.getLen()
		return l

class CFrame(Frame):
	__TS__ = [ TS0, TS1 ] + [TST]*6
	def __init__(self):
		Frame.__init__(self)

class TFrame(Frame):
	__TS__ = [TST]*8
	def __init__(self):
		Frame.__init__(self)

def main():
	C0 = CFrame()
	for i in range(51):
		f = C0.config(i)
		print C0.name(f),C0.getLen(f)


if __name__ == '__main__':
	main()