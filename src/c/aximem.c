#include <inttypes.h> //uint32_t,uint64_t
#include <unistd.h>
#include <stdio.h>
#include <string.h> //memcpy

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/types.h> 

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

int axi_open(axi_dma_t *c)
{
	int flag = 1;
	c->sock.servAddrLen = sizeof(struct sockaddr_in);
	c->sock.sid           = socket(PF_INET, SOCK_DGRAM, 0);
 	setsockopt( c->sock.sid, SOL_SOCKET, SO_REUSEADDR, &flag, sizeof(int));
  bzero(&(c->sock.servaddr), sizeof(c->sock.servaddr));
  bzero(&(c->sock.peeraddr), sizeof(c->sock.peeraddr));
  c->sock.servaddr.sin_family = AF_INET;
  c->sock.servaddr.sin_port = htons(c->sock.port);
  c->sock.servaddr.sin_addr.s_addr = htons(INADDR_ANY);
  bind(c->sock.sid, (struct sockaddr *)&(c->sock.servaddr), sizeof(c->sock.servaddr));
  c->sock.peerAddrLen = 0;
  bzero(&(c->inp.pm),sizeof(pmon_t));
	bzero(&(c->out.pm),sizeof(pmon_t));
}

int axi_close(axi_dma_t *c)
{
  c->sock.send_en = 0;
  c->sock.recv_en = 0;
	close(c->sock.sid);
  bzero(&(c->sock.servaddr), sizeof(c->sock.servaddr));
  bzero(&(c->sock.peeraddr), sizeof(c->sock.peeraddr));
  c->sock.peerAddrLen = 0;
}

int axi_udp_send(axi_dma_t *c,void *sendline, int len)
{
	if(c->sock.peerAddrLen!=0)
	{
		return sendto( c->sock.sid
					, sendline
					, len
					, 0
					, (struct sockaddr *)&(c->sock.peeraddr)
					, c->sock.peerAddrLen
					);
	}
	else
	{
		return -1;
	}
}

int axi_udp_recv( axi_dma_t *c, char *buf, int len )
{
	struct sockaddr_in addr;
	int l = sizeof(addr);
	int r = recvfrom( c->sock.sid
				, buf
				, len
				, 0
				, (struct sockaddr *)&(addr)
				, (socklen_t*)&l 
				);
	if (l!=0)
	{
		c->sock.peerAddrLen=l;
		memcpy(&(c->sock.peeraddr),&addr,sizeof(addr));
	}
	else
		c->out.pm.counter[2]++; // addr error
	return r;
}

int axi_inp_task( axi_dma_t *c, udp_package_t *send )
{
	uint64_t start;
	uint64_t l;
	int r;
	while(c->sock.send_en)
	{
		c->inp.start = c->inp.end;
		start = c->inp.start;
		l = c->inp.length;
		load_time(&(c->inp),AXI2S_IACNT);
		c->inp.data = NULL;
		if (c->inp.time<start+l)
		{
			c->inp.pm.counter[2]++; //data no ready
			if(start+l-c->inp.time > 2*c->inp.size)
				axi_inp_reset(c);
			return 0;
		} 
		if( c->inp.time>c->inp.size )
		{
			if( start < c->inp.time-c->inp.size ) 
			{
				start=(c->inp.time-c->inp.size/2)&(-1024L);
				c->inp.start = start;
				c->inp.end = start;
				c->inp.pm.counter[3]++; //data out of date
				return -1;
			}
		}
		send->header.time = c->inp.time;
		send->header.offset = c->inp.start;
		memcpy(send->data,axi_mem.mem+t2addr(start,&(c->inp)),l);
		r = axi_udp_send(c,(char *)send,sizeof(udp_package_t));
		if(r==sizeof(udp_package_t))
		{
			c->inp.end = start+l;
			c->inp.pm.counter[0]++; // send ok
		}
		else 
		{
			if(r==-1)
			{
				c->inp.pm.counter[1]++; // not peer
				if(c->inp.time>l)
					c->inp.end = (c->inp.time-l)&(-1024L);
				return -2;
			}	
			else
				c->inp.pm.counter[4]++; // send failure
		}	
	}
	return 1;
}

int axi_out_task( axi_dma_t *c, udp_package_t *recv )
{
	uint64_t start;
	uint64_t l;
	uint32_t s;
	uint32_t r;
	while(c->sock.recv_en)
	{
		l = 1024;
		r = axi_udp_recv(c,(char *)recv,sizeof(udp_package_t));
		if(r!=sizeof(udp_package_t)) 
		{
			c->out.pm.counter[4]++; // recv failure
			return -3;
		}
		start = recv->header.offset;
		c->out.start = start;
		load_time(&(c->out),AXI2S_OACNT);
		if( c->out.time > start ) {
			c->out.pm.counter[3]++; // data out of date
			return -1;	
		}
		if (c->out.time+c->out.size<start+l) 
		{
			c->out.pm.counter[1]++; // buffer full
			return 0;
		}
		s = t2addr(start,&(c->out));
		if( s+l>c->out.base+c->out.size ) 
		{
			c->out.pm.counter[5]++; // data aligned error
			return -2;
		}
		memcpy(axi_mem.mem+s,recv->data,1024);
			c->out.pm.counter[0]++; // out ok
	}
	return 1;
}

int axi_get(axi_dma_t *c)
{
	uint64_t start = c->inp.start;
	uint64_t l = (uint64_t)c->inp.length;
	load_time(&(c->inp),AXI2S_IACNT);
	c->inp.data = NULL;
	if ( c->inp.time < start+l ) 
		return 0;
	if ( start < c->inp.time-c->inp.size ) 
		return -1;
	c->inp.data = axi_mem.mem+t2addr(start,&(c->inp));
	return (int)l;
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

int axi_reportPeerIP(axi_dma_t *c)
{
	printf("host -> %s:%hu\n" , inet_ntoa( c->sock.peeraddr.sin_addr ), ntohs(c->sock.peeraddr.sin_port));
	printf("sever-> %s:%hu\n" , inet_ntoa( c->sock.servaddr.sin_addr ), ntohs(c->sock.servaddr.sin_port));
	return 0;
}

int axi_inp_reset(axi_dma_t *c)
{
  int64_t pos;
  load_time(&(c->inp),AXI2S_IACNT);
  pos = (int64_t)c->inp.bcnt*(int64_t)c->inp.size;
  c->inp.start = pos;
  c->inp.end = pos;
}