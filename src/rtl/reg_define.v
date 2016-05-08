/* Write only Reg */
`define AXI2S_EN        8'h00
`define AXI2S_IBASE     8'h10
`define AXI2S_ISIZE     8'h14
`define AXI2S_OBASE     8'h18
`define AXI2S_OSIZE     8'h1C
`define FRAME_LEN       8'h20
`define FRAME_ADJ       8'h24
`define TSTART          8'h30
`define TEND            8'h34
`define RSTART          8'h38
`define REND            8'h3C
/* Read Only Reg */
`define AXI2S_STATE     8'h00
`define AXI2S_IACNT     8'h10
`define AXI2S_IBCNT     8'h14
`define AXI2S_OACNT     8'h18
`define AXI2S_OBCNT     8'h1c
