#include <unistd.h>
#include <stdio.h>
#include "iomem.h"
#include "dev_mem.h"
#include "spi.h"

#define SPITIMEOUT 10
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
	while(~(reg->reg_Intr_status&0x2))
	{
		sleep(1);
		timeout++;
		if(timeout>SPITIMEOUT)
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

