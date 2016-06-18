import numpy as np

class Burst:
	slot = 625
	def __init__(self):
		pass
	def diff(self,s):
		r = []
		for i in range(len(s)-4):
			a = s[i+4]*np.conj(s[i])
			r.append(a.imag)
		return r

	def gmsk_mapper( self, inp, start_point ):
		"""
		//TODO consider placing this funtion in a separate class for signal processing
void gsm_receiver_cf::gmsk_mapper(const unsigned char * input, int nitems, gr_complex * gmsk_output, gr_complex start_point)
{
  gr_complex j = gr_complex(0.0, 1.0);

  int current_symbol;
  int encoded_symbol;
  int previous_symbol = 2 * input[0] - 1;
  gmsk_output[0] = start_point;

  for (int i = 1; i < nitems; i++) {
    //change bits representation to NRZ
    current_symbol = 2 * input[i] - 1;
    //differentially encode
    encoded_symbol = current_symbol * previous_symbol;
    //and do gmsk mapping
    gmsk_output[i] = j * gr_complex(encoded_symbol, 0.0) * gmsk_output[i-1];
    previous_symbol = current_symbol;
  }
}
		"""
		o = start_point
		out = []
		previous_symbol = inp[0]
		for current_symbol in inp[1:]:
			encoded_symbol = current_symbol * previous_symbol
			o = complex(0,1)*encoded_symbol*o
			#print "o",o
			out.append(o)
			previous_symbol = current_symbol
			
		return np.array(out)

	def channelEst( self, frame, training, osr ):
		inx = np.floor(np.arange(len(training))*osr)
		last = int(inx[-1]+1)
		#print len(frame)-last
		out = np.zeros(len(frame)-last,dtype=complex)
		for k in range(len(out)):
			slc = frame[k:]
			s = slc[inx.astype(int)]
			r = np.dot(s,training)
			out[k] = r
		return out
