from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
import threading
from ctypes import *
import time
from udp_header import *
import json

class udp_host:

	def __init__(self,ip,port):
		self.sock = socket(AF_INET, SOCK_DGRAM)
		self.sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
		#self.sock.settimeout(0.001)
		#self.sock.setblocking(1)
		self.port = port
		self.ip = ip
		
		self.q7 = (ip,port)
		self.sock.connect(self.q7)

		self.tx_en = 0
		self.rx_en = 0
		self.tx_s = 0
		self.rx_s = 0

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
		
		self.length = 1920000
		self.host = None
		
	def recv4rx(self):
		data,self.host = self.sock.recvfrom(sizeof(udp_package))
		if len(data)==sizeof(udp_package):
			return stream2struct(data,udp_package)
		if len(data)>=sizeof(udp_header):
			p = stream2struct(data[:sizeof(udp_header)],udp_header)
			if p.time==0xffffffffffffffff:
				print "host reset"
			return None
			
	def send4tx(self,t,o,p):
		s = udp_package()
		s.header.time   = t
		s.header.offset = o
		memmove(s.data,p,1024)
		cs = struct2stream(s)
		return self.sock.sendto(cs,self.q7)
		
	def rx(self):
		package = self.recv4rx()
		if None!=package:
			self.rx_cnt += 1
			self.rx_time = package.header.time
			self.rx_offset = package.header.offset
			buf = '\0'*1024
			memmove(buf,byref(package,16),1024)
			slef.frd.write(buf)  
			self.cnt+=256
			
	def now2chip(self):
		return long(time.time()*1.92e6)

	def tx(self):
		tx_time = self.now2chip()
		#if self.tx_offset < self.rx_offset:
		#	self.tx_offset = self.rx_offset + 1920*4
		#if self.tx_offset > self.rx_offset + 1920*400:
		#	self.tx_offset = self.rx_offset + 1920*4
		if tx_time>self.tx_time-0x100:
			r = self.send4tx(tx_time,self.tx_offset,self.data)
			if r:
				self.tx_time += 0x100
				self.tx_offset += 0x100
				if (self.tx_cnt%10)==0:
					print json.dumps(self.dump(),indent=2)
				self.tx_cnt += 1
				
	def run(self):
		self.frd = open('../../temp/rd.dat','wb')
		self.cnt = 0
		self.tx_time = self.now2chip()-0x1000
		self.tx()
		while self.cnt<self.length:
			self.rx()
			if (self.cnt&0xfff)==0:
				print self.host
		self.frd.close()
			
	def dump(self):
		s = [   "q7"
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
	c = udp_host("192.168.1.110",10000)
	c.run()
	
	
if __name__ == '__main__':
	main()

