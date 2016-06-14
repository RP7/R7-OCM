#include <stdio.h>

#include "Q7Mem.h"
#include "Q7MemAPI.h"


int main( int argc, char *argv[] )
{
  int blk = 75;
  int cp = 1;
  if( argc== 3 )
  {
    int l,c;
    sscanf(argv[1],"%d",&l);
    sscanf(argv[2],"%d",&c);
    if( (l%4096)!=0 )
      printf(" length must = N*4096\n");
    blk = (l+4095)/4096;
    cp = (c+4095)/4096;
  }
  initQ7Mem("tx_udp.d", blk, cp);
  initQ7Mem("rx_udp.d", blk, cp);
  Q7Mem *tx_mem = attachQ7Mem( "tx_udp.d" );
  dumpQ7Mem( tx_mem );
  Q7Mem *rx_mem = attachQ7Mem( "rx_udp.d" );
  dumpQ7Mem( rx_mem );
}
