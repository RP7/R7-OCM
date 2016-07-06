from ctypes import *
from socket import socket,AF_INET,SOCK_DGRAM,htonl
import numpy as np
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
	"""
	#define GSMTAP_CHANNEL_UNKNOWN	0x00
	#define GSMTAP_CHANNEL_BCCH	0x01
	#define GSMTAP_CHANNEL_CCCH	0x02
	#define GSMTAP_CHANNEL_RACH	0x03
	#define GSMTAP_CHANNEL_AGCH	0x04
	#define GSMTAP_CHANNEL_PCH	0x05
	#define GSMTAP_CHANNEL_SDCCH	0x06
	#define GSMTAP_CHANNEL_SDCCH4	0x07
	#define GSMTAP_CHANNEL_SDCCH8	0x08
	#define GSMTAP_CHANNEL_TCH_F	0x09
	#define GSMTAP_CHANNEL_TCH_H	0x0a
	#define GSMTAP_CHANNEL_ACCH	0x80
	"""
	_channel_ = ["UNKNOW","BCCH","CCCH","RACH","AGCH","PCH","SDCCH","SDCCH4","SDCCH8","TCH_F","TCH_H"]
	def __init__(self):
		self.block = gsmtap_data()

		self.block.header.version = 1
		self.block.header.hdr_len = 4
		self.block.header.type = 1
		self.block.header.signal_dbm = -40
		self.block.header.sub_type = 1
		self.sock = socket(AF_INET, SOCK_DGRAM)

	def send(self,ch,fn):
		memmove(self.block.data,ch.data,23)
		self.block.header.sub_type = self.name2inx(ch.name)
		(r,s) = ch.config
		self.block.header.timeslot = s
		if ch.name=="TCH_F":
			self.block.header.signal_dbm = c_int8(int(ch.chp))
		self.block.header.frame_number = htonl(fn)
		self.sock.sendto(self.struct2stream(self.block),('127.0.0.1',4729))

	def struct2stream(self,s):
		length  = sizeof(s)
		p       = cast(pointer(s), POINTER(c_char * length))
		return p.contents.raw
	def name2inx(self,name):
		for i in range(len(gsmtap._channel_)):
			if gsmtap._channel_[i]==name:
				return i
		return 0
