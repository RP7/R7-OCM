#ifndef __Q7_Mem_H
#define __Q7_Mem_H
#include <usrttype.h>
#include <memory.h>
#include <stdio.h>
#include <stdlib.h>
#include <CPBuffer.h>
#include <udp_header.h>
#include <sysClock.h>

class Q7Mem : public CPBuffer {
  public:
    struct structQ7MemHead {
      struct structCPBMeta meta;
      uint64_t _off;
      uint32_t maxSend;
      uint32_t overSend;
      uint64_t safe;
      uint64_t cpu;
      sysClock_t clk;
      udp_package_t packet;
      char appdata[1024];    
    };
  public:
    struct structQ7MemHead *head;
    sysClock sClk;
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
    uint64_t getOff(){  return head->_off; };
    void setOff( uint64_t off ) { head->_off = off; };
    void *_getBuf(uint64_t from, int len){ head->_off = from+(uint64_t)len; return CPBuffer::getBuf((long long)from,len);};
    void *_appData() { return (void *)&head->appdata;};

};
#endif // __Q7_Mem_H
