import gsmlib.GSMC0 as C0
import matplotlib.pyplot as plt

import numpy as np
import gsmlib.splibs as sp
import gsmlib.Burst as Burst
import gsmlib.burstfile as burstfile

c0 = C0.GSMC0()

c0.initSCH()
c0.initBCCH()

file = "../../../temp/log"

bf = burstfile.burstfile(file)
c0.state.timingSyncState.to("fine")
for i in range(3):
	c0.state.timingSyncState.once()
for cnt in range(8*51*26*10):
	b,_F = bf.toC0(c0)
	if b.ch!=None:
		ok,data = b.ch.callback(b,_F,c0.state)
	
