import os
import re

path = os.path.split(os.path.realpath(__file__))[0]
path = path+"/../rtl/reg_define.v"
addr = {}

reg_file = open(path)
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
			m = re.match(r"\s+8",line)
			if m:
				s = len(m.group(0))
				a = int(line[s+2:],16)
				addr[x]=a

