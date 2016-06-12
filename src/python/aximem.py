from ctypes import *
from c_lib import lib
from udp_header import *

class h_aximem(Structure):
	_fields_ = [  ("u_map", c_void_p)
							, ("c_map", c_void_p)
							]
class p_monitor(Structure):
	_fields_ = [  ("counter", c_uint*16) ]
	def dump(self,msg):
		r = {}
		for k in range(len(msg)):
			r[msg[k]] = self.counter[k]
		return r

class e_aximem(Structure):
	_fields_ = [  ("base", c_uint)
							, ("size", c_uint)
							, ("acnt", c_uint)
							, ("bcnt", c_uint)
							, ("time", c_ulonglong)
							, ("start", c_ulonglong)
							, ("end", c_ulonglong)
							, ("length", c_uint)
							, ("pm", p_monitor)
							, ("data", c_void_p)
							]

	def dump(self,msg):
		return {  "base": hex(self.base)
						, "size": hex(self.size)
						, "acnt": hex(self.acnt)
						, "bcnt": hex(self.bcnt)
						, "time": hex(self.time)
						, "start": hex(self.start)
						, "end": hex(self.end)
						, "length": hex(self.length)
						, "preformance_monitor_s":self.pm.dump(msg)
					}
class e_socket_info(Structure):
	_fields_ = [  ("sid", c_uint)
							, ("port", c_uint)
							, ("send_en", c_uint)
							, ("recv_en", c_uint)
							, ("servAddrLen", c_uint)
							, ("peerAddrLen", c_uint)
							, ("addr", c_char*64)
							]
	def dump(self):
		d = self.addr[:2*self.servAddrLen]
		return {
			  "sid":self.sid
			, "port":self.port
			, "send_en":self.send_en
			, "recv_en":self.recv_en
			, "servAddrLen":self.servAddrLen
			, "peerAddrLen":self.peerAddrLen
			, "addr":d[:]
		}

class axi_dma(Structure):
	_fields_ = [  ("inp", e_aximem)
							, ("out", e_aximem)
							, ("sock", e_socket_info)
						]

	def dump(self):
		inp_pm_msg = [
			  "inp_ok"
			, "not_peer"
			, "data_no_ready"
			, "data_out_of_date"
			, "send_failure"
		]

		out_pm_msg = [
			  "out_ok"
			, "buf_full"
			, "addr_err"
			, "data_out_of_date"
			, "recv_failure"
			, "aligned_err"
		]
		return {  "inp":self.inp.dump(inp_pm_msg)
						, "out":self.out.dump(out_pm_msg)
						, "sock":self.sock.dump()
						}

class aximem:
	def __init__(self,config=None):
		self.handle = h_aximem()

		self.dma = axi_dma()
		self.dma.sock.port = 10000
		if config==None:
			self.dma.inp.base = 0
			self.dma.inp.size = 0x100000
			self.dma.out.base = 0x1f00000
			self.dma.out.size = 0x100000
		else:
			self.init(config)
		self.errcnt = {}
		for i in range(0,-7,-1):
			self.errcnt[i] = 0
		self.inp_package = udp_package()
		self.out_package = udp_package()

		
	def init(self,config):
		self.base = lib.axi_base()
		self.dma.inp.base = config['AXI2S_IBASE']-self.base
		self.dma.inp.size = config['AXI2S_ISIZE']
		self.dma.out.base = config['AXI2S_OBASE']-self.base
		self.dma.out.size = config['AXI2S_OSIZE']
		if 'port' in config:
			self.dma.sock.port = config['port']
		self.dma.inp.length = 1024
		self.dma.out.length = 1024
		lib.axi_init(byref(self.handle))
		lib.axi_open(byref(self.dma))

	def dump(self):
		reg = c_uint*32
		reg_p = cast(self.handle.c_map, POINTER(reg))
		i = 0
		for x in reg_p.contents[:]:
			print "%04x:0x%08x"%(i,x)
			i += 4

	def get(self,s,l):
		self.dma.inp.start = s
		self.dma.inp.length = l
		r = lib.axi_get(byref(self.dma))
		if r==l:
			self.dma.inp.end = long(s)+l
			return r
		else:
			err = {    0:"data not ready"
							, -1:"data out of date"}
			if r in err:
				self.errcnt[r] += 1
			else:
				print "unknow reason"
			return None

	def put(self,s,l):
		self.dma.out.start = s
		self.dma.out.length = l
		r = lib.axi_put(byref(self.dma))
		if r==l:
			self.dma.out.end = long(s)+l
		else:
			err = {    0:"buffer full"
							, -1:"buffer overrun"
							, -2:"data unaligned"
							}
			if r in err:
				self.errcnt[r-2] += 1
			else:
				print "unknow reason"

	def reset(self,who):
		if who=="inp":
			lib.axi_inp_reset(byref(self.dma))
			
	def udp_inp(self):
		r = lib.axi_inp_task(byref(self.dma),byref(self.inp_package))
		return r

	def udp_out(self):
		r = lib.axi_out_task(byref(self.dma),byref(self.out_package))
		return r

	def close(self):
		lib.axi_close(byref(self.dma))

	def peer(self):
		lib.axi_reportPeerIP(byref(self.dma))

def main():
	a = aximem()
	a.dump()

if __name__ == '__main__':
	main()