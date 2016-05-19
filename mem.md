# 内存
## OCM
OCM被映射到0xfffc0000开始的256K内存空间，可以作为射频数据或者加速器使用
## 常规内存
可以在操作系统启动时保留一部分内存给硬件使用
修改uboot的配置，add to uEnv.txt

		fdt_high=0x10000000
		initrd_high=0x10000000
		bootargs=console=ttyPS0,115200 root=/dev/ram rw earlyprintk mem=480M

从0x1e00-0000开始的32M空间操作系统就不再使用了。

### /proc/umem（没有实现）
建立一个Q7用户空间的物理内存管理机制

* init/deinit

申请一块内存

    cat 'TxBuf 16M' > /proc/umem/init
    {'ret':'ok'}
    
/proc/q7umem 下会出现一个 TxBuf 的文件

    cat /proc/umem
    {'Name':'TxBuf','Phy_Addr':0x10000000,'Len':0x1000000}
    
释放一块内存

    cat 'TxBuf' > /proc/deinit
    {'ret':'ok'}
    