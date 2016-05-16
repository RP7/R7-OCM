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
	.mem = NULL
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

void ad9361_init()
{
	iommap(&ad9361_spi);
	iommap(&fpga_io);
	iommap(&ocm_mem);

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
	SPIREG *reg = (SPIREG *)(ad9361_spi.mem);
	H8 = addr>>8;
	reg->reg_Config = 0x4015;
	reg->reg_Tx_data = H8;
	reg->reg_Tx_data = addr;
	reg->reg_Tx_data = data;
	ret = 0;
	while(ret==0)
	{
		ret = reg->reg_Intr_status&0x4;
		timeout++;
		if(timeout>SPITIMEOUT)
			printf("%s spi op timeout A=[%03x] D=[%02x]\n",ad9361_spi.TAG,addr,data);
			break;
	}
	reg->reg_Config = 0x7c15;
	H8 = reg->reg_Rx_data;
	HL = reg->reg_Rx_data;
	ret = reg->reg_Rx_data;
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
	SPIREG *reg = (SPIREG *)(ad9361_spi.mem);
	while((reg->reg_Intr_status&0x10)==0x0)
	{
		r = reg->reg_Rx_data;
		timeout++;
		if(timeout>SPITIMEOUT)
		{	
			printf("%s spi clear rx fifo timeout\n",ad9361_spi.TAG);
			break;
		}
	}
	if(reg->reg_Intr_status&0x01) reg->reg_Intr_status = 0x01;
}

void writeNoWait(int *buf, int len)
{
	SPIREG *reg = (SPIREG *)(ad9361_spi.mem);
	int i = 0;
	int timeout;
	if(reg->reg_Intr_status&0x40) reg->reg_Intr_status = 0x40;
	reg->reg_Config = 0x15;
	reg->reg_TX_thres = 120;
	for(i=0;i<len;i++)
	{
		timeout = 0;
		while((reg->reg_Intr_status&0x4)==0x0)
		{
			timeout++;
			if(timeout>SPITIMEOUT)
			{	
				printf("%s spi write no wait timeout [%d]\n",ad9361_spi.TAG,i);
				break;
			}
			clearSPIRxFIFO();
		}
		reg->reg_Tx_data = buf[i];
	}
	clearSPIRxFIFO();
}

int readNoWait(int addr)
{
	SPIREG *reg = (volatile SPIREG *)(ad9361_spi.mem);
	int timeout,H8,HL,ret;
	reg->reg_Config = 0x15;
	reg->reg_RX_thres = 0;
	H8 = reg->reg_Rx_data;
	addr &= 0x3ff;
	H8 = addr>>8;
	reg->reg_Tx_data = H8;
	reg->reg_Tx_data = addr;
	reg->reg_Tx_data = 0xff;
	ret = 0;
	timeout = 0;
	while(ret==0)
	{
		ret = reg->reg_Intr_status&0x14;
		timeout++;
		if(timeout>SPITIMEOUT)
			printf("%s spi read no wait timeout A=[%03x]\n",ad9361_spi.TAG,addr);
			break;
	}
	reg->reg_Config = 0x15;
	H8 = reg->reg_Rx_data;
	HL = reg->reg_Rx_data;
	ret = reg->reg_Rx_data;
	return ret;
}
