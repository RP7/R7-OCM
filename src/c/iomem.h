#ifndef __IOMEM_H
#define __IOMEM_H
#include <sys/mman.h>
#include <fcntl.h>

typedef struct iomem_struct {
	const char *dev;
	const char *TAG;
	off_t addr;
	size_t size;
	int fd;
	void *mem;
	int cnt;
} IOMEM;

void *iommap(IOMEM* io);
int iomunmap(IOMEM* io);
void *io_off(IOMEM *io,int offset);
#endif


