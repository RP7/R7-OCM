#include <inttypes.h> //uint32_t,uint64_t

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

   typedef struct CC_s {
      uint64_t pp;
      uint64_t pr;
      int bs;
      int ps;
      int ts;
      int is;
      int maxE;
   } CC_t;

   """ for sch
   parity_polynomial = np.array([1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1])
   parity_remainder = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
   DATA_BLOCK_SIZE    = 25
   PARITY_SIZE        = 10
   TAIL_BITS_SIZE     = 4
   """
   sch_config = {
        'parity_polynomial' : np.array([1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1])
      , 'parity_remainder'  : np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
      , 'DATA_BLOCK_SIZE'   : 25
      , 'PARITY_SIZE'       : 10
      , 'TAIL_BITS_SIZE'    : 4
   }
   cch_config = {
        'parity_polynomial' : np.array([
          1, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 1, 0,
            0, 1, 0, 0, 0, 0, 0, 1,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 1, 0, 0,
            1
            ])
      , 'parity_remainder'  : np.array([1]*40)
      , 'DATA_BLOCK_SIZE'   : 184
      , 'PARITY_SIZE'       : 40
      , 'TAIL_BITS_SIZE'    : 4
   }
   def __init__(self,config):
      for x in config:
         self.__dict__[x] = config[x]
      self.PARITY_OUTPUT_SIZE = (self.DATA_BLOCK_SIZE + self.PARITY_SIZE + self.TAIL_BITS_SIZE)
      self.CONV_INPUT_SIZE    = self.PARITY_OUTPUT_SIZE
      self.CONV_SIZE          = (2 * self.CONV_INPUT_SIZE)
      self.K                  = 5
      self.h.maxE          = (2 * self.CONV_INPUT_SIZE + 1)
   
   static int hamming_distance2( int d )
   {
      return d&1+((d&2)>>1)
   }
   
   static int parity_check(unsigned char *d)
   {

     unsigned int i;
     unsigned char buf[DATA_BLOCK_SIZE + PARITY_SIZE], *q;

     memcpy(buf, d, DATA_BLOCK_SIZE + PARITY_SIZE);

     for (q = buf; q < buf + DATA_BLOCK_SIZE; q++)
       if (*q)
         for (i = 0; i < PARITY_SIZE + 1; i++)
           q[i] ^= parity_polynomial[i];
     return memcmp(buf + DATA_BLOCK_SIZE, parity_remainder, PARITY_SIZE);
   }

   static int conv_decode( CC_t *h, unsigned char *data, unsigned char *output)
   {

     int i, t;
     unsigned int rdata, state, nstate, b, o, distance, accumulated_error,
     min_state, min_error, cur_state;

     unsigned int ae[1 << (K - 1)];
     unsigned int nae[1 << (K - 1)]; // next accumulated error
     unsigned int state_history[1 << (K - 1)][CONV_INPUT_SIZE + 1];

     // initialize accumulated error, assume starting state is 0
     for (i = 0; i < (1 << (K - 1)); i++)
       ae[i] = nae[i] = h.maxE;
     ae[0] = 0;

     // build trellis
     for (t = 0; t < CONV_INPUT_SIZE; t++) {

       // get received data symbol
       rdata = (data[2 * t] << 1) | data[2 * t + 1];

       // for each state
       for (state = 0; state < (1 << (K - 1)); state++) {

         // make sure this state is possible
         if (ae[state] >= h.maxE)
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
         nae[i] = h.maxE;
       }
     }
       // the final state is the state with the fewest errors
     min_state = (unsigned int) - 1;
     min_error = h.maxE;
     for (i = 0; i < (1 << (K - 1)); i++) {
       if (ae[i] < min_error) {
         min_state = i;
         min_error = ae[i];
       }
     }

     // trace the path
     cur_state = min_state;
     for (t = CONV_INPUT_SIZE; t >= 1; t--) {
       min_state = cur_state;
       cur_state = state_history[cur_state][t]; // get previous
       output[t - 1] = prev_next_state[cur_state][min_state];
     }

     // return the number of errors detected (hard-decision)
     return min_error;
   }

   def compress_bits(self,sbuf):
      dbuf = []
      for i in range(0,len(sbuf),8):
         c = 0
         k = 1
         for x in sbuf[i:i+8]:
            c += k*x
            k *= 2
         dbuf.append(c)
      return dbuf


} // extern "C"
