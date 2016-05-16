#ifndef __IOMEM_H
#define __IOMEM_H
#include <sys/mman.h>

typedef struct iomem_struct {
	char *dev;
	char *TAG;
	off_t addr;
	size_t size;
	int fd;
	void *mem;
} IOMEM;

void *iommap(IOMEM* io);
int iomunmap(IOMEM* io);
void *io_off(IOMEM *io,int offset);
#endif


