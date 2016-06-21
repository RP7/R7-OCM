import GSMRoughSync
import time
import Q7Mem
import gsmlib.config as config
import gsmlib.GSM as gsm
import gsmlib.FCCH
import gsmlib.SCH
import gsmlib.TS
import matplotlib.pyplot as plt
import numpy as np
import gsmlib.Burst as Burst
import gsmlib.SB as SB
import gsmlib.NB as NB

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
	#print "fs,ls,s,l",fs,ls,s,l
	return sync.rx.mmap(ls*4,fs*4)

def flash():
	now = sync.rx.now()
	last = sync.getFrameStart()
	if last>now:
		last = now
		print "resync:"
		return None
	mfs = (now-last)/sync.sfl
	newStart = (mfs+1)*sync.sfl+last
	sync.setFrameStart(newStart)

def mflash():
	now = sync.rx.now()
	last = sync.getFrameStart()
	if last>now:
		last = now
		print "resync:"
		return None
	fl = 1920*120*51/26.
	mfs = long((now-last)/fl)
	newStart = long(mfs*fl+last)
	sync.setFrameStart(newStart)
	while(sync.rx.now()<newStart+fl):
		time.sleep(0.01)

gsmlib.Burst.mmap = mmap

# f0 = sync.sync()
# f1 = 0.
# while abs(f1-f0)>1e3:
# 	f1 = f0
# 	f0 = sync.sync()
# 	print "rough sync:",f0
# 	time.sleep(1)

mflash()
now = sync.rx.now()
for i in range(51*26):
	f = C0.frame[i]
	for b in f:
		if b.ch!=None:
			b.mapRfData()
			ok,data = b.ch.callback(b,i)
			if ok:
				if b.__class__.__name__=="FB":
					plt.plot(data)

	while(sync.rx.now()<now+i*sync.fl):
	 	time.sleep(0.01)
	 	print "x",
last = sync.getFrameStart()
print sch.hit
fsnew = sch.frameStart()
sync.setFrameStart(last+fsnew)

print "new fs",fsnew


def show0(i):
	mflash()
	b = C0.frame[i]
	r = mmap(long(b[0].pos),12500)
	d = Burst.Burst.short2Complex(r)
	l = len(d)/10
	plt.figure(1)
	for i in range(10):
		sd = d[i*l:i*l+l]
		plt.subplot(5,2,i+1)
		plt.plot(np.angle(sd))
	plt.show()

def show1(i,j):
	mflash()
	b = C0.frame[i]
	r = mmap(b[0].pos,12500)
	d = Burst.Burst.short2Complex(r)
	l = len(d)/10
	osr = float(config.SampleRate/gsm.SymbolRate)
	if j<=6:
		t = NB.NBTraining.modulated[j,:]
	else:
		t = SB.SBTraining.modulated
	print "len t",len(t)
	print "osr",osr
	plt.figure(1)
	for i in range(10):
		sd = d[i*l:i*l+l]
		p = b[0].channelEst(sd,t,osr)
		plt.subplot(5,2,i+1)
		plt.plot(np.abs(p))
	plt.show()

def show2(i,j,k,m):
	slots = 12
	ret = []
	mflash()
	b = C0.frame[i]
	r = mmap(b[0].pos-1250*11,1250*slots)
	d = Burst.Burst.short2Complex(r)
	pos = findSlot(d)
	l = len(d)/slots
	pos %= l
	pos %= (l/8)
	pos += k*l/8
	print pos
	plt.figure(1)
	plt.grid("on")
	for i in range(slots):
		sd = d[i*l+pos+60:i*l+l/8*m+pos]
		ret.append(sd)
		a = np.angle(sd[1:]/sd[:-1])
		plt.subplot(slots/2,2,i+1)
		if j==0:
			plt.plot(a)
			dec(a)
		else:
			t = SB.SBTraining.unmodulated
			osr = float(config.SampleRate/gsm.SymbolRate)
			plt.plot(np.abs(b[0].channelEst(a,t,osr)))
	plt.show()
	return ret

def findSlot(a):
	r = np.abs(a)
	osr = float(config.SampleRate/gsm.SymbolRate)
	gap = int(8.25*osr+0.5)
	p = np.zeros(len(r)-gap)
	for k in range(len(p)):
		p[k] = sum(r[k:k+gap])
	return p.argmin()

def dec(a):
	k = []
	r = ""
	g = []
	for i in range(len(a)-1):
		if a[i]*a[i+1]<0:
			k.append(i)
	for i in range(len(k)-1):
		l = k[i+1]-k[i]
		s = (l+3)/7
		if a[k[i]]>0:
			g += [-1]*s
		else:
			g += [1]*s
	ss = -1
	for i in range(len(g)):
		ss *= g[i]
		if ss==1:
			r += "1"
		else:
			r += "0"
	print r[:62],r[62:62+26],r[62+26:62*2+26],r[62*2+26:],len(r)

def adjust(n):
	last = sync.getFrameStart()
	sync.setFrameStart(last+n)

