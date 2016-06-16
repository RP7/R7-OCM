from urllib import urlopen
import json

class curlwrapper:
	def __init__(self,url):
		self.url = url

	def set_rx_freq(self,f):
		r = urlopen(self.url+'rx?freq='+str(f)).read()
		return json.loads(r)

	def get_rx_freq(self):
		r = urlopen(self.url+'rx?freq').read()
		return json.loads(r)

	def set_afc(self,d):
		r = urlopen(self.url+'misc?fun=awreg&reg=18&value='+hex(d)).read()
		return json.loads(r)

def main():
	c = curlwrapper('http://192.168.1.110:8080/')
	print c.set_rx_freq(939.8e6)
	print c.set_afc(0x1f)

if __name__ == '__main__':
	main()
