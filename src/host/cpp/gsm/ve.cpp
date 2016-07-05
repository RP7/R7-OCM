#include "gr_complex.h"
#include "vd.h"
#include <inttypes.h> //uint32_t,uint64_t
#include <stdio.h>
#define BURST_SIZE 148
extern "C"
{
typedef struct burst_s {
  int bl;
  float osr;
  short *recv;
  gr_complex frame[1500];
  gr_complex chn[6*10];
  gr_complex rh[3];
  int cut_pos;
  float chpower;
  gr_complex mafi[148];
  int demodulated[148];
  int msg[148];
  int stolen[2];
} burst_t;
typedef struct sch_s {
  burst_t *sb;
  unsigned char in_buf[78];
  unsigned char outbuf[35];
  uint64_t out[2];
} sch_t;

typedef struct cch_s {
  burst_t *nb[4];
  unsigned char in_buf[1024];
  unsigned char outbuf[1024];
  uint64_t out[4];
} cch_t;

typedef struct training_s {
  gr_complex sb[64];
  gr_complex nb[9][26];
  int sb_chn_s;
  int sb_chn_e;
  int nb_chn_s;
  int nb_chn_e;
} training_t;

static void build_t(gr_complex restore[2][8], gr_complex *rhh)
{
  int i;
  restore[0][0] =    gr_complex(0,-1)*(rhh[0]+rhh[2])-rhh[1]; // -j,-1,-j
  restore[0][1] =    gr_complex(0,1)*(rhh[2]-rhh[0])-rhh[1]; // -j,-1,+j
  restore[0][2] =    gr_complex(0,-1)*(rhh[0]+rhh[2])+rhh[1]; // -j,+1,-j
  restore[0][3] =    gr_complex(0,1)*(rhh[2]-rhh[0])+rhh[1]; // -j,+1,+j
  restore[1][0] = (-rhh[0]-rhh[2])-gr_complex(0,1)*rhh[1]; // -1,-j,-1
  restore[1][1] = (+rhh[2]-rhh[1])-gr_complex(0,1)*rhh[1]; // -1,-j,+1
  restore[1][2] = (-rhh[0]-rhh[2])+gr_complex(0,1)*rhh[1]; // -1,+j,-1
  restore[1][3] = (+rhh[2]-rhh[1])+gr_complex(0,1)*rhh[1]; // -1,+j,+1
  for(i=4;i<8;i++) {
    restore[0][i] = -restore[0][i^0x7];
    restore[1][i] = -restore[1][i^0x7];
  }
}

void matchFilter( 
    gr_complex *d
  , gr_complex *h
  , int len
  , int lenh
  , gr_complex *output
  , float osr
  , float timing 
  ) 
{
  int k,i;
  for( k=0;k<len;k++ ) {
    float s = (float)k*osr+timing;
    int   p = (int)s;
    float f = s-p;
    output[k]= gr_complex(0.,0.);
    for( i=0;i<lenh;i++ ) {
      output[k] += (d[p+i]*gr_complex(1.0-f,0)+d[p+i+1]*gr_complex(f,0))*conj(h[i]);
    }
  }
}

static inline float norm22(gr_complex x) 
{
  return x.real()*x.real()+x.imag()*x.imag();
}

static inline float norm2(gr_complex a,gr_complex b) 
{
  return norm22(a-b);
}


int maxwin(gr_complex *d,int dl,int l, float& max)
{
  float pd[dl],s=0.;
  int inx=0;
  int i;
  for(i=0;i<dl;i++) {
    s += norm22(d[i]);
    pd[i]=s;
  }
  max=0.;
  for(i=0;i<dl-l;i++) {
    float s = pd[i+l]-pd[i];
    if(s>max) {
      max = s;
      inx = i;
    }
  }
  return inx;
}

void channelEst(
    gr_complex *frame
  , gr_complex *training
  , int fl
  , int tl
  , float osr
  , int ol
  , gr_complex *output
  )
{
  int oi,i,j;
  for( oi=0;oi<ol;oi++ ) {
    output[oi] = gr_complex(0.,0.);
    float p = (float)oi;
    for( i=0;i<tl;i++ ) {
      output[oi] += frame[int(p)]*conj(training[i]);
      p+=osr;
    }
  }
}

#define update(s0,s1,p0,p1,su) \
      pm_candidate0 = o[s0] + norm(input[sample_nr]-restore[r_i][p0]); \
      pm_candidate1 = o[s1] + norm(input[sample_nr]-restore[r_i][p1]); \
      if(pm_candidate0 < pm_candidate1){ \
          n[su] = pm_candidate0; \
          tracback[sample_nr][su] = 0; \
      } \
      else{ \
          n[su] = pm_candidate1; \
          tracback[sample_nr][su] = 1; \
      } \

void viterbi_detector(const gr_complex * input
	, unsigned int samples_num
	, gr_complex * rhh
	, unsigned int start_state
	, const unsigned int * stop_states
	, unsigned int stops_num
	, int * output
  )
{
	gr_complex restore[2][8];
	float M0[4],M1[4];
	float *n,*o,*tmp;
	int i,j;
	int r_i;
	int sample_nr;
	int tracback[BURST_SIZE][4];
	float pm_candidate0,pm_candidate1;
	gr_complex x;
	for(i=0;i<4;i++){
		M0[i]=1e30;
	}
	M0[start_state]=0.;
	build_t(restore,rhh);
  
  sample_nr=0;
  o=M0;
  n=M1;
  r_i = 1;
  while(sample_nr<samples_num) {
    update(0,2,0,4,0);
    update(0,2,1,5,1);
    update(1,3,2,6,2);
    update(1,3,3,7,3);
    r_i = !r_i;
    tmp = o;
    o = n;
    n = tmp;
    sample_nr++;
  }
  unsigned int best_stop_state;
  float stop_state_metric, min_stop_state_metric;
  best_stop_state = stop_states[0];
  min_stop_state_metric = o[best_stop_state];
  for(i=1; i< stops_num; i++){
    stop_state_metric = o[stop_states[i]];
    if(stop_state_metric < min_stop_state_metric){
      min_stop_state_metric = stop_state_metric;
      best_stop_state = stop_states[i];
    }
  }
  sample_nr=samples_num;
  unsigned int state_nr=best_stop_state;
  unsigned int decision;
   
  while(sample_nr>0) {
    sample_nr--;
    decision = tracback[sample_nr][state_nr];
    output[sample_nr]=decision;
    state_nr += 4*decision;
    state_nr >>= 1;
  }
}

void viterbi_restore(int * input
  , unsigned int samples_num
  , gr_complex * rhh
  , unsigned int start_state
  , int r_i
  , gr_complex * output
  )
{
  gr_complex restore[2][8];
  build_t(restore,rhh);
  int sample_nr;
  int state = start_state;
  sample_nr=0;
  while(sample_nr<samples_num){
    state *= 2;
    state += input[sample_nr];
    state &= 0x7;
    output[sample_nr] = restore[r_i][state];
    sample_nr++;
    r_i = !r_i;
  }
}

void s2c(burst_t *b)
{
  float *p = (float *)&(b->frame);
  int i;
  for(i=0;i<b->bl*2;i++) {
    *p =(float)b->recv[i];
    p++;
  }
}
void scale_vec(gr_complex *x, int l, float c)
{
  int i;
  float *p;
  p = (float*)x;
  for(i=0;i<l*2;i++) {
    *p /= c;
    p++;
  }
}

void scale(burst_t *b)
{
  float s = b->rh[1].real();
  int i;
  float *p;
  p = (float*)&b->rh;
  for(i=0;i<6;i++) {
    *p /= s;
    p++;
  }
  p = (float*)&b->mafi;
  for(i=0;i<148*2;i++) {
    *p /= s;
    p++;
  }
}

void dediff_forward(int *msg, int len, int r_i, int s, int *output)
{
  int i;
  output[0] = s;
  r_i = !r_i;
  for(i=0;i<len-1;i++) {
    int k = msg[i]^msg[i+1]^r_i;
    s ^= k;
    output[i+1]=s;
    r_i = !r_i;
  }
}
void demodu_core(burst_t *b, training_t *tr, int _chn_s, int trlen, int msg0len)
{
  float max;
  int cut_pos = maxwin(b->chn,60,int(b->osr*2),max);
  b->chpower = max;
  float bs,timing;
  int ibs;
  if( cut_pos>b->osr ) {
    bs = float(cut_pos)-b->osr;
    ibs = (int)bs;
    timing = bs-ibs;
    matchFilter(b->chn+ibs,b->chn+cut_pos, 2, int(b->osr*2), b->rh, b->osr, timing);
    b->rh[2] = conj(b->rh[0]);
  }
  else {
    matchFilter(b->chn+cut_pos,b->chn+cut_pos, 2, int(b->osr*2), b->rh+1, b->osr, 0.);
    b->rh[0] = conj(b->rh[2]);
  }
  scale_vec(b->rh,3,(float)trlen);
  bs = float(cut_pos+_chn_s)-(b->osr)*(float)msg0len;
  ibs = (int)bs;
  timing = bs-ibs;
  matchFilter(b->frame+ibs,b->chn+cut_pos, 148, int(b->osr*2), b->mafi, b->osr, timing);
  scale(b);
  unsigned int stop_states[2] = {1,2};
  viterbi_detector(b->mafi, 148, b->rh, 2, stop_states, 2, b->demodulated );
  dediff_forward(b->demodulated+1, 147, 0, 0, b->msg+1);
}

void demodu_sb(burst_t *b, training_t *tr)
{
  gr_complex *start = b->frame+tr->sb_chn_s;
  channelEst( start, tr->sb, (int)((64+4)*b->osr), 64, b->osr, 60, b->chn );
  demodu_core(b,tr,tr->sb_chn_s,64,42);
  for(int i=0;i<39;i++)
    b->msg[i]=b->msg[i+4];
  for(int i=0;i<39;i++)
    b->msg[39+i]=b->msg[39+4+64+i];
  
}

void demodu_nb(burst_t *b, training_t *tr, int type)
{
  gr_complex *start = b->frame+tr->nb_chn_s;
  channelEst( start, tr->nb[type], (int)((26+4)*b->osr), 26, b->osr, 60, b->chn );
  demodu_core(b,tr,tr->nb_chn_s,26,61);
  
  for(int i=0;i<57;i++)
    b->msg[i]=b->msg[i+4];
  b->stolen[0]=b->msg[57+4];
  b->stolen[0]=b->msg[57+4+1+26];
  for(int i=0;i<57;i++)
    b->msg[57+i]=b->msg[57+4+1+26+1+i];
}

void demodu(burst_t *b, training_t *traingings, int type)
{
  s2c(b);
  if(type==0) { // SB 
    demodu_sb(b,traingings);
  }
  else { // NB
    demodu_nb(b,traingings,type-1);
  }
}
int doSch(sch_t *b, training_t *traingings, CC_t *h, int type)
{
  demodu(b->sb,traingings,type);
  for( int i=0;i<h->ins*2;i++ ) {
    b->in_buf[i]=b->sb->msg[i];
    printf("%d",(int)b->in_buf[i]);
  }
  printf("\n");
  int error = conv_decode(h,b->in_buf,b->outbuf);
  printf("Error %d\n",error);
  for( int i=0;i<h->bs;i++ ) {
    printf("%d",(int)b->outbuf[i]);
  }
  printf("\n");
  compress_bits(b->outbuf,35,b->out);
  printf("msg = %lx \n",b->out[0]);
  
  return parity_check(h,b->out);
}
void cch_deinterleave(cch_t *b, CC_t *t)
{
  int i,j,k;
  for(i=0;i<57*8;i++) {
    j = t->ilT[i];
    b->in_buf[i] = (unsigned char)b->nb[j/114]->msg[j%114];
  }
  // for(i=0;i<57*8;i++)
  //   printf("%d,",(int)b->in_buf[i]);
  // printf("\n");
}
int doCch(cch_t *b, training_t *traingings, CC_t *h, int type)
{
  int i;
  for(i=0;i<4;i++)
    demodu(b->nb[i],traingings,type);
  cch_deinterleave(b,h);
  int error = conv_decode(h,b->in_buf,b->outbuf);
  // printf("Error %d\n",error);
  // for( int i=0;i<h->bs;i++ ) {
  //   printf("%d",(int)b->outbuf[i]);
  // }
  // printf("\n");
  compress_bits(b->outbuf,h->bs+h->ps,b->out);
  // printf("msg = %lx \n",b->out[0]);
  
  return parity_check(h,b->out);
}
} //extern "C"