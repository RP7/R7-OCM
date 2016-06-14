#include <stdio.h>

#include "Q7Mem.h"
#include "Q7MemAPI.h"

#include "easySocket.h"

static udp_package_t sendBuf;
static udp_package_t recvBuf;
  

int main(int argc, char*argv[] )
{
  Q7Mem *tx_mem = attachQ7Mem( "tx_udp.d" );
  dumpQ7Mem( tx_mem );
  Q7Mem *rx_mem = attachQ7Mem( "rx_udp.d" );
  dumpQ7Mem( rx_mem );
  int port;
  sscanf( argv[2],"%d",&port );
  printf("port %d,sizeof int %d\n",port, sizeof(int));
  udpClient udp( argv[1], port );
  sendBuf.header.time = 0;
  sendBuf.header.offset = 0;
  udp.send( (char *)sendBuf, sizeof(sendBuf) );
  int len = 0;
  unsigned int last_send;
  while( (len=udp.recv( (char*)recvBuf, sizeof(recvBuf) )) == sizeof(recvBuf) )
  {
    memcpy(&(rx_mem.head.ph),&(recvBuf.header),sizeof(udp_package_t));
    
    long long from = (long long)recvBuf.header.offset;
    if( from != rx_mem._off )
    {
      printf("recv discontinued _off:%llx, off:%llx",rx_mem._off,from);
      rx_mem._off = from;
    }
    int *p = (int *)rx_mem->_getBuf( from, 1024 );
    memcpy( p, &(recvBuf.data), 1024 );
      unsigned int free = recvBuf[3] - 2;
      if((free-last_send)<60)
      {
        for( unsigned int x=last_send;x<free;x++ )
        {
          from = x * 300 * 4;
          p = (int *)tx_mem->_getBuf( from, 1200 );
          sendBuf[0] = 0x7f7f7f7f;
          sendBuf[1] = 1200;
          sendBuf[2] = x;
          sendBuf[3] = 0;
          memcpy( &sendBuf[4], p, 1200 );
          len = udp.send( (char *)sendBuf, 1216 );
          if( len!=1216 )
          {
            printf("udp send failure,%d\n",len);
          }
        }
      }
      else
      {
        printf(" OCM send buf overflow,%d,%d,%d\n",free-last_send, free, last_send);
      }
      last_send = free;

    }
    else
      printf("error in packet head, dropped %x %d %x %x\n",recvBuf[0],recvBuf[1],recvBuf[2],recvBuf[3]);
 }
 
}
