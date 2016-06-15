# 内存
## OCM
OCM被映射到0xfffc0000开始的256K内存空间，可以作为射频数据或者加速器使用
缺省使用OCM，访问速度快，不占用内存带宽。
但OCM比较小，如果缓冲大块数据无法使用这种模式，下面描述使用DRAM作为缓冲区的方法。
## 常规内存
### 保留操作系统不管理的内存
可以在操作系统启动时保留一部分内存给硬件使用
修改uboot的配置，add to uEnv.txt

		fdt_high=0x10000000
		initrd_high=0x10000000
		bootargs=console=ttyPS0,115200 root=/dev/ram rw earlyprintk mem=480M

从0x1e00-0000开始的32M空间操作系统就不再使用了。
### 修改AXIDMA的配置
AXI DMA有4个参数可以配置，分别是收发的BASE和SIZE。寄存器名：
		
		AXI_ISIZE
		AXI_IBASE
		AXI_OSIZE
		AXI_OBASE

修改AXI_IBASE和AXI_OBASE到0x1e00-0000开始的32M空间去，这段内存操作系统不会使用。
修改AXI_ISIZE和AXI_OSIZE为合适的值，收发公用32M内存，并且为64自家的整数倍。



