FPGA_BASE = 0x40000000
FPGA_SIZE = 0x40000
IEN = 1
OEN = 2
TDDMODE = 4
OCM_BASE = 0xfffc0000
OCM_SIZE = 0x40000
AD9361_SPI_BASE = 0xE0007000
AD9361_SPI_SIZE = 0x1000

import platform
c_system = platform.system()
