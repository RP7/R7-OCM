from fractions import Fraction
from SB import SB
from CH import CH
from config import *
from GSM import *
import numpy as np
class SCH(CH):
	__burst__ = SB
	"""
	static const unsigned int encode[1 << (K - 1)][2] = {
	  {0, 3}, {3, 0}, {3, 0}, {0, 3},
	  {0, 3}, {3, 0}, {3, 0}, {0, 3},
	  {1, 2}, {2, 1}, {2, 1}, {1, 2},
	  {1, 2}, {2, 1}, {2, 1}, {1, 2}
	};
	"""
	encode = [
	  [0, 3], [3, 0], [3, 0], [0, 3],
	  [0, 3], [3, 0], [3, 0], [0, 3],
	  [1, 2], [2, 1], [2, 1], [1, 2],
	  [1, 2], [2, 1], [2, 1], [1, 2]
	]
	"""
	static const unsigned int next_state[1 << (K - 1)][2] = {
	  {0, 8}, {0, 8}, {1, 9}, {1, 9},
	  {2, 10}, {2, 10}, {3, 11}, {3, 11},
	  {4, 12}, {4, 12}, {5, 13}, {5, 13},
	  {6, 14}, {6, 14}, {7, 15}, {7, 15}
	};
	"""
	next_state = [
	  [0,  8], [0,  8], [1,  9], [1,  9],
	  [2, 10], [2, 10], [3, 11], [3, 11],
	  [4, 12], [4, 12], [5, 13], [5, 13],
	  [6, 14], [6, 14], [7, 15], [7, 15]
	]
	"""
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
	"""
	prev_next_state = [
	  [ 0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2,  2,  2,  2,  2],
	  [ 0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2,  2,  2,  2,  2],
	  [ 2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2,  2,  2,  2],
	  [ 2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2,  2,  2,  2],
	  [ 2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2,  2,  2],
	  [ 2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2,  2,  2],
	  [ 2,  2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2,  2],
	  [ 2,  2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2,  2],
	  [ 2,  2,  2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2],
	  [ 2,  2,  2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2],
	  [ 2,  2,  2,  2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2],
	  [ 2,  2,  2,  2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2,  2],
	  [ 2,  2,  2,  2,  2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2],
	  [ 2,  2,  2,  2,  2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1,  2],
	  [ 2,  2,  2,  2,  2,  2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1],
	  [ 2,  2,  2,  2,  2,  2,  2,  0,  2,  2,  2,  2,  2,  2,  2,  1]
	]
	"""
	static const unsigned char parity_polynomial[PARITY_SIZE + 1] = {
	  1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1
	};

	static const unsigned char parity_remainder[PARITY_SIZE] = {
	  1, 1, 1, 1, 1, 1, 1, 1, 1, 1
	};
	"""
	parity_polynomial = np.array([1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1])
	parity_remainder = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
	DATA_BLOCK_SIZE    = 25
	PARITY_SIZE        = 10
	TAIL_BITS_SIZE     = 4
	PARITY_OUTPUT_SIZE = (DATA_BLOCK_SIZE + PARITY_SIZE + TAIL_BITS_SIZE)
	CONV_INPUT_SIZE    = PARITY_OUTPUT_SIZE
	CONV_SIZE          = (2 * CONV_INPUT_SIZE)
	K                  = 5
	MAX_ERROR          = (2 * CONV_INPUT_SIZE + 1)
	"""
	  ncc =
	    (decoded_data[ 7] << 2)  |
	    (decoded_data[ 6] << 1)  |
	    (decoded_data[ 5] << 0);
	  bcc = 
	    (decoded_data[ 4] << 2)  |
	    (decoded_data[ 3] << 1)  |
	    (decoded_data[ 2] << 0);
	  t1 =
	    (decoded_data[ 1] << 10) |
	    (decoded_data[ 0] << 9)  |
	    (decoded_data[15] << 8)  |
	    (decoded_data[14] << 7)  |
	    (decoded_data[13] << 6)  |
	    (decoded_data[12] << 5)  |
	    (decoded_data[11] << 4)  |
	    (decoded_data[10] << 3)  |
	    (decoded_data[ 9] << 2)  |
	    (decoded_data[ 8] << 1)  |
	    (decoded_data[23] << 0);
	  t2 =
	    (decoded_data[22] << 4)  |
	    (decoded_data[21] << 3)  |
	    (decoded_data[20] << 2)  |
	    (decoded_data[19] << 1)  |
	    (decoded_data[18] << 0);
	  t3p =
	    (decoded_data[17] << 2)  |
	    (decoded_data[16] << 1)  |
	    (decoded_data[24] << 0);

	  t3 = 10 * t3p + 1;
	"""
	_fields_ = {"ncc":[7,6,5],"bcc":[4,3,2],"t1":[1,0,15,14,13,12,11,10,9,8,23],"t2":[22,21,20,19,18],"t3p":[17,16,24]}
	def __init__(self):
		CH.__init__(self)
		self.hit = {}
		self.osr = float(SampleRate/SymbolRate)
		self.ovL = int(SB.overheadL()*self.osr)
		self.ovS = int(SB.overheadS()*self.osr)
	def callback(self,b,fn,state):
		if state.timingSyncState.state==1:
			p = b.peekL()
			pos = p.argmax()-self.ovL
		elif state.timingSyncState.state==2:
			p = b.peekS()
			pos = p.argmax()

			b.setChEst()
			b.viterbi_detector()
			self.msg = b.sbm0[3:]+b.sbm1[:-3]
			self.decoded_data = self.conv_decode()
			self.decode()
			if self.parity_check()!=0:
				print "fn",b.fn,"sn",b.sn,"error",self.last_error
			else:
				state.bcc = self.info['bcc']
			pos -= self.ovS

			
		if pos in self.hit:
			self.hit[pos] += 1
		else:
			self.hit[pos] = 1
		return 1,p

	def frameStart(self):
		p = 0
		h = 0
		for pos in self.hit:
			if self.hit[pos]>h:
				h=self.hit[pos]
				p = pos
		r = 0

		for x in range(p-2,p+3):
			if x in self.hit:
				r += self.hit[x]

		self.hit = {}
		return p,r


	"""
static int conv_decode(unsigned char *data, unsigned char *output)
{

  int i, t;
  unsigned int rdata, state, nstate, b, o, distance, accumulated_error,
  min_state, min_error, cur_state;

  unsigned int ae[1 << (K - 1)];
  unsigned int nae[1 << (K - 1)]; // next accumulated error
  unsigned int state_history[1 << (K - 1)][CONV_INPUT_SIZE + 1];

  // initialize accumulated error, assume starting state is 0
  for (i = 0; i < (1 << (K - 1)); i++)
    ae[i] = nae[i] = MAX_ERROR;
  ae[0] = 0;

  // build trellis
  for (t = 0; t < CONV_INPUT_SIZE; t++) {

    // get received data symbol
    rdata = (data[2 * t] << 1) | data[2 * t + 1];

    // for each state
    for (state = 0; state < (1 << (K - 1)); state++) {

      // make sure this state is possible
      if (ae[state] >= MAX_ERROR)
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
      nae[i] = MAX_ERROR;
    }
  }
    // the final state is the state with the fewest errors
  min_state = (unsigned int) - 1;
  min_error = MAX_ERROR;
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
	"""
	def conv_decode(self):
		data = self.msg
		ae = np.ones((1 << (SCH.K - 1)),dtype=int)*SCH.MAX_ERROR
		nae = np.ones((1 << (SCH.K - 1)),dtype=int)*SCH.MAX_ERROR
		state_history = np.zeros((1 << (SCH.K - 1),SCH.CONV_INPUT_SIZE + 1),dtype=int)
		ae[0] = 0
		for t in range(SCH.CONV_INPUT_SIZE):
			rdata = (data[2 * t] << 1) | data[2 * t + 1]
			for state in range(1<<(SCH.K-1)):
				if ae[state]>=SCH.MAX_ERROR:
					continue
				for b in range(2):
					nstate = SCH.next_state[state][b]
					o = SCH.encode[state][b]
					distance = self.hamming_distance2(rdata^o)
					accumulated_error = ae[state] + distance
					if accumulated_error < nae[nstate]:
						nae[nstate] = accumulated_error
						state_history[nstate,t + 1] = state
			ae[:] = nae[:]
			nae[:] = SCH.MAX_ERROR
		min_state = -1
		min_error = SCH.MAX_ERROR
		for i in range(1 << (SCH.K - 1)):
			if ae[i] < min_error:
				min_state = i
				min_error = ae[i]
		#print "erros",min_error
		cur_state = min_state
		output = np.zeros(SCH.CONV_INPUT_SIZE,dtype=int)
		for t in range(SCH.CONV_INPUT_SIZE,0,-1):
			min_state = cur_state
			cur_state = state_history[cur_state,t]
			output[t-1] = SCH.prev_next_state[cur_state][min_state]
		self.last_error = min_error
		return output

	def hamming_distance2(self,d):
		return d&1+((d&2)>>1)


	"""
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

	"""

	def parity_check(self):
		buf = []
		buf = np.array(self.decoded_data[:SCH.DATA_BLOCK_SIZE + SCH.PARITY_SIZE])
		for i in range(SCH.DATA_BLOCK_SIZE):
			if buf[i]==1:
				buf[i:i+SCH.PARITY_SIZE+1]^=SCH.parity_polynomial
		#print buf[:]
		return np.sum(buf[SCH.DATA_BLOCK_SIZE:SCH.DATA_BLOCK_SIZE+SCH.PARITY_SIZE]^SCH.parity_remainder)

	def decode(self):
		self.info = {}
		for d in SCH._fields_:
			l = SCH._fields_[d]
			m = 0
			for p in l:
				m *= 2
				m += self.decoded_data[p]
			self.info[d]=m
		self.info['t3']=self.info['t3p']*10+1
		return self.info
