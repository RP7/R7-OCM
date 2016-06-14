import math
import numpy as np
def Qfuncx(t):
	a = 0.
	T = int(t*10000)
	for x in range(T,100*10000):
		v = x/10000.
		a = a + (1/math.sqrt(2.*math.pi))*math.exp(0-v*v/2.)
	return a/10000.

def Qfunc(t):
	return 0.5-0.5*math.erf(t/math.sqrt(2.))

def Ffunc(t,B):
	a = 2.*math.pi*B/math.sqrt(math.log(2.))
	return 0.5*(Qfunc((t-0.5)*a)-Qfunc((t+0.5)*a))

def Fserial(B,OS,R,W):
	X=[]
	for t in range(-OS*R,OS*R):
		X.append(Ffunc(t/float(OS),B))
	sum = 0.
	for T in range(0,len(X)):
		sum = sum + X[T]
	all = sum
	Y=[]
	sum = 0.
	for T in range(0,len(X)):
		sum = sum + X[T]
		Y.append(int(sum/all*float(W-1)+.5))
	return Y

def fserial(B,OS,R):
	X=[]
	for t in range(-OS*R,OS*R):
		X.append(Ffunc(t/float(OS),B))
	sum = 0.
	for T in range(0,len(X)):
		sum = sum + X[T]
	all = sum
	print 'all',all
	Y=[]
	sum = 0.
	for T in range(0,len(X)):
		sum = sum + X[T]
		Y.append(sum/all*np.pi/2.)
	return Y

if __name__ == '__main__':
	S = fserial(0.3,4,2)
	print "#",len(S)
	for T in range(0,len(S)):
		print T,S[T]