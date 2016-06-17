import GSMRoughSync
import GSMFineSync
import time

while 1:
	GSMRoughSync.main()
	time.sleep(1)
	for i in range(10):
		GSMFineSync.main()
		time.sleep(10)
