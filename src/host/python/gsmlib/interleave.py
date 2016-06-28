import numpy as np
class interleave:
	def __init__(self,size,block_size):
		
		"""
		int
		interleave_init(INTERLEAVE_CTX *ictx, int size, int block_size)
		{
			ictx->trans_size = size;
			ictx->trans = (unsigned short *)malloc(size * sizeof *ictx->trans);

		//	DEBUGF("size: %d\n", size);
		//	DEBUGF("Block size: %d\n", block_size);
			int j, k, B;
			for (k = 0; k < size; k++)
			{
				B = k % 4;
				j = 2 * ((49 * k) % 57) + ((k % 8) / 4);
				ictx->trans[k] = B * block_size + j;
				/* Mapping: pos1 goes to pos2: pos1 -> pos2 */
		//		DEBUGF("%d -> %d\n", ictx->trans[k], k);
			}
		//	exit(0);
			return 0;
		}

		"""

		self.trans = np.zeros(size,dtype=int)
		for k in range(size):
			B = k%4
			j = 2*((49*k)%57) + ((k%8)/4)
			self.trans[k] = B*block_size+j

	def decode(self,msg_in):
		return msg_in[self.trans]
