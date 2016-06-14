#include <inttypes.h> //uint32_t,uint64_t

class clock {
 // time=(cpu_clock-co)*a+to
private:
	double a;
	int64_t co;
	int64_t to;
	double refa;
	int rate;
public:
	clock( double r ) { a = 1.; co = getCpu(); to = 0; refa = r; rate = 0; };
	setRef( double r) { refa = r };
	int64_t getCpu();
	int64_t cpu( int64_t t)  { return (int64_t)(((double)t-(double)to)/a+0.5)+co; };
	int64_t chip( int64_t c) { return (int64_t)(((double)c-(double)co)*a+0.5)+to; };
	int64_t now() { return chip(getCpu()); };
	int update( int64_t t, int64_t c ); 
};
