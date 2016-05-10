import os
import re
import AD9361_c

def remove(line):
	if line=='\r\n' or line=='\n' or line[:2]=='//':
		return None
	lines = line.split('//')
	if len(lines)>1:
		return lines[0]
	line = line.strip('\r\n')
	line = line.strip('\n')
	return line
def parse(line,order=None):
	line = remove(line)
	if line!=None:
		lines = re.split('\b+|\t+|,',line)
		print lines
		if order:
			for o in order:
				if lines[0]==o:
					order[o](lines[1:])

def main():
	path = os.path.split(os.path.realpath(__file__))[0]
	fn = path+"/../../AD9361/ad9361_config.reg"
	f = open(fn)
	ad = AD9361_c.AD9361_c()
	for x in f.readlines():
		parse(x,ad.order)


if __name__ == '__main__':
	main()
