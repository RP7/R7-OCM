#define AD9361_SPI_BASE 0xE0007000
#define AD9361_SPI_SIZE 0x1000
#define OCM_BASE 0xfffc0000
#define OCM_SIZE 0x40000
#define FPGA_BASE 0x40000000
#define FPGA_SIZE 0x40000

#define SPIDevice "/dev/mem"
#define FPGAdevice "/dev/mem"

/* AXI2S Write only Reg */
#define AXI2S_EN        0x00000
#define AXI2S_IBASE     0x00010
#define AXI2S_ISIZE     0x00014
#define AXI2S_OBASE     0x00018
#define AXI2S_OSIZE     0x0001C
#define FRAME_LEN       0x00020
#define FRAME_ADJ       0x00024
#define TSTART          0x00030
#define TEND            0x00034
#define RSTART          0x00038
#define REND            0x0003C
/* AXI2S Read Only Reg */
#define AXI2S_STATE     0x00000
#define AXI2S_IACNT     0x00010
#define AXI2S_IBCNT     0x00014
#define AXI2S_OACNT     0x00018
#define AXI2S_OBCNT     0x0001c
/* AD9361 Control Signal */
#define AD9361_RST      0x00100
#define AD9361_EN       0x00110
#define AD9361_TX_RX    0x00120
#define AD9361_EN_AGC   0x00130
#define RF_CTRL_IN      0x00140
#define RF_SW           0x00150
#define PA_EN           0x00160
