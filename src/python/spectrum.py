import web
import os
import axi2s_u
import AD9361_c
import adscripts
import axi2s_c
import json

urls = ('/','index','/data','data','/freq','freq')
class index:
	def GET(self):
		web.redirect('static/index.html')

class data:
	def GET(self):
		ocm = axi2s_u.axi2s_u()
		r = ocm.rfdata()
		ocm.deinit()
		web.header('Content-Type', 'text/json')
		return json.dumps(r)

class freq:
	def GET(self):
		i = web.input(tx='800e6',rx='700e6')
		print i
		ad = AD9361_c.AD9361_c() 
		if i.tx!='n':
			ad.Set_Tx_freq(25e6,float(i.tx))
		if i.rx!='n':
			ad.Set_Rx_freq(25e6,float(i.rx))
		ad.deinit()
		web.header('Content-Type', 'text/json')
		return json.dumps({'ret':'ok'})


if __name__ == "__main__":
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

	app = web.application(urls, globals())
	app.run()

