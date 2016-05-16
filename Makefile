SRCS = src/c/ad9361.c \
	src/c/iomem.c 
lib/q7.so : $(SRCS)
	gcc -shared -o lib/q7.so $(SRCS)
	