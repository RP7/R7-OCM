import AD9361_c
import sys

def rx_freq(f):
	ad = AD9361_c.AD9361_c()
	ad.Set_Rx_freq(25e6,f)
	ad.deinit()
	
def main():
	if len(sys.argv)>1:
		if sys.argv[1]=='Rx_f':
			rx_freq(float(sys.argv[2]))

if __name__ == '__main__':
	main()