import time
import numpy as np
import config
import GSM as gsm
import FCCH
import SCH
import BCCH
import CCCH
import SDCCH
import FACCH
import TS
import Burst
import SB
import NB
import GSMShareData
import threading

class SyncState:
	__Message__ = ["init","rough","fine","keep"]
	MAXSTATE = 1024
	
	def __init__(self):
		self.state = 0
		self.cnt = [0]*len(SyncState.__Message__)
	
	def dump(self):
		return SyncState.__Message__[self.state]
	
	def to(self,s):
		FindMsg = { SyncState.__Message__[i]:i for i in range(len(SyncState.__Message__)) }
		if s in FindMsg:
			self.state = FindMsg[s]
			self.cnt[self.state]=0
	
	def name(self):
		return SyncState.__Message__[self.state]
	
	def once(self):
		if self.cnt[self.state]<SyncState.MAXSTATE: 
			self.cnt[self.state]+=1
	def count(self,s):
		FindMsg = { SyncState.__Message__[i]:i for i in range(len(SyncState.__Message__)) }
		return self.cnt[FindMsg[s]]
class GSMSystemState:
	def __init__(self):
		self.freqSyncState = SyncState()
		self.timingSyncState = SyncState()
		self.bcc = 0
		self.bcch_log = None
		self.bcc = 0
		self.ncc = 0
		self.t1  = 0
		self.t2  = 0
		self.t3  = 0
		self.diff_fn = 0

class GSMC0:

	def __init__(self):
		self.C0 = TS.CFrame()
		self.fcch = FCCH.FCCH()
		self.C0.build(gsm.MultiFrame)
		self.fcch.attach(self.C0)
		self.rx = None
		self.tx = None
		self._fn = long(0)
		self.mfl = config.SampleRate*gsm.T_MultiFrame
		self.fl = config.SampleRate*gsm.T_Frame
		self.multiFrameCallBacks = {}
		self.MCB_mutex = threading.Lock()
		self.FS_mutex = threading.Lock()
		self.sleepTime = 0.
		self.state = GSMSystemState()
		self.osr = config.SampleRate/gsm.SymbolRate
		self.ccch = []
		self.sdcch = []
		self.bcch = []
		self.facch = []

	def initSCH(self):
		self.sch = SCH.SCH()
		self.sch.attach(self.C0)
		self.regMCB(self.frameTrack,None)
	
	def initBCCH(self):
		for i in [0]:
			ch = BCCH.BCCH(i)
			ch.attach(self.C0,gsm.MultiFrameC)
			self.bcch.append(ch)

	def initCCCH(self,r):
		for i in [0,2]:
			for n in r:
				ch = CCCH.CCCH(n,i)
				ch.attach(self.C0,gsm.MultiFrameC)
				self.ccch.append(ch)

	def initSDCCH(self,r,slots):
		for s in slots:
			for n in r:
				ch = SDCCH.SDCCH(n,s)
				ch.attach(self.C0,gsm.MultiFrameC)
				self.sdcch.append(ch)

	def initFACCH(self,r):
		for n in r:
			ch = FACCH.FACCH(n)
			ch.attach(self.C0,gsm.MultiFrameT)
			self.facch.append(ch)

	def getFn(self):
		_s = self._fn/gsm.SupperFrame
		_a = self._fn%gsm.SupperFrame
		_N = _a/gsm.MultiFrame
		_F = _a%gsm.MultiFrame
		return _s,_N,_F

	def setRx(self,rx):
		self.rx = rx
		self.data = self.rx.appData(GSMShareData.GSMAppData)
		Burst.mmap = self.mmap

	def getFrameStart( self ):
		return long(self.data.frame_start_point)
	
	def setFrameStart( self, s ):
		if s<0:
			s += self.mfl
			if self._fn>gsm.MultiFrame:
				self._fn = long(self._fn-gsm.MultiFrame)
			else:
				print "_fn wrony"
		self.data.frame_start_point = long(s)

	def mmap(self,s,l):
		_N = long(self._fn/gsm.MultiFrame)
		fs = long(self.getFrameStart()+self.mfl*_N+s*self.osr)
		ls = long(l*self.osr)
		return self.rx.mmap(ls*4,fs*4)

	def flash(self):
		now = self.rx.now()
		last = self.getFrameStart()
		_fn = long(now-last)/long(self.fl)
		if _fn < 0:
			if last+long(_fn*self.fl)>0:
				self.adjustFrameStart(long(_fn*self.fl))
				self._fn = 0
			else:
				print "can not reset",now,last,_fn,self.rx.now()
			print "reset for early again"
		else:
			self._fn = _fn

	def oneFrame(self):
		_s,_N,_F = self.getFn()
		if _F == 0:
			self.multiFrameCallBack(_s,_N)
		self._fn += 1
		if self.wait()==0:
			return
		f = self.C0.frame[_F]
		for b in f:
			if b.ch!=None:
				b.mapRfData()
				ok,data = b.ch.callback(b,_F,self.state)
			if self.state.timingSyncState.name()=="fine" and self.state.timingSyncState.count("fine")>3:
				b.default_callback(_F,self.state)
	
	def wait(self):
		w = self.getFrameStart()+long(self._fn*self.fl)
		if w<long(self.rx.now()-config.SampleRate*2):
			self.flash()
			print "Reset(Late)"
			return 0
		while self.rx.now()<w:
			self.sleepTime+=0.01
			time.sleep(0.01)		
			if w>long(self.rx.now()+config.SampleRate*10):
				print " maybe rf reset"
				self.reset()
				return 0
		return 1
		

	def multiFrameCallBack(self,s,N):
		for f in self.multiFrameCallBacks:
			f(s,N,self.multiFrameCallBacks[f])

	def regMCB(self,f,args):
		self.multiFrameCallBacks[f]=args

	def deregMCB(self,f):
		if f in self.multiFrameCallBacks:
			del self.multiFrameCallBacks[f]

	def frameTrack(self,s,N,a):
		if self.state.timingSyncState.name()!="fine":
			print "hit:",self.sch.hit
		fsnew,r = self.sch.frameStart()

		print "Sleep",self.sleepTime,"fs new",fsnew,"r",r,
		
		if r<130*0.7:
			if self.state.timingSyncState.name()=="fine":
				self.state.timingSyncState.to("rough")
			if self.state.timingSyncState.count("rough")>2:
				self.state.timingSyncState.to("init")
				self.state.freqSyncState.to("init")
		else:
			if self.state.timingSyncState.name()=="rough":
				self.state.timingSyncState.to("fine")
			self.adjustFrameStart( fsnew )

		self.sleepTime = 0.
		self.state.timingSyncState.once()
		print "state:",self.state.timingSyncState.name()
	def run(self,MAXC):
		self.reset()
		cnt = 0
		while cnt<MAXC or MAXC==-1:
			if self.state.freqSyncState.name()=="init":
				ok,data = self.findFCCH()
				if ok==1:
					self.state.timingSyncState.to("rough")
					self.state.freqSyncState.to("rough")
				self.flash()
			else:
				self.oneFrame()
			cnt += 1
		return data

	def findFCCH(self):
		_s,_N,_f = self.getFn()
		d = (_f/51-2)*51
		fl = long(self.fl*53/self.osr)
		print "frame@",d
		start = long(d*gsm.S_Frame)
		rawmf = self.mmap(start,fl)
		data = self.fcch.find(rawmf,float(self.osr))
		ok = self.searchFrameStart(data)
		
		return ok,data

	def searchFrameStart(self,nc):
		p = nc.argmin()
		minnc = nc[p]
		print "find",p,minnc

		mpd = int(p/(gsm.S_Frame*self.osr))
		mp = p-mpd*gsm.S_Frame*self.osr
		
		pnc = nc[np.arange(mp,len(nc),float(gsm.S_Frame*self.osr)).astype(int)]
		pattern = [0,10,20,30,40]

		fsfn = self.patternSumSearch(pnc,pattern,51)
		ok = 1
		for pp in pattern:
			h = pnc[(fsfn+pp)%51]
			if h>minnc*0.7:
				ok=0
			print "%7d"%h,
		print "fn",fsfn,""
		if ok==1:
			if fsfn>26:
				fsfn -= 51
			fs = int(fsfn*float(gsm.S_Frame*self.osr)+mp)#-gsm.S_Slot*self.osr
			print "fs@",fsfn,fs
			self.adjustFrameStart(fs)
		return ok

	def patternSumSearch(self,d,p,m):
		r = np.zeros(m,dtype=int)
		for i in range(len(r)):
			for pp in p:
				r[i] += d[(i+pp)%m]
		inx = r.argmin()
		return inx 
	def adjustFrameStart(self,n):
		last = self.getFrameStart()
		self.setFrameStart(last+n)

	def reset(self):
		self.state.timingSyncState.to("init")
		self.state.freqSyncState.to("init")
		self.waitClockStable()
		if self.rx.now()>self.mfl:
			self.setFrameStart(long(self.mfl))
		else:
			self.setFrameStart(long(0))
		self.flash()
	
	def waitClockStable( self ):
		while self.rx.clkRate()<4:
			print "clock not stable",self.rx.clkRate()
			time.sleep(2)	
