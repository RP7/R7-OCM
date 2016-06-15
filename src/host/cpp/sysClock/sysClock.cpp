#include <sysClock.h>
#include <stdio.h>

typedef struct { unsigned long t[2]; } timing;
#define timing_now(x) asm volatile(".byte 15;.byte 49" : "=a"((x)->t[0]),"=d"((x)->t[1]))
int64_t sysClock::getCpu()
{
  timing now;
  timing_now(&now);
  return (int64_t)now.t[0]+4294967296LL*(int64_t)now.t[1];
}

int sysClock::update( int64_t t, int64_t c )
{
	return 0;
}
void sysClock::dump()
{
	printf("cpu now :%lx ",getCpu());
	printf("rate:%d,a=%20.18lf,to=%lx,co=%lx\n",clk->rate,clk->a,clk->to,clk->co);
}
