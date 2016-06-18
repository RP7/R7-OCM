import GSMRoughSync
import GSMFineSync
import GSMTimingSync
import time

while 1:
	GSMRoughSync.main()
	time.sleep(1)
	for i in range(10):
		GSMFineSync.main()
		time.sleep(7)
		r = GSMTimingSync.main()
		if r<0:
			print "reset",r
			GSMRoughSync.main()
		time.sleep(7)
		
