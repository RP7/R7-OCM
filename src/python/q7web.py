import web
import os
import axi2s_u
import AD9361_c
import adscripts
import axi2s_c
import json

urls = ( '/'      ,'index'
	     , '/tx'    ,'tx'
	     , '/rx'    ,'rx'
	     , '/txbuf' ,'txbuf'
	     , '/misc'  ,'misc'
	     )

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

class txbuf:
	def POST(self):
		i = web.input()
		print i
		web.header('Content-Type', 'text/json')
		return json.dumps({'ret':'ok'})

class misc:
	def GET(self):
		i = web.input(fun=None)
		axi2s = axi2s_c.axi2s_c()
		if i.fun in axi2s.api:
			ret = axi2s.api[i.fun](i)
		else:
			ret = {'ret':'err','res':'undefined fun or miss fun'}
		web.header('Content-Type', 'text/json')
		return json.dumps(ret)


def init():
	path = os.path.split(os.path.realpath(__file__))[0]
	fn = path+"/../../AD9361/ad9361_config.reg"
	f = open(fn)
	ad = AD9361_c.AD9361_c()
	for x in f.readlines():
		adscripts.parse(x,ad.order)
	ad.Check_FDD()
	ad.deinit()
	
	ocm = axi2s_u.axi2s_u()
	ocm.cleanTx()
	ocm.deinit()
	
	uut = axi2s_c.axi2s_c()
	uut.init()

	uut.check()
	uut.deinit()

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()

