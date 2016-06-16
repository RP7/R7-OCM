#include <usrttype.h>
#include <inttypes.h> //uint32_t,uint64_t
#include "Q7Mem.h"

extern "C" {
  void initQ7Mem( const char *fileName, int blk, int cp );
  Q7Mem *attachQ7Mem( const char *fileName );
  void dumpQ7Mem( Q7Mem *h );
  int64_t chipNow( Q7Mem *h );
  int64_t cpuNow( Q7Mem *h );
  int64_t cpu2chip( Q7Mem *h, int64_t c );
  void *appData( Q7Mem *h );
  int clkRate( Q7Mem *h );
};// extern "C"


