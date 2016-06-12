import web
import os
import axi2s_u
import AD9361_c
import adscripts
import axi2s_c
import json
import time
from download import downloadThread 
import base64
import ad9361_fir
import config
import udp_server
import FM

urls = ( '/'      ,'index'
	     , '/tx'    ,'tx'
	     , '/rx'    ,'rx'
	     , '/txbuf' ,'txbuf'
	     , '/rxbuf' ,'rxbuf'
	     , '/misc'  ,'misc'
	     , '/data'  ,'data'
	     , '/fir'   ,'fir'
	     , '/init'  ,'initapi'
	     , '/udp'   , 'udp'
			 , '/FM'    , 'FMAPI'
	     )


_g = config.config()

class initapi:
	def GET(self):
		i = web.input()
		if 'IBASE' in i:
			_g.AXI2S_IBASE = int(i.IBASE,16)
		if 'ISIZE' in i:
			_g.AXI2S_ISIZE = int(i.ISIZE,16)
		if 'OBASE' in i:
			_g.AXI2S_OBASE = int(i.OBASE,16)
		if 'OSIZE' in i:
			_g.AXI2S_OSIZE = int(i.OSIZE,16)
		if 'rx' in i:
			if 'freq' in i:
				_g.rx['freq'] = float(i.freq)
			if 'gain' in i:
				if 'port' in i:
					if i.port=='0':
						_g.rx['gain'][0] = int(i.gain)
					else:
						_g.rx['gain'][1] = int(i.gain)
				else:
					_g.rx['gain'][0] = int(i.gain)
					_g.rx['gain'][1] = int(i.gain)
		init_res = _g.init()

		ret = {'ret':'ok','data':init_res}
		web.header('Content-Type', 'text/json')
		return json.dumps(ret)		

class index:
	def GET(self):
		web.redirect('static/index.html')

class txrx:
	def GET(self):
		ret = {'ret':'ok'}
		i = web.input(freq=None,gain=None,sample=None,start=None,port=None)
		if i.freq!=None:
			if i.freq=="":
				ret['data']={'freq':self.ad.webapi[self.name]['get']['freq']()}
			else:
				self.ad.webapi[self.name]['set']['freq'](float(i.freq))
		if i.gain!=None:
			if i.port==None:
				p = [1,2]
			else:
				p = [int(i.port)]
			if i.gain=="":
				ret['data']={}
				ret['data']['gain']={}
				for pp in p:
					ret['data']['gain'][pp]=self.ad.webapi[self.name]['get']['gain'](pp)
			else:
				for pp in p:
					self.ad.webapi[self.name]['set']['gain'](float(i.gain),pp)
			
		if i.sample!=None:
			ret['ret']='not implement'
		return ret
	
class tx(txrx):
	def GET(self):
		self.ad = AD9361_c.AD9361_c()
		self.name = 'tx'
		ret = txrx.GET(self)
		self.ad.deinit()
		web.header('Content-Type', 'text/json')
		return json.dumps(ret)

class rx(txrx):
	def GET(self):
		self.ad = AD9361_c.AD9361_c()
		self.name = 'rx'
		ret = txrx.GET(self)
		self.ad.deinit()
		web.header('Content-Type', 'text/json')
		return json.dumps(ret)

class paser:
	def paser(self,member,i):
		if member in i:
			ret = int(i[member])
		else:
			ret = 0
		return ret
	
	def paser3(self,i):
		self.axi2s = axi2s_c.axi2s_c(_g.todict())
		self.axi2s.getCNT()
		self.start = self.paser('start',i)
		self.len = self.paser('samples',i)*4
		self.frame = self.paser('frame',i)

class txbuf:
	def POST(self):
		i = web.input()
		print i
		web.header('Content-Type', 'text/json')
		return json.dumps({'ret':'ok'})

class rxbuf(paser):
	def GET(self):
		i = web.input()
		paser.paser3(self,i)
		if self.frame==0:
			self.frame = self.axi2s.cnt['AXI2S_IBCNT']
		sp = self.axi2s.IinBuf(self.frame,self.start)
		ep = self.axi2s.IinBuf(self.frame,self.start+self.len)
		ret = {'cnt':self.axi2s.cnt,'start':self.start,'frame':self.frame,'len':self.len}
		print 'sp',sp,'ep',ep	
		if sp==0 and ep==0:
			mem = axi2s_u.axi2s_u()
			web.header('Content-Type', 'application/octet-stream')
			if self.start+self.len<=self.axi2s.base['AXI2S_ISIZE']:
				buf = mem.dev.bufread(self.start,self.len)
				return buf
		else:
			web.header('Content-Type', 'text/json')
			if sp>0:
				return json.dumps({'ret':'err','res':'Data not ready','data':ret})
			elif ep>0 and sp==0:
				return json.dumps({'ret':'err','res':'Data not all ready','data':ret})
			elif ep==0 and sp<0:
				return json.dumps({'ret':'err','res':'Data not all valid','data':ret})
			elif ep<0:
				return json.dumps({'ret':'err','res':'Data not in buf','data':ret})
		web.header('Content-Type', 'text/json')
		return json.dumps({'ret':'err','res':'unknow','cnt':self.axi2s.cnt,'data':ret})

class misc:
	def GET(self):
		i = web.input(fun=None)
		axi2s = axi2s_c.axi2s_c(_g.todict())
		ad = AD9361_c.AD9361_c()
		if i.fun in axi2s.api:
			ret = axi2s.api[i.fun](i)
		elif i.fun in ad.api:
			ret = ad.api[i.fun](i)
		else:
			ret = {'ret':'err','res':'undefined fun or miss fun'}
		web.header('Content-Type', 'text/json')
		return json.dumps(ret)
	
	def POST(self):
		i = web.input()
		web.header('Content-Type', 'text/json')
		if 'adscripts' in i:
			ad = AD9361_c.AD9361_c()
			lines = i.adscripts.split('\n')
			for x in lines:
				adscripts.parse(x,ad.order)
			return json.dumps({'ret':'ok'})
		elif 'bit' in i:
			f = open('/tmp/bit','w')
			f.write(i.bit)
			f.close()
			downloadThread('download','/tmp/bit').start()
			return json.dumps({'ret':'ok'})
		return json.dumps({'ret':'err','res':'not bit or adscripts'})

class fir:
	def POST(self):
		i = web.input()
		web.header('Content-Type', 'text/json')
		ad = AD9361_c.AD9361_c()
		ftr = ad9361_fir.ad9361_fir(port=3)
		if 'fir' in i:
			lines = i.fir.split('\n')
			ftr.fromlines(lines)
			for n in ftr.fir:
				if n in ['tx','rx']:
					ftr.txrx = n
					if 'port' in ftr.fir[n]:
						ftr.port = ftr.fir[n]['port']
					ftr.build(ftr.fir[n]['coeffs'],ftr.fir[n]['gain'])
			ad.cntrWrite('AD9361_EN',0)
			ftr.download(ad.SPIWrite)
			ad.Check_FDD()
			return json.dumps({'ret':'ok'})
		elif 'chead' in i:
			if 'rx' in i:
				ftr.txrx = 'rx'
			elif 'tx' in i:
				ftr.txrx = 'tx'
			else:
				ftr.txrx = 'rx'
			if 'port' in i:
				ftr.port = int(i.port)
			if 'gain' in i:
				g = int(i.gain)
			else:
				g = 0
			coeffs = ftr.fromchead(i.chead)
			ftr.build(coeffs,g)
			ad.cntrWrite('AD9361_EN',0)
			ftr.download(ad.SPIWrite)
			ad.Check_FDD()
			return json.dumps({'ret':'ok'})	
		return json.dumps({'ret':'err','res':'not fir coeff'})

class data:
	def GET(self):
		ram = axi2s_u.axi2s_u(_g.AXI2S_IBASE,_g.AXI2S_ISIZE)
		r = ram.rfdata()
		ram.deinit()
		web.header('Content-Type', 'text/json')
		return json.dumps(r)
		
class udp:
	def GET(self):
		i = web.input()
		web.header('Content-Type', 'text/json')
		if 'stop' in i:
			if _g.udpSrv!=None:
				_g.udpSrv.exit()
				_g.udpSrv = None
			return json.dumps({"ret":"ok","data":_g.aximem.dma.dump(),"err":_g.aximem.errcnt})
		if 'info' in i:
			_g.aximem.peer()
			if _g.udpSrv!=None:
				return json.dumps({"ret":"ok","data":_g.aximem.dma.dump(),"err":_g.aximem.errcnt,"server":_g.udpSrv.dump()})
			else:
				return json.dumps({"ret":"ok","data":_g.aximem.dma.dump(),"err":_g.aximem.errcnt})
		if 'port' in i:
			_g.port = int(i.port)
		else:
			_g.port = 10000
		if _g.udpSrv!=None:
				_g.udpSrv.exit()
		c = _g.todict()
		axi2s = axi2s_c.axi2s_c(c)
		_g.udpSrv = udp_server.udp_server()
		_g.udpSrv.aximem = _g.aximem
		_g.udpSrv.aximem.init(c)
		axi2s.init()
		_g.aximem.reset("inp")
		_g.udpSrv.run()
		return json.dumps({"ret":"ok"})

class FMAPI:
	def GET(self):
		i = web.input()
		web.header('Content-Type', 'text/json')
		if 'stop' in i:
			if _g.FM!=None:
				_g.FM.exit()
				_g.FM = None
			return json.dumps({"ret":"ok"})
		if 'info' in i:
			if _g.FM!=None:
				return json.dumps({"ret":"ok","data":_g.FM.aximem.dma.dump(),"err":_g.FM.aximem.errcnt,"fm":_g.FM.info()})
			else:
				return json.dumps({"ret":"ok","err":"FM not install"})
		if 'start' in i:
			if _g.FM!=None:
				_g.FM.exit()
			c = _g.todict()
			axi2s = axi2s_c.axi2s_c(c)
			_g.FM = FM.FM(2560*8)
			_g.FM.config(c)
			_g.FM.aximem.init(c)
			axi2s.init()
			_g.FM.run()
			return json.dumps({"ret":"ok"})
		if 'data' in i:
			if _g.FM!=None:
				web.header('Content-Type', 'application/octet-stream')
				buf = _g.FM.out()
				return buf
			else:
				return json.dumps({"ret":"ok","err":"FM not install"})

def init():
	path = os.path.split(os.path.realpath(__file__))[0]
	fn = path+"/../../AD9361/ad9361_config.reg"
	f = open(fn)
	ad = AD9361_c.AD9361_c()
	for x in f.readlines():
		adscripts.parse(x,ad.order)
	ad.Check_FDD()
	ad.deinit()
	
	# ocm = axi2s_u.axi2s_u()
	# ocm.cleanTx()
	# ocm.deinit()
	
	# uut = axi2s_c.axi2s_c(_g.todict())
	# uut.init()

	# uut.check()
	# uut.deinit()
	_g.init()
	
if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()

