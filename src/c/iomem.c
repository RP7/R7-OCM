#include "iomem.h"
#include <stdio.h>

void *iommap(IOMEM* io)
{
	io->fd = 0;

	io->fd = open(io->dev , O_RDWR | O_SYNC);
	if(io->fd < 0)
	{
		printf("%s Can't Open %s\n" ,io->TAG , io->dev);
		return NULL;
	}
	printf("%s Open %s Success \n" ,io->TAG , io->dev);
	printf("%s fd is : %d\n" ,io->TAG , io->fd);
	io->mem = (void *)0;

	io->mem = mmap(0 , io->size , PROT_READ|PROT_WRITE ,  MAP_FILE|MAP_SHARED , io->fd , io->addr);
	
	if(io->mem == NULL)
	{
		printf("%s Can't Open mmap\n" , io->TAG);
		close(io->fd);
		return NULL;
	}
	if(io->mem == (void *)(-1))
	{
		printf("%s Can't Open mmap\n" , io->TAG);
		printf("%s InValid addr : 0x%x\n" , io->TAG , io->mem);
		close(io->fd);
		return NULL;
	}
	printf("%s Open Mmap Success\n" , io->TAG);
	printf("%s Valid addr : 0x%x\n", io->TAG , io->mem);
	return io->mem;
}

int iomunmap(IOMEM* io)
{
    munmap( io->mem , io->size );
    return close(io->fd);
}

void *io_off(IOMEM *io,int offset)
{
	return (void *)(io->mem+offset);
}
