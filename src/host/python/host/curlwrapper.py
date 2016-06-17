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
		hd = d>>2
		ld = d&3
		r = urlopen(self.url+'misc?fun=arreg&reg=1a').read()
		r1a = json.loads(r)
		old = int(r1a["data"][:-1],16)
		ld |= old&0xfc
		r = urlopen(self.url+'misc?fun=awreg&reg=1a&value='+hex(ld)).read()
		r = urlopen(self.url+'misc?fun=awreg&reg=18&value='+hex(hd)).read()
		return json.loads(r)

def main():
	c = curlwrapper('http://192.168.1.110:8080/')
	print c.set_rx_freq(939.8e6)
	print c.set_afc(0x7c)

if __name__ == '__main__':
	main()
