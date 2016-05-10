import os
import re



def loadFromVerilog(fn,addr):
	reg_file = open(fn)
	for line in reg_file.readlines():
		m = re.match(r"`define(\s+)",line)
		if m:
			x = m.group(0)
			s = len(x)
			line = line[s:]
			m = re.match(r"(\S+)",line)
			if m:
				x = m.group(0)
				s = len(x)
				line = line[s:]
				#print x,line
				m = re.match(r"\s+18",line)
				if m:
					s = len(m.group(0))
					a = int(line[s+2:],16)
					addr[x]=a
	return addr

def loadFromC(fn,addr):
	reg_file = open(fn)
	for line in reg_file.readlines():
		m = re.match(r"#define(\s+)",line)
		if m:
			x = m.group(0)
			s = len(x)
			line = line[s:]
			m = re.match(r"(\S+)",line)
			if m:
				x = m.group(0)
				s = len(x)
				line = line[s:]
				#print x,line
				m = re.match(r"\s+0x",line)
				if m:
					s = len(m.group(0))
					a = int(line[s:s+8],16)
					addr[x]=a
	return addr


addr = {}
path = os.path.split(os.path.realpath(__file__))[0]
fn = path+"/../rtl/reg_define.v"

addr = loadFromVerilog(fn,addr)

fn = path+"/../c/ad9361_spi.h"
addr = loadFromC(fn,addr)

#print addr
