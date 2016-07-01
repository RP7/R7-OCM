import AD9361_c
import axi2s_c
import aximem

class config:
	def __init__(self):
		self.AXI2S_IBASE = 0x1e000000
		self.AXI2S_ISIZE = 0xea6000
		self.AXI2S_OBASE = 0x1f000000
		self.AXI2S_OSIZE = 0xea6000
		self.rx    = {
				'freq':940.1e6
			, 'gain': [68,68]
			}
		self.aximem = aximem.aximem()
		self.udpSrv = None
		self.FM = None
		self.port = 10000
		self.scan = None
		
	def todict(self):
		r = {}
		for k in ['AXI2S_IBASE','AXI2S_ISIZE','AXI2S_OBASE','AXI2S_OSIZE','rx','port']:
			r[k] = self.__dict__[k]
		return r
	
	def init(self):
		c = self.todict()
		axi2s = axi2s_c.axi2s_c(c)
		ad = AD9361_c.AD9361_c()
		axi2s.init()
		ad.webapi['rx']['set']['freq'](self.rx['freq'])
		ad.webapi['rx']['set']['gain'](self.rx['gain'][0],0)
		ad.webapi['rx']['set']['gain'](self.rx['gain'][0],1)
		self.aximem.init(c)
		self.aximem.reset("inp")
		ad.Check_FDD()
		return c
