import os

class ad9361_fir:
	"""
  ----------------------------------------------------------------------------------------
	|reg 0x60 TX Filter Coefficient Address<7:0>         - reg 0xF0 RX                     |
  ----------------------------------------------------------------------------------------
	|reg 0x61 TX Filter coefficient Write Data <7:0>     - reg 0xF1 RX                     |
  ----------------------------------------------------------------------------------------
	|reg 0x62 TX Filter coefficient Write Data <15:8>    - reg 0xF2 RX                     |
	----------------------------------------------------------------------------------------
	|reg 0x63 TX Filter coefficient Read Data<7:0>       - reg 0xF3 RX                     |
	----------------------------------------------------------------------------------------
	|reg 0x64 TX Filter coefficient Read Data<15:8>      - reg 0xF4 RX                     |
	----------------------------------------------------------------------------------------
	|reg 0x65 TX Filter Configuration                    - reg 0xF5 RX                     |
	----------------------------------------------------------------------------------------
	|       bit7:5       |      bit4:3       |   bit2    |     bit1       |      bit0      | 
	|Number of Taps<2:0> | Select Tx CH<1:0> | Write Tx  | Start Tx Clock | Tx Filter Gain |
	----------------------------------------------------------------------------------------
	|reg 0xF6 RX Filter Gain bit1:0         | 3 -12dB | 2 -6dB | 1 0dB (default) | 0  +6dB |
	----------------------------------------------------------------------------------------
	"""
	def __init__(self,txrx='tx',port=1):
		self.regname = {'addr':0,'wdataL':1,'wdataH':2,'rdataL':3,'rdataH':4,'config':5,'rxgain':6}
		self.base = {'tx':0x60,'rx':0xf0}
		self.txrx = txrx
		self.port = port
		self.order = []
	
	def add(self,r,v):
		self.order.append((self.base[self.txrx]+self.regname[r],v))
	
	def start(self,taps,g):
		t =(taps+15)/16-1
		v = (t&0x7)<<5
		v |= (self.port&3)<<3
		v |= 0x2
		if self.txrx=='tx':
			v |= g&1 
		self.add('config',v)
		if self.txrx=='rx':
			self.add('rxgain',g&3)
		self.config = v
			
	def coeff(self,n,v):
		self.add('addr',n)
		self.add('wdataL',v&0xff)
		self.add('wdataH',(v>>8)&0xff)
		self.add('config',self.config|4)
		self.add('rdataH',0)
		self.add('rdataH',0)
		
	def end(self):
		self.add('config',self.config)
		self.add('config',self.config&0xfd)

	def build(self,coeffs,g):
		l = len(coeffs)
		if l<=128 and l>0:
			self.start(l,g)
			for i in range(l):
				self.coeff(i,coeffs[i])
		self.end()

	def split(self,x):
		return x.split(',')
	
	def toScript(self):
		self.script = ""
		for (r,v) in self.order:
			self.script += 'SPIWrite\t%03X,%02X\n'%(r,v)

	def fromfile(self,fn):
		f = open(fn)
		lines = f.readlines()
		self.fromlines(lines)

	def fromlines(self,lines):
		name = [a[:2].lower() for a in self.split(lines[0])]
		gain = [int(a[5:]) for a in self.split(lines[1])]
		self.fir = {}
		for (a,b) in zip(name,gain):
			self.fir[a] = {'gain':b,'coeffs':[]}
		for line in lines[2:]:
			if len(line)>1:
				for (a,b) in zip(name,self.split(line)):
					self.fir[a]['coeffs'].append(int(b))

	def download(self,spiwrite):
		for (r,v) in self.order:
			spiwrite(r,v)

	def fromcheadfile(self,fn):
		f = open(fn)
		s = f.read()
		return self.fromchead(s)
		
	def fromchead(self,s):
		scoeff = self.getCoeff(s)
		scoeffs = scoeff.split(',')
		coeffs = []
		for s in scoeffs:
			coeffs.append(int(s))
		return coeffs
		
	def getCoeff(self,s):
		ss = s.split('{')
		sss = ss[1].split('}')
		return sss[0]

def main():
	path = os.path.split(os.path.realpath(__file__))[0]
	fn = path+"/../../AD9361/200K_1920K.h"
	uut = ad9361_fir(port=3)
	c = uut.fromcheadfile(fn)
	print c

def main_0():
	path = os.path.split(os.path.realpath(__file__))[0]
	fn = path+"/../../AD9361/LTE1p4_MHz.ftr"
	uut = ad9361_fir(port=3)
	uut.fromfile(fn)
	print uut.fir
	for n in uut.fir:
		if n in ['tx','rx']:
			uut.txrx = n
			if 'port' in uut.fir[n]:
				uut.port = uut.fir[n]['port']
			uut.build(uut.fir[n]['coeffs'],uut.fir[n]['gain'])
	uut.toScript()
	print uut.script

if __name__ == '__main__':
	main()




		
		
