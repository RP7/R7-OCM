import threading
import time
import os

class downloadThread(threading.Thread):
	def __init__(self,name,bit):
		threading.Thread.__init__(self,name=name)
		self.bitfn = bit
	
	def run(self):
		time.sleep(1)
		os.system('cat %s > /dev/xdevcfg'%self.bitfn)
		print "download OK"
