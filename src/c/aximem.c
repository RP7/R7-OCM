#include <inttypes.h>
#include <unistd.h>
#include <stdio.h>

#include "aximem.h"
#include "iomem.h"

static const char axi_mem_tag[] = "AXIMEM";
static const char MEM_dev[] = "/dev/mem";
static const char fpgaio_tag[] = "FPGA_IO";


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

