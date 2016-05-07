#include <stdio.h>
#include <sys/mman.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

#include "ocm_io.h"

/********************************************************************/
/* v1.0 : 实现基本IO读写功能
/* v1.1 : 支持连续读写，用memcpy方式
/********************************************************************/

#define VER					"1.1"				
#define TAG_OCM					"[drvOCM]"
#define DEVNAME_OCM 			"/dev/mem"
#define OCM_ADDR_BASE		0xfffC0000

void *g_OCM_pntr;

int drvOCM_OpenDev(const char *dev)
{
	int fd = 0;

	fd = open(dev , O_RDWR | O_SYNC);
	if(fd < 0)
	{
		printf("%s Can't Open %s\n" , TAG_OCM , dev);
		return -1;
	}
	else
	{
		printf("%s Open %s Success \n" , TAG_OCM , dev);
		printf("%s fd is : %d\n" , TAG_OCM , fd);
		return fd;
	}

}
int drvOCM_CloseDev(const int fd)
{
    return close(fd);
}

void *drvOCM_Mmap(int fd , int addr_base)
{
	void *pntr = (void *)0;

	pntr = mmap(0 , 0X40000 , PROT_READ|PROT_WRITE ,  MAP_FILE|MAP_SHARED , fd , addr_base);
	
	if(pntr == NULL)
	{
		printf("%s Can't Open mmap\n" , TAG_OCM);
		close(fd);
		return NULL;
	}
	else if(pntr == (void *)(-1))
	{
		printf("%s Can't Open mmap\n" , TAG_OCM);
		printf("%s InValid addr : 0x%x\n" , TAG_OCM , pntr);
		close(fd);
		return NULL;
	}
	else
	{
		printf("%s Open Mmap Success\n" , TAG_OCM);
		printf("%s Valid addr : 0x%x\n", TAG_OCM , pntr);
		return pntr;
	}
}

int drvOCM_Munmap( void *pntr , int len )
{
	munmap( pntr , len );
	return 0;
}

int drvOCM_Init( void )
{
	int fd = 0;

	// Open /dev/axi_gp_0
	fd = drvOCM_OpenDev(DEVNAME_OCM);
	// Mmap OCM Hw Addr.
	g_OCM_pntr = drvOCM_Mmap(fd , OCM_ADDR_BASE);
	return fd;
}

int drvOCM_Read( int io_addr )
{
	int io_data = 0;

	io_data = _OCM_IO_(io_addr);	

	return io_data;
}

int drvOCM_ReadMem( int start_addr, int *rd_data, int num )
{
	memcpy( rd_data, g_OCM_pntr + start_addr, sizeof(int) * num );

	return 0;
}

int drvOCM_Write( int io_addr , int io_data )
{	
	_OCM_IO_(io_addr) = io_data;

	return 0;
}

int drvOCM_WriteMem( int start_addr , int *wr_data, int num )
{	
	memcpy( g_OCM_pntr + start_addr, wr_data, sizeof(int) * num );

	return 0;
}


