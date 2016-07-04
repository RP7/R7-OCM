INC = src/include

SRCS = src/c/ad9361.c \
	src/c/iomem.c \
	src/c/fm.c \
	src/c/aximem.c
	
lib/q7.so : $(SRCS)
	gcc -I$(INC) -fPIC -shared -o lib/q7.so $(SRCS)

clean:
	rm R7OCM.cache -rf
	rm R7OCM.hw -rf
	rm R7OCM.ioplanning -rf
	rm R7OCM.runs -rf
	rm R7OCM.sdk -rf
	rm R7OCM.sim -rf
	rm R7OCM.srcs -rf
	rm src.tgz -f
	rm R7OCM.xpr -f
	rm .Xil -rf
	rm src/python/*.pyc -f
	rm src/python/web/*.pyc -f
	rm lib/* -f
	rm temp/* -f

backup:
	tar -X .gitignore -czf ../R7OCM.tgz .

install:
	chmod +x scripts/upload.sh
	chmod +x scripts/curlinit.sh
	cp scripts/post-commit .git/hooks/
	chmod +x .git/hooks/post-commit

HOSTINC = -Isrc/host/include \
		  -Isrc/host/cpp/USRT/include \
		  -Isrc/include

HOSTFLAG=-fPIC -fpermissive -Lwork -g
LIBS = /tmp/libUSRT.so /tmp/libmd5api.so /tmp/libQ7.so

HOSTLDFLAG=-ldl -lpthread $(LIBS)

/tmp/libQ7.so: src/host/cpp/Q7Mem/Q7Mem.cpp src/host/cpp/Q7Mem/Q7MemAPI.cpp src/host/cpp/sysClock/sysClock.cpp
	g++ ${HOSTINC} ${HOSTFLAG} -shared -o /tmp/libQ7.so src/host/cpp/Q7Mem/Q7Mem.cpp src/host/cpp/Q7Mem/Q7MemAPI.cpp src/host/cpp/sysClock/sysClock.cpp /tmp/libUSRT.so /tmp/libmd5api.so $(LDFLAG)

hostlib:/tmp/libQ7.so

usrtlib:
	mkdir -p work
	mkdir -p src/host/cpp/USRT/work
	cd src/host/cpp/USRT;make work/libmd5api.so
	cp src/host/cpp/USRT/work/libmd5api.so /tmp
	cd src/host/cpp/USRT;make work/libUSRT.so
	cp src/host/cpp/USRT/work/libUSRT.so /tmp
	sudo ldconfig


work/initQ7Mem : src/host/cpp/Q7Mem/initMem.cpp 
	g++ ${HOSTINC} ${HOSTFLAG} -o work/initQ7Mem src/host/cpp/Q7Mem/initMem.cpp $(HOSTLDFLAG)

work/dumpQ7Mem : src/host/cpp/Q7Mem/dumpMem.cpp 
	g++ ${HOSTINC} ${HOSTFLAG} -o work/dumpQ7Mem src/host/cpp/Q7Mem/dumpMem.cpp $(HOSTLDFLAG)

work/rxclock : src/host/cpp/sysClock/rxclock.cpp 
	g++ ${HOSTINC} ${HOSTFLAG} -o work/rxclock src/host/cpp/sysClock/rxclock.cpp $(HOSTLDFLAG)

work/Q7UDP :  src/host/cpp/Q7Mem/Q7UDP.cpp 
	g++ ${HOSTINC} ${HOSTFLAG} -o work/Q7UDP src/host/cpp/Q7Mem/Q7UDP.cpp $(HOSTLDFLAG)

hostutils = work/initQ7Mem \
	work/dumpQ7Mem \
	work/Q7UDP \
	work/rxclock 

host:${hostutils} hostlib

/tmp/libcgsm.so:src/host/cpp/gsm/ve.cpp src/host/cpp/gsm/vd.cpp
	g++ ${HOSTINC} ${HOSTFLAG} -shared -o /tmp/libcgsm.so src/host/cpp/gsm/ve.cpp src/host/cpp/gsm/vd.cpp

	