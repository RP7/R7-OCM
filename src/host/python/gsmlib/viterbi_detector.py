import numpy as np

class viterbi_detector:
	def __init__(self,K,L,training):
		self.SN = 1<<(K-1)
		self.K = K
		self.L = L
		self.Fmetrics  = np.zeros((self.SN,L+1))
		self.Bmetrics  = np.zeros((self.SN,L+1))
		self.tracback = np.zeros((self.SN,L),dtype=int)
		self.f_r_i = (len(training)-self.K+1)%2
		self.b_r_i = 1
	
	def setTraining(self,training,f_r_i,b_r_i):
		self.startFS = self.toState(training[-(self.K-1):],f_r_i)
		self.startBS = self.toState(training[:(self.K-1)],b_r_i) 

		
	def toState(self,t,r_i):
		"""
		1  -> 1
		-1 -> 0
		"""
		s = 0
		for x in t:
			s *= 2
			if r_i == 1:
				if x.real>0:
					s+=1
			else:
				if x.imag>0:
					s+=1
			r_i = 1 -r_i
		return s

	def s2s(self,s,r_i):
		"""
		inverse order
		rf = 1
		if = 0
		"""
		ret = np.zeros(self.K,dtype=complex)
		if r_i==1:
			inc = 1
		else:
			inc = 0
		for i in range(self.K):
			if (s&1)==1:
				ret[i] = 1.+0j
			else:
				ret[i] = -1.+0j
			s >>=1
			if (i+inc)%2 == 0:
				ret[i] *= 1.j
		return ret


	def table(self,r):
		self.t = np.zeros((2,self.SN*2),dtype=complex)
		for r_i in range(2):
			for s in range(self.SN*2):
				self.t[r_i][s]=np.dot(self.s2s(s,r_i),r)
		

	def mindiff(self,x,h):
		y = h-x
		yy = y*np.conj(y)
		return bin(yy.argmin())
	
	def metric(self,x,y):
		return -((x-y)*np.conj(x-y)).real

	def t2b(self,t,r_i):
		l = []
		for x in t:
			if r_i==0:
				v = x.imag
			else:
				v = x.real
			if v>0:
				l.append(1)
			else:
				l.append(0)
			r_i = 1 - r_i
		return l 

	def maxState(self,h):
		return h.argmax()    
	
	def forward(self,m):
		r_i = self.f_r_i
		for i in range(self.SN):
			self.Fmetrics[i,0]=-1e100
			self.Fmetrics[self.startFS,0]=0
		for i in range(self.L):
			for s in range(self.SN/2):
				m00 = self.Fmetrics[s,i]+self.metric(m[i],self.t[r_i,s*2])
				m08 = self.Fmetrics[s+self.SN/2,i]+self.metric(m[i],self.t[r_i,s*2+self.SN])
				if m00>m08:
					self.Fmetrics[s*2,i+1]=m00
					self.tracback[s*2,i]=0
				else:
					self.Fmetrics[s*2,i+1]=m08
					self.tracback[s*2,i]=1
				m10 = self.Fmetrics[s,i]+self.metric(m[i],self.t[r_i,s*2+1])
				m18 = self.Fmetrics[s+self.SN/2,i]+self.metric(m[i],self.t[r_i,s*2+self.SN+1])
				if m10>m18:
					self.Fmetrics[s*2+1,i+1]=m10
					self.tracback[s*2+1,i]=0
				else:
					self.Fmetrics[s*2+1,i+1]=m18
					self.tracback[s*2+1,i]=1
			r_i = 1 - r_i
		end = self.Fmetrics[:,self.L]
		ends = end.argmax()
		#ends = 0
		ret = []
		es = ends
		for i in range(self.K-1):
			ret.append(es&1)
			es >>= 1

		for i in range(self.L-1,-1,-1):
			b = self.tracback[ends,i]
			ret.append(b)
			ends /=2
			ends += b*self.SN/2

		return ret[::-1]

	def backward(self,m):
		r_i = self.b_r_i
		for i in range(self.SN):
			self.Bmetrics[i,self.L]=-1e100
			self.Bmetrics[self.startBS,self.L]=0
		for i in range(self.L-1,-1,-1):
			mm = m[i]
			for s in range(self.SN/2):
				m00 = self.Bmetrics[2*s,i+1]+self.metric(mm,self.t[r_i,2*s])
				m08 = self.Bmetrics[2*s+1,i+1]+self.metric(mm,self.t[r_i,s*2+1])
				if m00>m08:
					self.Bmetrics[s,i]=m00
					self.tracback[s,i]=0
					s0 = 2*s
				else:
					self.Bmetrics[s,i]=m08
					self.tracback[s,i]=1
					s0 = 2*s+1
				m10 = self.Bmetrics[2*s,i+1]+self.metric(mm,self.t[r_i,s*2+self.SN])
				m18 = self.Bmetrics[2*s+1,i+1]+self.metric(mm,self.t[r_i,s*2+self.SN+1])
				if m10>m18:
					self.Bmetrics[s+self.SN/2,i]=m10
					self.tracback[s+self.SN/2,i]=0
					s1 = 2*s+self.SN
				else:
					self.Bmetrics[s+self.SN/2,i]=m18
					self.tracback[s+self.SN/2,i]=1
					s1 = 2*s+self.SN+1
				#print (s>>1)&1,mm,s0,s1
				
			#print self.Bmetrics[:,i]
			r_i = 1 - r_i
		end = self.Bmetrics[:,0]
		ends = end.argmax()
		#ends = 0
		ret = []
		es = ends
		for i in range(self.K-1):
			ret.append((es>>(self.K-1-1))&1)
			es <<= 1

		for i in range(self.L):
			b = self.tracback[ends,i]
			ret.append(b)
			ends *=2
			ends += b
			ends &= (self.SN-1)

		return ret
	def dediff_forward(self,msg,r_i,s):
		r = []
		r_i = 1-r_i
		for i in range(len(msg)-1):
			r.append(msg[i]^msg[i+1]^r_i)
			r_i = 1-r_i
		d = s
		dr = [d]
		for x in r:
			d = d^x
			dr.append(d)
		return dr

	def dediff_backward(self,msg,r_i,e):
		r = []
		r_i = 1-r_i
		for i in range(len(msg)-1):
			r.append(msg[i]^msg[i+1]^r_i)
			r_i = 1-r_i
		d = e
		dr = [0]*len(msg)
		dr[-1]=e
		for k in range(len(r)-1,-1,-1):
			d = d^r[k]
			dr[k] = d
		return dr

	def outMsg(self,a):
		for x in a:
			print x,
		print ""

	def restore_forward(self,msg,starts,r_i):
		ret = np.zeros(len(msg),dtype=complex)
		i = 0
		for x in msg:
			starts *= 2
			starts += x
			ret[i]=self.t[r_i,starts]
			r_i = 1-r_i
			starts &= self.SN-1
			i+=1
		return ret
	def restore_backward(self,msg,starts,r_i):
		ret = np.zeros(len(msg),dtype=complex)
		i = len(msg)-1
		for x in msg[::-1]:
			starts /= 2
			starts += x*self.SN
			ret[i]=self.t[r_i,starts]
			r_i = 1-r_i
			i-=1
		return ret

	def _forward(self,t,m,start,r_i,l):
		(i,sn) = t.shape
		sn /= 2
		metrics = np.zeros((sn,l+1))
		tracback = np.zeros((sn,l),dtype=int)
		for i in range(sn):
			metrics[i,0]=-1e100
		metrics[start,0]=0
		for i in range(l):
			for s in range(sn/2):
				# shift in 0
				#print s,metrics[s,i],metrics[s+sn/2,i],m[i],t[r_i,s*2],t[r_i,s*2+sn],t[r_i,s*2+1],t[r_i,s*2+sn+1]
				m00 = metrics[s,i]+(m[i]*t[r_i,s*2]).real
				m08 = metrics[s+sn/2,i]+(m[i]*t[r_i,s*2+sn]).real
				if m00>m08:
					metrics[s*2,i+1]=m00
					tracback[s*2,i]=0
				else:
					metrics[s*2,i+1]=m08
					tracback[s*2,i]=1
				#print m00,m08,
				# shift in 1
				m10 = metrics[s,i]+(m[i]*t[r_i,s*2+1]).real
				m18 = metrics[s+sn/2,i]+(m[i]*t[r_i,s*2+sn+1]).real
				if m10>m18:
					metrics[s*2+1,i+1]=m10
					tracback[s*2+1,i]=0
				else:
					metrics[s*2+1,i+1]=m18
					tracback[s*2+1,i]=1
				#print m10,m18
	        #print r_i,m[i],mindiff(m[i],t[r_i,:])
			#print "%3d %3d"%(i,maxState(metrics[:,i+1])),tracback[:,i],m[i]
			r_i = 1 - r_i
		end = metrics[:,l]
		ends = end.argmax()
		print "end state",ends
		ret = []
		es = ends
		for i in range(4):
			ret.append(es&1)
			es >>= 1

		for i in range(l-1,0,-1):
			b = tracback[ends,i]
			ret.append(b)
			ends /=2
			ends += b*sn/2

		return ret[::-1]