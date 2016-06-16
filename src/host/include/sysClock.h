#ifndef __SYSCLOCK_H
#define __SYSCLOCK_H

#include <inttypes.h> //uint32_t,uint64_t
typedef struct sysClock_s {
	double a;
	int64_t to;
	int64_t co;
	double refa;
	int rate;
} sysClock_t;
class sysClock {
 // time=(cpu_clock)*a+to
private:
	sysClock_t *clk;
public:
	void attach( sysClock_t *pc ) { clk = pc; };
	sysClock() { clk=0; };
	sysClock( sysClock_t *pc ) { clk = pc; pc->a = 1.; pc->to = 0; pc->co=0; pc->refa = 1.; pc->rate = 0; };
	void setRef( double r) { clk->refa = r; };
	void reset() { clk->rate = 0; };
	int rate() { return clk->rate; };
	int64_t getCpu();
	int64_t cpu( int64_t t)  { return (int64_t)(((double)t-(double)clk->to)/clk->a+0.5)+clk->co; };
	int64_t chip( int64_t c) { return (int64_t)((double)(c-clk->co)*clk->a+0.5)+clk->to; };
	int64_t now() { return chip(getCpu()); };
	int update( int64_t t, int64_t c );
	void dump();
};
#endif //__SYSCLOCK_H
