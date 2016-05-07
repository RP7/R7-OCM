#ifndef _OCM_IO_H
#define _OCM_IO_H

#define _OCM_IO_(ZZ)		(*((int *)(g_OCM_pntr + ZZ)))

extern int drvOCM_OpenDev( const char *dev );
extern int drvOCM_CloseDev( const int fd );
extern void *drvOCM_Mmap(int fd , int addr_base);
extern int drvOCM_Munmap( void *pntr , int len );
extern int drvOCM_Init( void );
extern int drvOCM_Read( int io_addr );
extern int drvOCM_ReadMem( int start_addr, int *rd_data, int num );
extern int drvOCM_Write( int io_addr , int io_data );
extern int drvOCM_WriteMem( int start_addr , int *wr_data, int num );
#endif
