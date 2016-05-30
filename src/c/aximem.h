typedef struct struct_aximem {
	void *u_mmap;
	void *c_mmap;
} aximem_t;

#define AXIMEM_BASE 0x1e000000
#define AXIMEM_SIZE 0x02000000

#define FPGA_BASE 0x40000000
#define FPGA_SIZE 0x40000

