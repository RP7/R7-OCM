import numpy as np

import gsmlib.splibs as sp
import matplotlib.pyplot as plt

def readfile(fn):
	f = open(fn)
	l = []
	for line in f.readlines():
		line = line.replace("+-","-")
		a = complex(line)
		l.append(a)
	return np.array(l)
mafi = readfile("../../../data/mafi")
training = readfile("../../../data/training")
rhh = readfile("../../../data/rhh")

mafi = mafi/rhh[2]
rhh = rhh/rhh[2]

def toState(t,r_i):
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

def s2s(s,r_i):
	"""
	inverse order
	rf = 1
	if = 0
	"""
	ret = np.zeros(5,dtype=complex)
	if r_i==1:
		inc = 1
	else:
		inc = 0
	for i in range(5):
		if (s&1)==1:
			ret[i] = 1.+0j
		else:
			ret[i] = -1.+0j
		s >>=1
		if (i+inc)%2 == 0:
			ret[i] *= 1.j
	return ret


def table(r):
	t = np.zeros((2,32),dtype=complex)
	for r_i in range(2):
		for s in range(32):
			t[r_i][s]=np.dot(s2s(s,r_i),r)
	return t
def mindiff(x,h):
    y = h-x
    yy = y*np.conj(y)
    return bin(yy.argmin())
def t2b(t,r_i):
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
            
def maxState(h):
    return h.argmax()    
def forward(t,m,start,r_i,l):
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
		print "%3d %3d"%(i,maxState(metrics[:,i+1])),tracback[:,i],m[i]
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

t = table(rhh)
fout = np.zeros(64,dtype=complex)
for i in range(64-5):
    
	ss = toState(training[i:i+5],i%2)
	r_i = i%2
	#print training[i],"%4d"%(ss),t[r_i][ss],mafi[42+2+i]
	fout[i]=t[r_i][ss]

y = t2b(training,0)

from gsmlib.viterbi_detector import viterbi_detector

v = viterbi_detector(5,len(mafi),training)
v.table(rhh)
#z = v.forward(mafi[42+62:])
a = v.forward(mafi)
v.table(np.conj(rhh))
b = v.backward(mafi[::-1])
b = b[::-1]
x = forward(np.conj(t),mafi,0,0,len(mafi))

# c = v.forward(mafi[::-1])
# c = c[::-1]
# d = v.backward(mafi[::-1])
# d = d[::-1]


