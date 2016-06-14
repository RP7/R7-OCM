#ifndef __Q7_Mem_H
#define __Q7_Mem_H
#include <usrttype.h>
#include <memory.h>
#include <stdio.h>
#include <stdlib.h>
#include <CPBuffer.h>
#include <udp_header.h>

class Q7Mem : public CPBuffer {
  public:
    struct structQ7MemHead {
      struct structCPBMeta meta;
      long long _off;
      udp_header_t ph;
      long long overSend;
    };
  private:
    struct structQ7MemHead *head;
  public:
    
    Q7Mem();
    void attach( const char *n );
    void newQ7Mem( const char *n, long long dataL, long long cpL, long long resL );
    void init();
    void dumpHead();
    const char *getName();
    ~Q7Mem();
    void start();
    int64 getKey();
    long long int getOff(){  return head->_off; };
    void *_getBuf(long long from, int len){ head->_off = from+len; return CPBuffer::getBuf(from,len);};
};
#endif // __Q7_Mem_H
