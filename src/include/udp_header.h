#ifndef __UDP_HEADER_H
#define __UDP_HEADER_H
#include <inttypes.h> //uint32_t,uint64_t

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


#endif // __UDP_HEADER_H
