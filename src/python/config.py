import AD9361_c
import axi2s_c

class config:
	def __init__(self):
		self.AXI2S_IBASE = 0xfffc0000
		self.AXI2S_ISIZE = 0x10000
		self.AXI2S_OBASE = 0xfffd0000
		self.AXI2S_OSIZE = 0x10000
		self.rx    = {
				'freq':940.1e6
			, 'gain': [68,68]
			}

	def todict(self):
		r = {}
		for k in ['AXI2S_IBASE','AXI2S_ISIZE','AXI2S_OBASE','AXI2S_OSIZE','rx']:
			r[k] = self.__dict__[k]
		return r
	
	def init(self):
		axi2s = axi2s_c.axi2s_c(_g.todict())
		ad = AD9361_c.AD9361_c()
		axi2s.init()
		ad.webapi['rx']['set']['freq'](self.rx['freq'])
		ad.webapi['rx']['set']['gain'](self.rx['gain'][0],0)
		ad.webapi['rx']['set']['gain'](self.rx['gain'][0],1)
		return self.todict()
