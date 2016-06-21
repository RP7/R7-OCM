import gsmlib.GSMC0 as C0
import matplotlib.pyplot as plt

import Q7Mem

import numpy as np
import gsmlib.splibs as sp

rx = Q7Mem.rx()
c0 = C0.GSMC0()
c0.setRx(rx)
c0.initSCH()
r = c0.run()

plt.plot(r)

plt.show()

sb = c0.C0.frame[1][0]
