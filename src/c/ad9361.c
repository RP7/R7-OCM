#include <unistd.h>
#include <stdio.h>
#include "iomem.h"
#include "dev_mem.h"
#include "spi.h"

#define SPITIMEOUT 100
static const char ad9361_tag[] = "AD9361_SPI";
static const char ad9361_dev[] = SPIDevice;
static const char fpgaio_tag[] = "FPGA_IO";
static const char ocm_tag[] = "OCM_MEM";


static IOMEM ad9361_spi = {
	.dev = ad9361_dev,
	.TAG = ad9361_tag,
	.addr = AD9361_SP_BASE,
	.size = AD9361_SPI_SIZE,
	.fd = 0,
	.mem = NULL,
	.cnt = 0
};

static IOMEM fpga_io = {
	.dev = ad9361_dev,
	.TAG = fpgaio_tag,
	.addr = FPGA_BASE,
	.size = FPGA_SIZE,
	.fd = 0,
	.mem = NULL
};

static IOMEM ocm_mem = {
	.dev = ad9361_dev,
	.TAG = ocm_tag,
	.addr = OCM_BASE,
	.size = OCM_SIZE,
	.fd = 0,
	.mem = NULL
};

#define FPGA_IO(x) (*((int *)io_off(&fpga_io,x)))
#define SPI_REG(x) (*((int *)io_off(&ad9361_spi,x)))

void ad9361_init()
{
	iommap(&ad9361_spi);
	iommap(&fpga_io);
	iommap(&ocm_mem);
	ad9361_spi.cnt = 0;

}

void ad9361_deinit()
{
	iomunmap(&ad9361_spi);
	iomunmap(&fpga_io);
	iomunmap(&ocm_mem);
}

int ad9361_spi_op(int addr,int data)
{
	int H8,HL,ret;
	int timeout = 0;
	H8 = addr>>8;
	SPI_REG(SPI_RX_thres) = 3;
	SPI_REG(SPI_Config) = 0x4015;
	SPI_REG(SPI_Tx_data) = H8;
	SPI_REG(SPI_Tx_data) = addr;
	SPI_REG(SPI_Tx_data) = data;
	ret = 0;
	while(ret==0)
	{
		ret = SPI_REG(SPI_Intr_status)&0x10;
		timeout++;
		if(timeout>SPITIMEOUT)
			printf("%s spi op timeout A=[%03x] D=[%02x]\n",ad9361_spi.TAG,addr,data);
			break;
	}
	usleep(1);
	SPI_REG(SPI_Config) = 0x7c15;
	H8 = SPI_REG(SPI_Rx_data);
	HL = SPI_REG(SPI_Rx_data);
	ret = SPI_REG(SPI_Rx_data);
	return ret;
}

void ad9361_spi_write(int addr, int data)
{
	addr &= 0x3ff;
	addr |= 0x8000;
	ad9361_spi_op(addr,data);
}

int ad9361_spi_read(int addr, int data)
{
	addr &= 0x3ff;
	return ad9361_spi_op(addr,0xff);
}

void RESET_AD9361()
{
	FPGA_IO(AD9361_RST) = 0;
	FPGA_IO(AD9361_RST) = 1;
}

int readSPI_C(int addr)
{
	return *((int *)(ad9361_spi.mem+addr));
}

int writeSPI_C(int addr, int data)
{
	return *((int *)(ad9361_spi.mem+addr));
}

void clearSPIRxFIFO()
{
	int r;
	int timeout = 0;
	while(ad9361_spi.cnt>0)
	{
		r = SPI_REG(SPI_Rx_data);
		ad9361_spi.cnt--;
	}
}

void writeNoWait(int *buf, int len)
{
	int i = 0;
	int timeout;
	if(SPI_REG(SPI_Intr_status)&0x40) SPI_REG(SPI_Intr_status) = 0x40;
	SPI_REG(SPI_Config) = 0x15;
	SPI_REG(SPI_TX_thres) = 120;
	for(i=0;i<len;i++)
	{
		timeout = 0;
		while((SPI_REG(SPI_Intr_status)&0x4)==0x0)
		{
			timeout++;
			if(timeout>SPITIMEOUT)
			{	
				printf("%s spi write no wait timeout [%d]\n",ad9361_spi.TAG,i);
				break;
			}
		}
		SPI_REG(SPI_Tx_data) = buf[i];
		ad9361_spi.cnt++;
	}
}

int readNoWait(int addr)
{
	int timeout,H8,HL,ret;
	clearSPIRxFIFO();
	SPI_REG(SPI_Config) = 0x15;
	addr &= 0x3ff;
	H8 = addr>>8;
	SPI_REG(SPI_Tx_data) = H8;
	SPI_REG(SPI_Tx_data) = addr;
	SPI_REG(SPI_Tx_data) = 0xff;
	ret = 0;
	timeout = 0;
	while(ret==0)
	{
		ret = SPI_REG(SPI_Intr_status);
		printf("%s spi read no wait A=[%03x] S=[%02x]\n",ad9361_spi.TAG,addr,ret);
		ret &= 0x10;
		timeout++;
		if(timeout>SPITIMEOUT)
			printf("%s spi read no wait timeout A=[%03x]\n",ad9361_spi.TAG,addr);
			break;
	}
	H8 = SPI_REG(SPI_Rx_data);
	HL = SPI_REG(SPI_Rx_data);
	ret = SPI_REG(SPI_Rx_data);
	return ret;
}
