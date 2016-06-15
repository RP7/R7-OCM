#include <stdio.h>

#include "Q7Mem.h"
#include "Q7MemAPI.h"


int main()
{
  Q7Mem *tx_mem = attachQ7Mem( "tx_udp.d" );
  dumpQ7Mem( tx_mem );
  Q7Mem *rx_mem = attachQ7Mem( "rx_udp.d" );
  dumpQ7Mem( rx_mem );
}
