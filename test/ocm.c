#include <stdio.h>
#include <sys/mman.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

#define DEVNAME "/dev/mem"
#define FPGA_ADDR_BASE 0xFFFC0000
void *g_FPGA_pntr;
#define _FPGA_IO_(ZZ) (*((int *)(g_FPGA_pntr + ZZ)))
#define TAG "MEM"

int drvFPGA_Init( void );
char buffer[65536];

int main()
{
	int i,j;
	int *p;
	drvFPGA_Init();
	p = (int *)buffer;
	for(i=0;i<256*64;i++) *(p+i)=i*4;

	drvFPGA_WriteMem( 0x10000, p, 65536/sizeof(int) );

	for(i=0;i<256*64;i++) *(p+i)=0;

	drvFPGA_ReadMem( 0, p, 65536/sizeof(int) );
	for(i=0;i<256*16;i++)
	{
		if((i%16)==0) printf("\n%03x ",i>>4);	
		printf("%08x ",*(p+i));
	}
}

int drvFPGA_OpenDev(const char *dev)
{
	int fd = 0;

	fd = open(dev , O_RDWR | O_SYNC);
	if(fd < 0)
	{
		printf("%s Can't Open %s\n" , TAG , dev);
		return -1;
	}
	else
	{
		printf("%s Open %s Success \n" , TAG , dev);
		printf("%s fd is : %d\n" , TAG , fd);
		return fd;
	}
}

int drvFPGA_CloseDev(const int fd)
{
    return close(fd);
}

void *drvFPGA_Mmap(int fd , int addr_base)
{
	void *pntr = (void *)0;

	pntr = mmap(0 , 0x40000 , PROT_READ|PROT_WRITE ,  MAP_FILE|MAP_SHARED , fd , addr_base);
	
	if(pntr == NULL)
	{
		printf("%s Can't Open mmap\n" , TAG);
		close(fd);
		return NULL;
	}
	else if(pntr == (void *)(-1))
	{
		printf("%s Can't Open mmap\n" , TAG);
		printf("%s InValid addr : 0x%x\n" , TAG , pntr);
		close(fd);
		return NULL;
	}
	else
	{
		printf("%s Open Mmap Success\n" , TAG);
		printf("%s Valid addr : 0x%x\n", TAG , pntr);
		return pntr;
	}
}

int drvFPGA_Munmap( void *pntr , int len )
{
	munmap( pntr , len );
	return 0;
}

int drvFPGA_Init( void )
{
	int fd = 0;

	//Open /dev/axi_gp_0
	fd = drvFPGA_OpenDev(DEVNAME);
	//Mmap FPGA Hw Addr.
	g_FPGA_pntr = drvFPGA_Mmap(fd , FPGA_ADDR_BASE);
	return fd;
}

int drvFPGA_Read( int io_addr )
{
	int io_data = 0;
	io_data = _FPGA_IO_(io_addr);	
	return io_data;
}

int drvFPGA_ReadMem( int start_addr, int *rd_data, int num )
{
	memcpy( rd_data, g_FPGA_pntr + start_addr, sizeof(int) * num );
	return 0;
}

int drvFPGA_Write( int io_addr , int io_data )
{	
	_FPGA_IO_(io_addr) = io_data;
	return 0;
}

int drvFPGA_WriteMem( int start_addr , int *wr_data, int num )
{	
	memcpy( g_FPGA_pntr + start_addr, wr_data, sizeof(int) * num );
	return 0;
}

