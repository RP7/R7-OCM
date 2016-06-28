from ctypes import *
from socket import socket,AF_INET,SOCK_DGRAM

class gsmtap_hdr(Structure):
	_pack_ = 1
	_fields_ = [   ("version", c_int8)
		, ("hdr_len", c_int8)
		, ("type", c_int8)
		, ("timeslot", c_int8)
		, ("arfcn", c_int16)
		, ("signal_dbm", c_int8)
		, ("snr_db", c_int8)
		, ("frame_number", c_int32)
		, ("sub_type", c_int8)
		, ("antenna_nr", c_int8)
		, ("sub_slot", c_int8)
		, ("res", c_int8)
	]

class gsmtap_data(Structure):
	_pack_ = 1
	_fields_ = [   ("header", gsmtap_hdr)
		, ("data",c_int8*23)
	]

class gsmtap:
	def __init__(self):
		self.block = gsmtap_data()

		self.block.header.version = 1
		self.block.header.hdr_len = 4
		self.block.header.type = 1
		self.block.header.signal_dbm = -40
		self.block.header.sub_type = 1
		self.sock = socket(AF_INET, SOCK_DGRAM)

	def send(self,data):
		self.block.data[:]=data[:]
		self.sock.sendto(self.struct2stream(self.block),('127.0.0.1',4729))

	def struct2stream(self,s):
		length  = sizeof(s)
		p       = cast(pointer(s), POINTER(c_char * length))
		return p.contents.raw
