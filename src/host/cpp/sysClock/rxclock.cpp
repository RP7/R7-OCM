#include <sysClock.h>
#include <Q7Mem.h>
#include "Q7MemAPI.h"
#include <inttypes.h> //uint32_t,uint64_t
#include <unistd.h>
#include <math.h>

typedef struct pair_s {
	int64_t c;
	int64_t t;
} pair_t;

static pair_t his[16];
static int current = 0;

void getCurrent( Q7Mem *rx_mem )
{
	his[current].c = rx_mem->head->cpu;
	his[current].t = rx_mem->head->packet.header.offset;
	current ++;
	current &= 0xf;
}

void leastSquare( double *pa, int64_t * pto, int64_t *pco )
{
	int64_t sumc = 0;
	int64_t sumt = 0;
	int i;
	for( i=0;i<16;i++ )
	{
		sumc += his[i].c;
		sumt += his[i].t;
	}
	sumc += 8;
	sumt += 8;
	sumc >>= 4;
	sumt >>= 4;
	double cc = 0.;
	double ct = 0.;
	for( i=0;i<16;i++ )
	{
		double c0 = (double)(his[i].c-sumc);
		cc += c0*c0;
		ct += c0*(double)(his[i].t-sumt);
	}
	if( cc!=0. )
	{
		*pa = ct/cc;
		*pto = sumt;
		*pco = sumc;
	}
}

int clklevel(double newa,double olda)
{
	if(fabs(olda)<1e-5)
		return 0;
	double d = (newa-olda)/olda;
	printf("diff: %le\n",d);
	double dr = -log10(fabs(d))/0.3;
	dr = pow(1.1,dr);
	if( dr>30. )
		dr = 30.;
	return (int)dr;
}

int main(int argc, char*argv[] )
{
  Q7Mem *rx_mem = attachQ7Mem( "rx_udp.d" );
  dumpQ7Mem( rx_mem );

  int i;
  double a;
  int64_t to,co;

  for( i=0;i<16;i++ )
  	getCurrent( rx_mem );
  ;
  rx_mem->head->clk.rate = 0;
  while(1)
  {
  	sleep(rx_mem->head->clk.rate+1);
  	getCurrent( rx_mem );
  	leastSquare( &a, &to, &co );
  	rx_mem->head->clk.rate = clklevel(a,rx_mem->head->clk.a);
  	rx_mem->head->clk.a = a;
  	rx_mem->head->clk.to = to;
  	rx_mem->head->clk.co = co;
  	rx_mem->dumpHead();
  }  
}

