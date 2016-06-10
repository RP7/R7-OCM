from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
import threading
from ctypes import *
import time
import aximem
from udp_header import *
			
class udp_server:

	def __init__(self):
		self.tx_en = 0
		self.rx_en = 0
		self.tx_stop = 0
		self.tx_stop = 0

		self.tx_thread = threading.Thread(target = self.tx, name = 'tx')
		self.rx_thread = threading.Thread(target = self.rx, name = 'rx')
	
		self.aximem = None

	def tx(self):
		self.aximem.dma.sock.recv_en = 1
		while(True):
			if self.tx_en==0:
				time.sleep(0.001)
			else:
				r = self.aximem.udp_out()
			if self.tx_stop==1:
				break

	def rx(self):
		self.aximem.dma.sock.send_en = 1
		while(True):
			if self.rx_en==0:
				time.sleep(0.001)
			else:
				r = self.aximem.udp_inp()
			if self.rx_stop==1:
				break

	def stop(self):
		self.aximem.dma.sock.recv_en = 0
		self.aximem.dma.sock.send_en = 0
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
		self.aximem.close()

	def run(self):
		self.stop()
		self.en()
		self.tx_thread.start()
		self.rx_thread.start()

	def dump(self):
		s = ["tx_en","tx_stop","rx_en","rx_stop"]
		r = {}
		for x in s:
			r[x] = self.__dict__[x]
		return r

