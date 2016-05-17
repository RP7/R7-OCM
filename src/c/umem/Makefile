obj-m += umem.o
RELEASE = `uname -r`
KDIR:=/lib/modules/$(RELEASE)/build
all:
	make -C $(KDIR) M=`pwd` modules
clean:
	make -C $(KDIR) M=`pwd` modules clean
	rm -f modules.order
	rm -f *~
