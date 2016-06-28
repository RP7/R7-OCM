from ctypes import *
from socket import socket,AF_INET,SOCK_DGRAM

class gsmtap_hdr(Structure):
	__pack__ = 1
	__fields__ = [   ("version", c_int8)
		, ("hdr_len", c_int8)
		, ("type", c_int8)
		, ("timeslot", c_int8)
		, ("arfcn", c_int16)
		, ("signal_dbm", c_int8)
		, ("frame_number", c_int32)
		, ("sub_type", c_int8)
		, ("sub_slot", c_int8)
		, ("res", c_int8)
	]

class gsmtap_data(Structure):
	__pack__ = 1
	__fields__ = [   ("hdr", gsmtap_hdr)
		, ("data",c_int8*23)
	]

class gsmtap:
	def __init__(self):
		self.package = gsmtap_data()
		
		self.package.hdr.version = 1
		self.package.hdr.hdr_len = 23
		self.package.hdr.type = 1
		self.package.hdr.signal_dbm = -40
		self.package.hdr.sub_type = 1
		self.sock = socket(AF_INET, SOCK_DGRAM)

	def send(self,data):
		self.package.data[:]=data[:]
		self.sock.sendto(('127.0.0.1',4729),self.struct2stream(self.package))

	def struct2stream(self,s):
		length  = sizeof(s)
		p       = cast(pointer(s), POINTER(c_char * length))
		return p.contents.raw

