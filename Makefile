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
HOSTLDFLAG=-ldl -lpthread

work/libQ7.so: hostlib src/host/cpp/Q7Mem/Q7Mem.cpp src/host/cpp/Q7Mem/Q7MemAPI.cpp src/host/cpp/sysClock/sysClock.cpp
	g++ ${HOSTINC} ${HOSTFLAG} -shared -o work/libQ7.so src/host/cpp/Q7Mem/Q7Mem.cpp src/host/cpp/Q7Mem/Q7MemAPI.cpp src/host/cpp/sysClock/sysClock.cpp work/libUSRT.so work/libmd5api.so $(LDFLAG)

hostlib:
	mkdir -p work
	mkdir -p src/host/cpp/USRT/work
	cd src/host/cpp/USRT;make work/libUSRT.so
	cp src/host/cpp/USRT/work/*.so work

work/initQ7Mem : src/host/cpp/Q7Mem/initMem.cpp work/libQ7.so work/libmd5api.so work/libUSRT.so
	g++ ${HOSTINC} ${HOSTFLAG} -o work/initQ7Mem src/host/cpp/Q7Mem/initMem.cpp work/libQ7.so work/libmd5api.so work/libUSRT.so $(HOSTLDFLAG)

work/dumpQ7Mem : src/host/cpp/Q7Mem/dumpMem.cpp work/libQ7.so work/libmd5api.so work/libUSRT.so
	g++ ${HOSTINC} ${HOSTFLAG} -o work/dumpQ7Mem src/host/cpp/Q7Mem/dumpMem.cpp work/libQ7.so work/libmd5api.so work/libUSRT.so $(HOSTLDFLAG)

work/Q7UDP :  src/host/cpp/Q7Mem/Q7UDP.cpp work/libQ7.so work/libmd5api.so work/libUSRT.so
	g++ ${HOSTINC} ${HOSTFLAG} -o work/Q7UDP src/host/cpp/Q7Mem/Q7UDP.cpp work/libQ7.so work/libmd5api.so work/libUSRT.so $(HOSTLDFLAG)

hostutils:work/initQ7Mem \
	work/dumpQ7Mem \
	work/Q7UDP

host:hostutils

	