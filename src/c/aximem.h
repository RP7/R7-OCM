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

typedef struct socketInfo
{
	int s;
	int port;
	int send_en;
	int recv_en;
	int servAddrLen;
	int peerAddrLen;
	struct sockaddr_in servaddr;
	struct sockaddr_in peeraddr;
} socket_info_t;

typedef struct struct_axi_dma
{
	axi_entity_t inp;
	axi_entity_t out;
	socket_info_t sock;
} axi_dma_t;

typedef struct udp_header_s
{
	uint64_t time;
	uint64_t offset;
} udp_header_t;

typedef struct udp_package_s
{
	udp_header_t header;
	char data[1024];
} udp_package_t;

