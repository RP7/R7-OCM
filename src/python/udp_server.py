from socket import socket, AF_INET, SOCK_DGRAM
import threading
from ctypes import *
import time
import aximem

class udp_header(Structure):
	_field_ =  [  ("time", c_ulonglong)
							, ("offset", c_ulonglong)
						]

class udp_package(Structure):
	_field_ =  [  ("header", udp_header)
							, ("data", c_char*1024)
						]
						
class udp_server(socket):

	def __init__(self,port):
		self.port = port
		self.myAddr = ("0.0.0.0",port)
		socket.__init__(self, AF_INET, SOCK_DGRAM)
		self.bind(self.myAddr)
		self.peerAddr = None
		self.tx_en = 0
		self.rx_en = 0
		self.tx_stop = 0
		self.tx_stop = 0

		self.tx_thread = threading.Thread(target = self.tx, name = 'tx')
		self.rx_thread = threading.Thread(target = self.rx, name = 'rx')
	
		self.aximem = None

	def struct2stream(self,s):
		length  = sizeof(s)
		p       = cast(pointer(s), POINTER(c_char * length))
		return p.contents.raw

	def stream2struct(self, string, stype):
		if not issubclass(stype, Structure):
			raise ValueError('The type of the struct is not a ctypes.Structure')
		length      = sizeof(stype)
		stream      = (c_char * length)()
		stream.raw  = string
		p           = cast(stream, POINTER(stype))
		return p.contents

	def recv4tx(self):
		data,addr = self.recvfrom(sizeof(udp_package))
		if len(data)==sizeof(udp_package):
			self.peerAddr = addr
			return self.stream2struct(data,udp_package)
		if len(data)>sizeof(udp_header):
			p = self.stream2struct(data[:sizeof(udp_header)],udp_header)
			if p.time==0xffffffffffffffff:
				self.peerAddr = None
			
	def send4rx(self,t,o,p):
		if self.peerAddr==None:
			return
		s = udp_package()
		s.header.time = t
		s.header.offset = o
		memcpy(s.data,p,1024)
		cs = self.struct2stream(s)
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
				start = self.aximem.last_inp_end
				r = self.aximem.get(start,1024)
				if r<0:
					self.aximem.reset("inp")
				elif r==0:
					time.sleep(0.01)
				else:
					self.send4rx(self.aximem.inp.time,start,self.aximem.inp.data)
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

			


