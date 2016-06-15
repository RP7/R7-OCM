typedef struct { unsigned long t[2]; } timing;
#define timing_now(x) asm volatile(".byte 15;.byte 49" : "=a"((x)->t[0]),"=d"((x)->t[1]))
int64_t clock::getCpu()
{
  timing now;
  timing_now(&now);
  return (int64_t)now.t[0]+4294967296LL*(int64_t)now.t[1];
}

int clock::update( int64_t t, int64_t c )
{
	if( c+1000000L<co )
		return -1;
	double dt = (double)(t-to);
	double dc = (double)(c-co);

	double r = dt/dc;
	double newrate = r/(r-a);
	newrate = newrate:-newrate?newrate>0;
	if( dt>newrate*100000. )
	{
		to = t;
		co = c;
		a = r;
		return 1;
	}
	return 0;
}