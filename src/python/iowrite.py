import axi2s_c
import sys

uut = axi2s_c.axi2s_c()
uut.write(sys.argv[1],int(sys.argv[2],16))


