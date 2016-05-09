#define SPI_Config            0x00000000 //32 mixed 0x00020000 SPI configuration register
#define SPI_Intr_status       0x00000004 //32 mixed 0x00000004 SPI interrupt status register
#define SPI_Intrpt_en         0x00000008 //32 mixed 0x00000000 Interrupt Enable register
#define SPI_Intrpt_dis        0x0000000C //32 mixed 0x00000000 Interrupt disable register
#define SPI_Intrpt_mask       0x00000010 //32 ro 0x00000000 Interrupt mask register
#define SPI_En                0x00000014 //32 mixed 0x00000000 SPI_Enable Register
#define SPI_Delay             0x00000018 //32 rw 0x00000000 Delay Register
#define SPI_Tx_data           0x0000001C //32 wo 0x00000000 Transmit Data Register.
#define SPI_Rx_data           0x00000020 //32 ro 0x00000000 Receive Data Register
#define SPI_Slave_Idle_count  0x00000024 //32 mixed 0x000000FF Slave Idle Count Register
#define SPI_TX_thres          0x00000028 //32 rw 0x00000001 TX_FIFO Threshold Register
#define SPI_RX_thres          0x0000002C //32 rw 0x00000001 RX FIFO Threshold Register
#define SPI_Mod_id            0x000000FC //32 ro 0x00090106 Module ID register

/************************************************************************************************************************ 
SPI_Config Linux 0x7c09

Modefail_gen_en 17 rw 0x1 ModeFail Generation Enable
1: enable
* 0: disable

Man_start_com (MANSTRT) 16 wo 0x0 Manual Start Command
1: start transmission of data
* 0: don't care

Man_start_en 15 rw 0x0 Manual Start Enable
* 1: enables manual start
0: auto mode

Manual_CS 14 rw 0x0 Manual CS
* 1: manual CS mode
0: auto mode

CS 13:10 rw 0x0 Peripheral chip select lines (only valid if Manual_CS=1)
xxx0 - slave 0 selected
xx01 - slave 1 selected
x011 - slave 2 selected
0111 - reserved
* 1111 - No slave selected

PERI_SEL 9 rw 0x0 Peripheral select decode
1: allow external 3-to-8 decode
* 0: only 1 of 3 selects

REF_CLK 8 rw 0x0 Master reference clock select
1: not supported
* 0: use SPI REFERENCE CLOCK

reserved 7:6 rw 0x0 Reserved, read as zero, write with 00

BAUD_RATE_DIV 5:3 rw 0x0 Master mode baud rate divisor controls the amount the spi_ref_clk is divided inside the SPI block
000: not supported
* 001: divide by 4
010: divide by 8
011: divide by 16
100: divide by 32
101: divide by 64
110: divide by 128
111: divide by 25

CLK_PH  (CPHA)  2 rw 0x0 Clock phase
1: the SPI clock is inactive outside the word
* 0: the SPI clock is active outside the word

CLK_POL (CPOL) 1 rw 0x0 Clock polarity outside SPI word
1: the SPI clock is quiescent high
* 0: the SPI clock is quiescent low
MODE_SEL (MSTREN) 0 rw 0x0 Mode select
* 1: the SPI is in master mode
0: the SPI is in slave mode

*****************************************************************************************************************************/