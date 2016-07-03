#include "gr_complex.h"
#define BURST_SIZE 148
extern "C"
{

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


int maxwin(gr_complex *d,int dl,int l)
{
  float pd[dl],s=0.,max=0.;
  int inx=0;
  int i;
  for(i=0;i<dl;i++) {
    s += norm22(d[i]);
    pd[i]=s;
  }
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
      //printf("%d ",int(p));
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
} //extern "C"