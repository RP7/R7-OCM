#include <inttypes.h> //uint32_t,uint64_t
#include <stdio.h>
#include "vd.h"

#define K 5
extern "C" 
{
   static const unsigned int encode[1 << (K - 1)][2] = {
     {0, 3}, {3, 0}, {3, 0}, {0, 3},
     {0, 3}, {3, 0}, {3, 0}, {0, 3},
     {1, 2}, {2, 1}, {2, 1}, {1, 2},
     {1, 2}, {2, 1}, {2, 1}, {1, 2}
   };
   static const unsigned int next_state[1 << (K - 1)][2] = {
     {0, 8}, {0, 8}, {1, 9}, {1, 9},
     {2, 10}, {2, 10}, {3, 11}, {3, 11},
     {4, 12}, {4, 12}, {5, 13}, {5, 13},
     {6, 14}, {6, 14}, {7, 15}, {7, 15}
   };
   static const unsigned int prev_next_state[1 << (K - 1)][1 << (K - 1)] = {
     { 0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2,  2,  2,  2,  2},
     { 0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2,  2,  2,  2,  2},
     { 2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2,  2,  2,  2},
     { 2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2,  2,  2,  2},
     { 2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2,  2,  2},
     { 2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2,  2,  2},
     { 2,  2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2,  2},
     { 2,  2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2,  2},
     { 2,  2,  2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2},
     { 2,  2,  2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2},
     { 2,  2,  2,  2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2},
     { 2,  2,  2,  2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2},
     { 2,  2,  2,  2,  2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2},
     { 2,  2,  2,  2,  2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2},
     { 2,  2,  2,  2,  2,  2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1},
     { 2,  2,  2,  2,  2,  2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1}
   };


   static int hamming_distance2( int d )
   {
      return d&1+((d&2)>>1);
   }
   
   int parity_check( CC_t *h, uint64_t *d )
   {

      int i,j;
      int pos = 0;
      uint64_t w=d[pos];
      int len = h->bs;
      uint64_t mask = (1LL<<h->ps)-1LL;
      j = 0;
      while(len>0) {
         if( w&1 ) {
            w ^= h->pp;
         }
         w >>= 1;
         j++;
         len--;
         if( j==64 ) {
            pos++;
            w ^= d[pos];
            j=0;
         }
         //printf("%dth step : %lx,(%lx,%lx)\n",j,w,h->pp,h->pr);
      }
      if ((64-j)<h->ps) {
         w ^=(d[pos+1]<<(64-j));
      }
      w &= mask;
      //printf("parity check %lx:(%lx,%lx),%lx,%d\n",w,h->pp,h->pr,d[pos+1],j);
      if(w==h->pr)
         return 0;
      else
         return 1;
   }

   int conv_decode( CC_t *h, unsigned char *data, unsigned char *output )
   {

     int i, t;
     unsigned int rdata, state, nstate, b, o, distance, accumulated_error,
     min_state, min_error, cur_state;

     unsigned int ae[1 << (K - 1)];
     unsigned int nae[1 << (K - 1)]; // next accumulated error
     unsigned int state_history[1 << (K - 1)][h->ins + 1];

     // initialize accumulated error, assume starting state is 0
     for (i = 0; i < (1 << (K - 1)); i++)
       ae[i] = nae[i] = h->maxE;
     ae[0] = 0;

     // build trellis
     for (t = 0; t < h->ins; t++) {

       // get received data symbol
       rdata = (data[2 * t] << 1) | data[2 * t + 1];

       // for each state
       for (state = 0; state < (1 << (K - 1)); state++) {

         // make sure this state is possible
         if (ae[state] >= h->maxE)
           continue;

         // find all states we lead to
         for (b = 0; b < 2; b++) {

           // get next state given input bit b
           nstate = next_state[state][b];

           // find output for this transition
           o = encode[state][b];

           // calculate distance from received data
           distance = hamming_distance2(rdata ^ o);

           // choose surviving path
           accumulated_error = ae[state] + distance;
           if (accumulated_error < nae[nstate]) {

             // save error for surviving state
             nae[nstate] = accumulated_error;

             // update state history
             state_history[nstate][t + 1] = state;
           }
         }
       }

       // get accumulated error ready for next time slice
       for (i = 0; i < (1 << (K - 1)); i++) {
         ae[i] = nae[i];
         nae[i] = h->maxE;
       }
     }
       // the final state is the state with the fewest errors
     min_state = (unsigned int) - 1;
     min_error = h->maxE;
     for (i = 0; i < (1 << (K - 1)); i++) {
       if (ae[i] < min_error) {
         min_state = i;
         min_error = ae[i];
       }
     }

     // trace the path
     cur_state = min_state;
     for (t = h->ins; t >= 1; t--) {
       min_state = cur_state;
       cur_state = state_history[cur_state][t]; // get previous
       output[t - 1] = prev_next_state[cur_state][min_state];
     }

     // return the number of errors detected (hard-decision)
     return min_error;
   }

   int compress_bits( unsigned char *sbuf, int len, uint64_t *output )
   {  
      int i,j;
      uint64_t c,k;
      int pos = 0;
      unsigned char *p = sbuf;
      c = 0;
      k = 1;
      j = 0;
      while(len>0) {
         k = (uint64_t)*p;
         k<<=j;      
         c |= k;
         j++;
         if( j==64 ) {
            output[pos] = c;
            pos++;
            c = 0;
            k = 1;
            j = 0;
         }
         len--;
         p++;
      }
      if(j!=0) {
         output[pos] = c;
         pos++;
      }
      return pos;
   }

} // extern "C"
