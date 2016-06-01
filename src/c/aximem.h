typedef struct struct_aximem {
	void *u_mmap;
	void *c_mmap;
} aximem_t;

#define AXIMEM_BASE 0x1e000000
#define AXIMEM_SIZE 0x02000000

#define FPGA_BASE 0x40000000
#define FPGA_SIZE 0x40000

typedef struct struct_axi_entity
{
	uint32_t base;
	uint32_t size;
	uint32_t acnt;
	uint32_t bcnt;
	uint64_t time;
	uint64_t start;
	uint64_t end;
	uint32_t length;
	void *data;
} axi_entity_t;

typedef struct struct_axi_dma
{
	axi_entity_t inp;
	axi_entity_t out;
} axi_dma_t;
