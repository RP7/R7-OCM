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