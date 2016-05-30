#include <inttypes.h>
#include <unistd.h>
#include <stdio.h>

#include "aximem.h"
#include "iomem.h"

static const char axi_mem_tag[] = "AXIMEM";
static const char MEM_dev[] = "/dev/mem";
static const char fpgaio_tag[] = "FPGA_IO";

#define AXI2S_IACNT     0x00010
#define AXI2S_IBCNT     0x00014
#define AXI2S_OACNT     0x00018
#define AXI2S_OBCNT     0x0001c

static IOMEM axi_mem = {
	.dev = MEM_dev,
	.TAG = axi_mem_tag,
	.addr = AXIMEM_BASE,
	.size = AXIMEM_SIZE,
	.fd = 0,
	.mem = NULL,
	.cnt = 0
};

static IOMEM fpga_io = {
	.dev = MEM_dev,
	.TAG = fpgaio_tag,
	.addr = FPGA_BASE,
	.size = FPGA_SIZE,
	.fd = 0,
	.mem = NULL
};

void axi_init(aximem_t *axi)
{
	if( fpga_io.mem != NULL ) 
		axi->c_mmap = fpga_io.mem;
	else
		axi->c_mmap = iommap(&fpga_io);
	if( axi_mem.mem != NULL ) 
		axi->u_mmap = axi_mem.mem;
	else
		axi->u_mmap = iommap(&axi_mem);
}

#define FPGA_IO(x) (*((int *)(&(fpga_io.mem+x))))

int axi_get(int s, int l, axiconfig_t *c)
{
	int o = FPGA_IO[AXI2S_IACNT];
	if (o>s && o<s+l) {
		c->p = NULL;
		return 0;
	}
	c->p = axi_mem.mem+s;
	return l;		
}

int axi_put(int s, int l, axiconfig_t *c)
{
	int o = FPGA_IO[AXI2S_OACNT];
	if (o<s && o>s+l) 
		memcpy(axi_mem.mem+s,c->p,l);
		return l;		
	}
	return 0;
}
