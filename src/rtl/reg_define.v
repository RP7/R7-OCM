`define AXI2SREG_BASE   18'h00000
`define AD9361REG_BASE  18'h00100

/* AXI2S Write only Reg */
`define AXI2S_EN        18'h00000
`define AXI2S_TEST      18'h00004
`define AXI2S_IBASE     18'h00010
`define AXI2S_ISIZE     18'h00014
`define AXI2S_OBASE     18'h00018
`define AXI2S_OSIZE     18'h0001C
`define FRAME_LEN       18'h00020
`define FRAME_ADJ       18'h00024
`define TSTART          18'h00030
`define TEND            18'h00034
`define RSTART          18'h00038
`define REND            18'h0003C
/* AXI2S Read Only Reg */
`define AXI2S_STATE     18'h00000
`define AXI2S_IACNT     18'h00010
`define AXI2S_IBCNT     18'h00014
`define AXI2S_OACNT     18'h00018
`define AXI2S_OBCNT     18'h0001c
`define AXI_RRESP       18'h00020
`define AXI_WRESP       18'h00024
`define AXI_STATUS      18'h00028
`define AXI_RADDR       18'h00030
`define AXI_WADDR       18'h00034

/* AD9361 Control Signal */
`define AD9361_RST			18'h00100
`define AD9361_EN				18'h00110
`define AD9361_TX_RX    18'h00120
`define AD9361_EN_AGC   18'h00130
`define RF_CTRL_IN      18'h00140
`define RF_SW           18'h00150
`define PA_EN           18'h00160
