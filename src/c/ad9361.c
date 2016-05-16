#include <unistd.h>
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
	.off_t = AD9361_SP_BASE,
	.size_t = AD9361_SPI_SIZE,
	.fd = 0,
	.mem = NULL
};

static IOMEM fpga_io = {
	.dev = ad9361_dev,
	.TAG = fpgaio_tag,
	.off_t = FPGA_BASE,
	.size_t = FPGA_SIZE,
	.fd = 0,
	.mem = NULL
};

static IOMEM ocm_mem = {
	.dev = ad9361_dev,
	.TAG = ocm_tag,
	.off_t = OCM_BASE,
	.size_t = OCM_SIZE,
	.fd = 0,
	.mem = NULL
};

#define FPGA_IO(x) (*(io_off(&fpga_io,x)))

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
	SPIREG *reg = (SPIREG *)(ad9361_spi.mem);
	H8 = addr>>8;
	reg->SPI_Config(0x4015);
	reg->SPI_Tx_data = H8;
	reg->SPI_Tx_data = addr;
	reg->SPI_Tx_data = data;
	while(~(reg->SPI_Intr_status&0x2))
	{
		sleep(1);
		timeout++;
		if(timeout>SPITIMEOUT)
			break;
	}
	reg->SPI_Config(0x7c15);
	H8 = reg->SPI_Rx_data;
	HL = reg->SPI_Rx_data;
	ret = reg->SPI_Rx_data;
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
