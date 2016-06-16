#include <stdio.h>

#include "Q7Mem.h"
#include "Q7MemAPI.h"

#include "easySocket.h"

int check(Q7Mem *tx,uint64_t rxtime)
{
  if( tx->head->packet.header.offset<rxtime )
  {
    printf("send data is out of date\n");
    tx->head->packet.header.offset = (rxtime+1024L)&(-1024L);
  }
  if( tx->head->packet.header.offset>rxtime+tx->getSize() )
  {
    printf("send data is out of buffer\n");
    tx->head->packet.header.offset = (rxtime+1024L)&(-1024L);
  }
  
  tx->head->safe = rxtime+tx->head->overSend;
  tx->head->packet.header.time = rxtime;
  return 0;
}

int main(int argc, char*argv[] )
{
  Q7Mem *tx_mem = attachQ7Mem( "tx_udp.d" );
  tx_mem->head->maxSend = 16;
  tx_mem->head->overSend = 1920*4*4; //4ms
  dumpQ7Mem( tx_mem );
  Q7Mem *rx_mem = attachQ7Mem( "rx_udp.d" );
  dumpQ7Mem( rx_mem );
  int port;
  sscanf( argv[2],"%d",&port );
  printf("port %d,sizeof int %ld\n",port, sizeof(int));
  udpClient udp( argv[1], port );
  udp.send( (char *)(&tx_mem->head->packet), sizeof(udp_package_t) );
  int len = 0;
  
  while( (len=udp.recv( (char*)(&rx_mem->head->packet), sizeof(udp_package_t) )) == sizeof(udp_package_t) )
  {
    uint64_t from = rx_mem->head->packet.header.offset;
    uint64_t offset = rx_mem->getOff();
    rx_mem->head->cpu = rx_mem->sClk.getCpu();
    if( from != offset )
    {
      printf("recv discontinued _off:%lx, off:%lx\n",offset,from);
      rx_mem->setOff(from);
    }
    void *p = (void *)rx_mem->_getBuf( from, sizeof(rx_mem->head->packet.data) );
    memcpy( p, &(rx_mem->head->packet.data), sizeof(rx_mem->head->packet.data) );
    int ck = check(tx_mem,rx_mem->head->packet.header.time);
      
    for( int i=0;i<tx_mem->head->maxSend;i++ )
    {
      if(tx_mem->head->packet.header.offset<tx_mem->head->safe)
      {
        p = (void *)tx_mem->_getBuf( tx_mem->head->packet.header.offset, sizeof(tx_mem->head->packet.data) );
        memcpy(&(tx_mem->head->packet.data),p,sizeof(tx_mem->head->packet.data));
        tx_mem->head->packet.header.offset += sizeof(tx_mem->head->packet.data);
        len = udp.send( (char *)(&tx_mem->head->packet), sizeof(udp_package_t) );
        if( len!=sizeof(udp_package_t) )
        {
          printf("udp send failure,%d\n",len);
        }
      }
      else
        break;
    }
  }
  printf("recv length error %d, exit\n",len);
}
