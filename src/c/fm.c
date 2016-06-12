#include <inttypes.h> //uint32_t,uint64_t
#include <math.h>
#include <stdio.h>

typedef struct fm_s {
	int16_t *buf;
	int16_t *result;
	int os1;
	int os2;
	int len;
	int atan_lut[131072];
	int16_t pre[2];
} fm_t;

static int atan_lut_size = 131072; /* 512 KB */
static int atan_lut_coef = 8;

int fm_init( fm_t *c )
{
	int i = 0;

	for (i = 0; i < atan_lut_size; i++) {
		c->atan_lut[i] = (int) (atan((double) i / (1<<atan_lut_coef)) / 3.14159 * (1<<14));
	}

	return 0;
}

inline void multiply_c(int16_t *a, int16_t *b, int *cr, int *cj)
{

	int ar,aj,br,bj;
	ar = (int)a[0];
	aj = (int)a[1];
	br = (int)b[0];
	bj = (int)b[1];
	*cr = ar*br + aj*bj;
	*cj = aj*br - ar*bj;
}

int polar_disc_lut( fm_t *c,int16_t *a, int16_t *b)
{
	int cr, cj, x, x_abs;

	multiply_c(a,b, &cr, &cj);

	/* special cases */
	if (cr == 0 || cj == 0) {
		if (cr == 0 && cj == 0)
			{return 0;}
		if (cr == 0 && cj > 0)
			{return 1 << 13;}
		if (cr == 0 && cj < 0)
			{return -(1 << 13);}
		if (cj == 0 && cr > 0)
			{return 0;}
		if (cj == 0 && cr < 0)
			{return 1 << 14;}
	}

	/* real range -32768 - 32768 use 64x range -> absolute maximum: 2097152 */
	x = (cj << atan_lut_coef) / cr;
	x_abs = abs(x);

	if (x_abs >= atan_lut_size) {
		/* we can use linear range, but it is not necessary */
		return (cj > 0) ? 1<<13 : -1<<13;
	}

	if (x > 0) {
		return (cj > 0) ? c->atan_lut[x] : c->atan_lut[x] - (1<<14);
	} else {
		return (cj > 0) ? (1<<14) - c->atan_lut[-x] : -c->atan_lut[-x];
	}

	return 0;
}

int fm_demod(fm_t *c)
{
	int i, pcm, k, o;
	int16_t *lp = c->buf;
	int16_t *pre  = c->pre;
	int32_t *ipre = (int32_t *)c->pre;
	float *output = (float *)c->result;
	float scale = 1./c->os2/8192.;
	int len = (c->len+c->os1*c->os2-1)/(c->os1*c->os2);
	for(i=0;i<len;i++)
	{
		pcm = 0;
		k = c->os2;
		while(k>0)
		{
			pcm += polar_disc_lut(c,lp,pre);
			*ipre = *(int32_t *)lp;
			lp += c->os1*2;
			k--;
		}
		*output = (float)pcm*scale;
		output++;
	}
	return i;
}

