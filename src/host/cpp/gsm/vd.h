#ifndef __VD_H
#define __VD_H
#include <inttypes.h> //uint32_t,uint64_t

typedef struct CC_s {
      uint64_t pp;
      uint64_t pr;
      int bs;
      int ps;
      int ts;
      int ins;
      int maxE;
      int ilT[57*8];
} CC_t;
extern "C"
{
	int conv_decode( CC_t *h, unsigned char *data, unsigned char *output );
	int parity_check( CC_t *h, uint64_t *d );
	int compress_bits( unsigned char *sbuf, int len, uint64_t *output);
}   
#endif //__VD_H 