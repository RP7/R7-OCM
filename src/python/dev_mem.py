import mmap
from ctypes import *

class dev_mem:
    DEVNAME = '/dev/mem'
    def __init__(self,BASE,LEN):
        self.len = LEN
        self.base = BASE
        self.fd = open(dev_mem.DEVNAME,'r+b',buffering)
        self.mmap = mmap.mmap(self.fd.fileno(),LEN, offset=BASE) 

    def ioread(self,addr):
        buf = self.memread(addr,1)
        return buf[0]

    def iowrite(self,addr,d):
        buf = (c_uint*1)()
        buf[0] = d
        self.memwrite(addr,d)
    
    def memread(self,addr,len):
        buf = (c_uint*len)()
        self.mmap.seek(addr)
        memmove(buf,self.mmap.read(4*len),4*len)
        return buf

    def memwrite(self,addr,buf):
        self.mmap.seek(addr)
        self.mmap.write(buf)




