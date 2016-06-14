#include <usrttype.h>
#include "Q7Mem.h"

namespace std {

extern "C" {
  
  void initQ7Mem( const char *fileName, int blk, int cp )
  {
    Q7Mem *handle = new Q7Mem();
    handle->newQ7Mem( fileName
      , (long long)(blk*4096)
      , (long long)(cp*4096)
      , (long long)sizeof(struct Q7Mem::structQ7MemHead)
      );
  }

  Q7Mem *attachQ7Mem( const char *fileName )
  {
    Q7Mem *h = new Q7Mem();
    h->attach( fileName );
    h->start();
    return h;
  }  
  void dumpQ7Mem( Q7Mem *h )
  {
    h->dumpHead();
  }
  void offset( Q7Mem *h, long long int *r )
  {
    *r = ( long long int )h->getOff();
  }
  int Q7write( Q7Mem *h, void *buf, int len, long long int off )
  {
    void *p = (void *)h->getBuf( off, len );
    if( p!=NULL )
    {
      memcpy( p, buf, len );
      return len;
    }
    else
      return 0;
  }  
  int Q7read( Q7Mem *h, void *buf, int len, long long int off )
  {
    void *p = (void *)h->getBuf( off, len );
    if( p!=NULL )
    {
      memcpy( buf, p, len );
      return len;
    }
    else
      return 0;
  }
  void *getAddr( Q7Mem *h, long long int off )
  {
    return (void *)h->getBuf(off,0);
  }   
  int mSize( Q7Mem *h )
  {
    return (int)h->getSize();
  }
};// extern "C"

};//namespace std

