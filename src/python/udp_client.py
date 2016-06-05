from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
import threading
from ctypes import *
import time
from udp_header import *
import json
import sys
import signal


class udp_client(socket):

	def __init__(self,ip,port):
		self.port = port
		self.ip = ip
		self.host = (ip,port)
		socket.__init__(self, AF_INET, SOCK_DGRAM)
		self.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
		self.connect(self.host)
		self.tx_en = 0
		self.rx_en = 0
		self.tx_stop = 0
		self.tx_stop = 0

		self.tx_thread = threading.Thread(target = self.tx, name = 'tx')
		self.rx_thread = threading.Thread(target = self.rx, name = 'rx')
	
		self.rx_cnt = 0
		self.tx_cnt = 0
		self.rx_time = 0
		self.rx_offset = 0
		self.tx_time = 0
		self.tx_offset = 0
		self.data = (c_uint*0x100)()
		memset(byref(self.data),0,0x400)
		

	def recv4rx(self):
		data = self.recv(sizeof(udp_package))
		if len(data)==sizeof(udp_package):
			return stream2struct(data,udp_package)
		if len(data)>=sizeof(udp_header):
			p = stream2struct(data[:sizeof(udp_header)],udp_header)
			if p.time==0xffffffffffffffff:
				print "host reset"
			
	def send4tx(self,t,o,p):
		s = udp_package()
		s.header.time   = t
		s.header.offset = o
		memmove(s.data,p,1024)
		cs = struct2stream(s)
		self.sendto(cs,self.host)
		return sizeof(s)

	def rx(self):
		while(True):
			if self.rx_en==0:
				time.sleep(0.001)
			else:
				package = self.recv4rx()
				self.rx_cnt += 1
				self.rx_time = package.header.time
				self.rx_offset = package.header.offset
			if self.rx_stop==1:
				break
	def now2chip(self):
		return long(time.time()*1.92e6)

	def tx(self):
		while(True):
			if self.tx_en==0:
				time.sleep(0.001)
			else:
				tx_time = self.now2chip()
				if tx_time>self.tx_time-0x100:
					self.tx_time += 0x100
					self.tx_offset += 0x100
					if self.tx_offset < self.rx_offset:
						self.tx_offset = self.rx_offset + 1920*4
					if self.tx_offset > self.rx_offset + 1920*400:
						self.tx_offset = self.rx_offset + 1920*4
					self.send4tx(tx_time,self.tx_offset,self.data)
					self.tx_cnt += 1
			if self.tx_stop==1:
				break

	def stop(self):
		self.rx_stop = 1
		self.tx_stop = 1
		time.sleep(0.1)
	
	def en(self):
		self.rx_stop = 0
		self.tx_stop = 0
		self.tx_en = 1
		self.rx_en = 1
		
	def exit(self):
		self.stop()
		self.close()


	def run(self):
		self.stop()
		self.en()
		self.tx_time = self.now2chip()
		self.tx_thread.start()
		self.rx_thread.start()

	def dump(self):
		s = [   "host"
					, "tx_en"
					, "tx_stop"
					, "rx_en"
					, "rx_stop"
					, "tx_time"
					, "tx_offset"
					, "rx_time"
					, "rx_offset"
					, "rx_cnt"
					, "tx_cnt"
					]
		r = {}
		for x in s:
			r[x] = self.__dict__[x]
		return r

def main():
	c = udp_client("192.168.1.110",10000)
	signal.signal(signal.SIGTERM,c.exit)
	c.run()
	cnt = 0
	while cnt<100:
		print json.dumps(c.dump(),indent=2)
		time.sleep(1)
		cnt += 1
		print "#%08d"%cnt
	c.exit()

if __name__ == '__main__':
	main()

