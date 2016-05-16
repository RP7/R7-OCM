import os
import ctypes

path = os.path.split(os.path.realpath(__file__))[0]
fn = path+"/../../lib/q7.so"

lib = ctypes.CDLL(fn)

def init():
	lib.ad9361_init()

def deinit():
	lib.ad9361_deinit()

def main():
	init()
	deinit()
	
if __name__ == '__main__':
	main()
