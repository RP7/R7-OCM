#include <inttypes.h> //uint32_t,uint64_t
#include <unistd.h>
#include <stdio.h>
#include <string.h> //memcpy

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

#define FPGA_IO(x) (*((uint32_t *)(fpga_io.mem+(x))))

static inline uint64_t f2t(uint32_t f, uint32_t s, uint32_t size)
{
	return (uint64_t)f*(uint64_t)(size)+(uint64_t)s;
}

static inline uint32_t t2addr(uint64_t t, axi_entity_t *e)
{
	return (uint32_t)(t%(uint64_t)(e->size))+e->base;
}

static inline void load_time(axi_entity_t *e,uint32_t base)
{
	e->acnt = FPGA_IO(base);
	e->bcnt = FPGA_IO(base+4);
	e->time = f2t(e->bcnt,e->acnt,e->size);
	
}

int axi_get(axi_dma_t *c)
{
	uint64_t start = c->inp.start;
	uint32_t l = c->inp.length;
	load_time(&(c->inp),AXI2S_IACNT);
	c->inp.data = NULL;
	if (c->inp.time<start+l) return 0;
	if (start<c->inp.time-c->inp.size) return -1;
	c->inp.data = axi_mem.mem+t2addr(start,&(c->inp));
	return l;
}

int axi_put(axi_dma_t *c)
{
	uint32_t s;
	uint64_t start = c->out.start;
	uint32_t l = c->out.length;
	load_time(&(c->out),AXI2S_OACNT);
	if( c->out.time > start ) return -1;
	if (c->out.time+c->out.size<start+l) return 0;
	s = t2addr(start,&(c->out));
	if( s+l>c->out.base+c->out.size) return -2;
	memcpy(axi_mem.mem+s,c->out.data,l);
	return l;		
}

void axi_now( axi_dma_t *c )
{
	load_time(&(c->inp),AXI2S_IACNT);
	load_time(&(c->out),AXI2S_OACNT);
}

int axi_base(void)
{
	return AXIMEM_BASE;
}