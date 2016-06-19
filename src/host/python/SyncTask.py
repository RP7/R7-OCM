import GSMRoughSync
import time
import Q7Mem
import gsmlib.config as config
import gsmlib.GSM as gsm
import gsmlib.FCCH
import gsmlib.SCH
import gsmlib.TS

sync = GSMRoughSync.GSMRoughSync(939.8e6,'http://192.168.1.110:8080/')
fcch = gsmlib.FCCH.FCCH()
sch = gsmlib.SCH.SCH()
C0 = gsmlib.TS.CFrame()


C0.build(51*26)
sch.attach(C0)
fcch.attach(C0)

def mmap(s,l):
	fs = long(sync.getFrameStart()+s*config.SampleRate/gsm.SymbolRate)
	ls = long(l*config.SampleRate/gsm.SymbolRate)
	return sync.rx.mmap(ls*4,fs*4)

gsmlib.Burst.mmap = mmap

f0 = sync.sync()
f1 = 0.
while abs(f1-f0)>1e3:
	f1 = f0
	f0 = sync.sync()
	print "rough sync:",f0
	time.sleep(1)

now = sync.rx.now()
for i in range(len(C0.frame)):
	f = C0.frame[i]
	for b in f:
		if b.ch!=None:
			b.mapRfData()
			b.ch.callback(b,i)
	while(sync.rx.now()<now+i*sync.fl):
		time.sleep(0.01)
		