import web
import os
import axi2s_u

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
	app = web.application(urls, globals())
	app.run()

