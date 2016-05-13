import web
import os
import axi2s_u
import AD9361_c
import adscripts
import axi2s_c

urls = ('/','index','/data','data')
class index:
	def GET(self):
		web.redirect('static/index.html')
class data:
	def GET(self):
		ocm = axi2s_u.axi2s_u()
		r = ocm.idata()
		return r

if __name__ == "__main__":
	path = os.path.split(os.path.realpath(__file__))[0]
	fn = path+"/../../AD9361/ad9361_config.reg"
	f = open(fn)
	ad = AD9361_c.AD9361_c()
	for x in f.readlines():
		adscripts.parse(x,ad.order)
	uut = axi2s_c.axi2s_c()
	uut.init()
	uut.write('AD9361_EN',1)
	uut.check()

	app = web.application(urls, globals())
	app.run()

