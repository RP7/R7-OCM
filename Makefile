SRCS = src/c/ad9361.c \
	src/c/iomem.c 
lib/q7.so : $(SRCS)
	gcc -fPIC -shared -o lib/q7.so $(SRCS)

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
	
	
	
	