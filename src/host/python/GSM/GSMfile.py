import wave
import struct
from matplotlib.pylab import *
from GSMChan import GSMChan
from FB import FB
from SB import SB

class GSMfile(GSMChan):
	
	def __init__(self,fn):
		f = wave.open(fn,"rb")

		params = f.getparams()  
		nchannels, sampwidth, self.framerate, self.nframes = params[:4]
		print nchannels, sampwidth, self.framerate, self.nframes
		self.nframes =  120000*100 #for test
		raw = f.readframes(self.nframes)
		GSMChan.__init__(self,raw)
		f.close()
		
		
if __name__ == '__main__':

	aGSM = GSMfile('e:/zhaom/works/hackrf/gsmsch/data/gsm_11_09.wav')
	fMap,fpos,fm = aGSM.fbsearch()
	"""
	aGSM.channelPower()
	chs,fbs = aGSM.channels(3.25e6/3)
	aFB = FB()
	pos,peek,freq = aFB.rough(chs[-7])
	
	inx = aFB.find(chs[-7],pos,freq)
	
	aSB = SB()
	dem = aSB.diff(chs[-7][inx:inx+625*9])
	"""
	
	
	

		
	