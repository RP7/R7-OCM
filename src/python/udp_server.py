from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
import threading
from ctypes import *
import time
import aximem
from udp_header import *

class udp_server(socket):

	def __init__(self,port):
		self.port = port
		self.myAddr = ("0.0.0.0",port)
		socket.__init__(self, AF_INET, SOCK_DGRAM)
		self.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
		self.bind(self.myAddr)
		self.peerAddr = None
		self.tx_en = 0
		self.rx_en = 0
		self.tx_stop = 0
		self.tx_stop = 0

		self.tx_thread = threading.Thread(target = self.tx, name = 'tx')
		self.rx_thread = threading.Thread(target = self.rx, name = 'rx')
	
		self.aximem = None

	def recv4tx(self):
		data,addr = self.recvfrom(sizeof(udp_package))
		if len(data)==sizeof(udp_package):
			self.peerAddr = addr
			return stream2struct(data,udp_package)
		if len(data)>sizeof(udp_header):
			p = stream2struct(data[:sizeof(udp_header)],udp_header)
			if p.time==0xffffffffffffffff:
				self.peerAddr = None
			
	def send4rx(self,t,o,p):
		if self.peerAddr==None:
			return
		s = udp_package()
		s.header.time = t
		s.header.offset = o
		memmove(s.data,p,1024)
		cs = struct2stream(s)
		self.sendto(cs,self.peerAddr)
		return sizeof(s)

	def tx(self):
		while(True):
			if self.tx_en==0:
				time.sleep(0.001)
			else:
				package = self.recv4tx()
				self.aximem.dma.out.data = pointer(package.data)
				self.aximem.put(package.offset,1024)
			if self.tx_stop==1:
				break

	def rx(self):
		while(True):
			if self.rx_en==0:
				time.sleep(0.001)
			else:
				start = self.aximem.dma.inp.end
				r = self.aximem.get(start,1024)
				if r<0:
					self.aximem.reset("inp")
				elif r==0:
					time.sleep(0.01)
				else:
					self.send4rx(self.aximem.dma.inp.time,start,self.aximem.dma.inp.data)
			if self.rx_stop==1:
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
		self.tx_thread.start()
		self.rx_thread.start()

	def dump(self):
		s = ["myAddr","peerAddr","tx_en","tx_stop","rx_en","rx_stop"]
		r = {}
		for x in s:
			r[x] = self.__dict__[x]
		return r

			


