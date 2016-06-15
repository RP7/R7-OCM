`timescale 1 ps / 1 ps
`include "config.v"

module R7OCM_top
   (
    /////////////////// global clock input
    SYS_CLK,
    /////////////////// DDR interface
    DDR_addr,
    DDR_ba,
    DDR_cas_n,
    DDR_ck_n,
    DDR_ck_p,
    DDR_cke,
    DDR_cs_n,
    DDR_dm,
    DDR_dq,
    DDR_dqs_n,
    DDR_dqs_p,
    DDR_odt,
    DDR_ras_n,
    DDR_reset_n,
    DDR_we_n,
    /////////////////// MIO
    FIXED_IO_ddr_vrn,
    FIXED_IO_ddr_vrp,
    FIXED_IO_mio,
    FIXED_IO_ps_clk,
    FIXED_IO_ps_porb,
    FIXED_IO_ps_srstb,
    /////////////////// GE interface
    GMII_TX_EN,
    GMII_TX_ER,
    GMII_TXD,
    GMII_TXCLK,
    GMII_GTXCLK,
    GMII_RXD,
    GMII_RX_ER,
    GMII_RX_DV,
    GMII_RXCLK,
    
    GMII_MDIO,
    GMII_MDIO_MDC,
    GMII_GE_IND,
    /////////////////// RF
    PA_EN,
    RF_SW,
    /////////////////// AD9361
    AD9361_RST,
    AD9361_EN,

    AD9361_Tx_Rx,           
    AD9361_EN_AGC,          
    
    AD9361_RX_Frame_P,      
    AD9361_RX_Frame_N,      
    AD9361_DATA_CLK_P,      
    AD9361_DATA_CLK_N,      
    AD9361_RX_DATA_P,       
    AD9361_RX_DATA_N,       
    
    AD9361_TX_Frame_P,      
    AD9361_TX_Frame_N,      
    AD9361_FB_CLK_P,        
    AD9361_FB_CLK_N,        
    AD9361_TX_DATA_P,       
    AD9361_TX_DATA_N,       
    
    RF_CTRL_IN,             
    RF_CTRL_OUT, 
    /////////////////// AD9361 SPI
    AD9361_SPI_CLK, //         : out   std_logic;
    AD9361_SPI_ENB, //         : out   std_logic;
    AD9361_SPI_DI,  //         : out   std_logic;
    AD9361_SPI_DO,  //         : in    std_logic;  

    /////////////////// test interface
    TEST_LED
  );

  input SYS_CLK; 

  inout [14:0]DDR_addr;
  inout [2:0]DDR_ba;
  inout DDR_cas_n;
  inout DDR_ck_n;
  inout DDR_ck_p;
  inout DDR_cke;
  inout DDR_cs_n;
  inout [3:0]DDR_dm;
  inout [31:0]DDR_dq;
  inout [3:0]DDR_dqs_n;
  inout [3:0]DDR_dqs_p;
  inout DDR_odt;
  inout DDR_ras_n;
  inout DDR_reset_n;
  inout DDR_we_n;
  
  inout FIXED_IO_ddr_vrn;
  inout FIXED_IO_ddr_vrp;
  inout [53:0]FIXED_IO_mio;
  inout FIXED_IO_ps_clk;
  inout FIXED_IO_ps_porb;
  inout FIXED_IO_ps_srstb;

  input [7:0]GMII_RXD;
  input GMII_RXCLK;
  input GMII_RX_DV;
  input GMII_RX_ER;
  output [7:0]GMII_TXD;
  input GMII_TXCLK;
  output GMII_GTXCLK;
  output GMII_TX_EN;
  output GMII_TX_ER;
  inout GMII_MDIO;
  output GMII_MDIO_MDC;
  input GMII_GE_IND;
// RF
  output PA_EN;
  output RF_SW;
// AD9361
  output AD9361_RST;
  output AD9361_EN;

  output AD9361_Tx_Rx;          //          : out std_logic;
  output AD9361_EN_AGC;         //          : out std_logic;

  input  AD9361_RX_Frame_P;     //          : in  std_logic;
  input  AD9361_RX_Frame_N;     //          : in  std_logic;
  input  AD9361_DATA_CLK_P;     //          : in  std_logic;
  input  AD9361_DATA_CLK_N;     //          : in  std_logic;
  input  [5:0]AD9361_RX_DATA_P; //          : in  std_logic_vector(5 downto 0);
  input  [5:0]AD9361_RX_DATA_N; //          : in  std_logic_vector(5 downto 0);

  output AD9361_TX_Frame_P;     //          : out std_logic;
  output AD9361_TX_Frame_N;     //          : out std_logic;
  output AD9361_FB_CLK_P;       //          : out std_logic;
  output AD9361_FB_CLK_N;       //          : out std_logic;
  output [5:0]AD9361_TX_DATA_P; //          : out std_logic_vector(5 downto 0);
  output [5:0]AD9361_TX_DATA_N; //          : out std_logic_vector(5 downto 0);

  output [3:0]RF_CTRL_IN;       //          : out std_logic_vector(3 downto 0);
  input  [7:0]RF_CTRL_OUT;      //          : in  std_logic_vector(7 downto 0);
// AD9361 SPI  
  inout AD9361_SPI_CLK;
  inout AD9361_SPI_ENB;
  inout AD9361_SPI_DI;
  inout AD9361_SPI_DO;

  output [3:0]TEST_LED;

// internal signal

  wire ENET0_MDIO_O;
  wire ENET0_MDIO_T;
  wire ENET0_MDIO_I;
  wire[17:0] BRAM_PORTA_addr;
  wire BRAM_PORTA_clk;
  wire[31:0] BRAM_PORTA_din;
  wire[31:0] BRAM_PORTA_dout;
  wire BRAM_PORTA_en;
  wire BRAM_PORTA_rst;
  wire[3:0] BRAM_PORTA_we;

// AXI HP wire
  wire FCLK_CLK1;
  wire axi_rst_n;

  wire AXI_clk;
  wire [31:0]AXI_HP0_araddr;
  wire [1:0]AXI_HP0_arburst;
  wire [3:0]AXI_HP0_arcache;
  wire [5:0]AXI_HP0_arid;
  wire [3:0]AXI_HP0_arlen;
  wire [1:0]AXI_HP0_arlock;
  wire [2:0]AXI_HP0_arprot;
  wire [3:0]AXI_HP0_arqos;
  wire AXI_HP0_arready;
  wire [2:0]AXI_HP0_arsize;
  wire AXI_HP0_arvalid;
  wire [31:0]AXI_HP0_awaddr;
  wire [1:0]AXI_HP0_awburst;
  wire [3:0]AXI_HP0_awcache;
  wire [5:0]AXI_HP0_awid;
  wire [3:0]AXI_HP0_awlen;
  wire [1:0]AXI_HP0_awlock;
  wire [2:0]AXI_HP0_awprot;
  wire [3:0]AXI_HP0_awqos;
  wire AXI_HP0_awready;
  wire [2:0]AXI_HP0_awsize;
  wire AXI_HP0_awvalid;
  wire [5:0]AXI_HP0_bid;
  wire AXI_HP0_bready;
  wire [1:0]AXI_HP0_bresp;
  wire AXI_HP0_bvalid;
  wire [31:0]AXI_HP0_rdata;
  wire [5:0]AXI_HP0_rid;
  wire AXI_HP0_rlast;
  wire AXI_HP0_rready;
  wire [1:0]AXI_HP0_rresp;
  wire AXI_HP0_rvalid;
  wire [31:0]AXI_HP0_wdata;
  wire [5:0]AXI_HP0_wid;
  wire AXI_HP0_wlast;
  wire AXI_HP0_wready;
  wire [3:0]AXI_HP0_wstrb;
  wire AXI_HP0_wvalid;

  wire rst,Sclk,sync;
  wire Ien,Oen,ad9361_Ien;

  wire [31:0]Sin;
  wire [31:0]Sout;
  wire [11:0]Rx_I;
  wire [11:0]Rx_Q;
  
  wire [31:0] AXI_IBASE;
  wire [31:0] AXI_OBASE;
  wire [23:6] AXI_ISIZE;
  wire [23:6] AXI_OSIZE;

  wire [23:6] AXI_IACNT;
  wire [23:6] AXI_OACNT;

  wire [31:0] AXI_IBCNT;
  wire [31:0] AXI_OBCNT;

  wire sys_Ien,sys_Oen;
  wire MOSI,MISO,SCK,SS;
  wire sys_async;
  wire [31:0] AXI2S_REG_DOUT;
  wire [31:0] AD9361_REG_DOUT;

`ifdef DEBUG 
  wire test;

  wire [31:0]axiwresp;
  wire [31:0]axirresp;
  wire [31:0]axistatus;
  wire [31:0]testD;
`endif

armocm_wrapper core
  (
  .BRAM_PORTA_addr(BRAM_PORTA_addr),
  .BRAM_PORTA_clk(BRAM_PORTA_clk),
  .BRAM_PORTA_din(BRAM_PORTA_din),
  .BRAM_PORTA_dout(BRAM_PORTA_dout),
  .BRAM_PORTA_en(BRAM_PORTA_en),
  .BRAM_PORTA_rst(BRAM_PORTA_rst),
  .BRAM_PORTA_we(BRAM_PORTA_we),

  .DDR_addr(DDR_addr),
  .DDR_ba(DDR_ba),
  .DDR_cas_n(DDR_cas_n),
  .DDR_ck_n(DDR_ck_n),
  .DDR_ck_p(DDR_ck_p),
  .DDR_cke(DDR_cke),
  .DDR_cs_n(DDR_cs_n),
  .DDR_dm(DDR_dm),
  .DDR_dq(DDR_dq),
  .DDR_dqs_n(DDR_dqs_n),
  .DDR_dqs_p(DDR_dqs_p),
  .DDR_odt(DDR_odt),
  .DDR_ras_n(DDR_ras_n),
  .DDR_reset_n(DDR_reset_n),
  .DDR_we_n(DDR_we_n),
  
  .ENET0_GMII_RXD(GMII_RXD),
  .ENET0_GMII_RX_CLK(GMII_RXCLK),
  .ENET0_GMII_RX_DV(GMII_RX_DV),
  .ENET0_GMII_RX_ER(GMII_RX_ER),
  .ENET0_GMII_TXD(GMII_TXD),
  .ENET0_GMII_TX_CLK(ENET0_GMII_TX_CLK),
  .ENET0_GMII_TX_EN(GMII_TX_EN),
  .ENET0_GMII_TX_ER(GMII_TX_ER),
  .ENET0_MDIO_I(ENET0_MDIO_I),
  .ENET0_MDIO_MDC(GMII_MDIO_MDC),
  .ENET0_MDIO_O(ENET0_MDIO_O),
  .ENET0_MDIO_T(ENET0_MDIO_T),
  
  .FIXED_IO_ddr_vrn(FIXED_IO_ddr_vrn),
  .FIXED_IO_ddr_vrp(FIXED_IO_ddr_vrp),
  .FIXED_IO_mio(FIXED_IO_mio),
  .FIXED_IO_ps_clk(FIXED_IO_ps_clk),
  .FIXED_IO_ps_porb(FIXED_IO_ps_porb),
  .FIXED_IO_ps_srstb(FIXED_IO_ps_srstb),

  .FCLK_CLK1(FCLK_CLK1),
  .FCLK_RESET1_N(axi_rst_n),
  
  .S_AXI_HP0_araddr(AXI_HP0_araddr),
  .S_AXI_HP0_arburst(AXI_HP0_arburst),
  .S_AXI_HP0_arcache(AXI_HP0_arcache),
  .S_AXI_HP0_arid(AXI_HP0_arid),
  .S_AXI_HP0_arlen(AXI_HP0_arlen),
  .S_AXI_HP0_arlock(AXI_HP0_arlock),
  .S_AXI_HP0_arprot(AXI_HP0_arprot),
  .S_AXI_HP0_arqos(AXI_HP0_arqos),
  .S_AXI_HP0_arready(AXI_HP0_arready),
  .S_AXI_HP0_arsize(AXI_HP0_arsize),
  .S_AXI_HP0_arvalid(AXI_HP0_arvalid),
  .S_AXI_HP0_awaddr(AXI_HP0_awaddr),
  .S_AXI_HP0_awburst(AXI_HP0_awburst),
  .S_AXI_HP0_awcache(AXI_HP0_awcache),
  .S_AXI_HP0_awid(AXI_HP0_awid),
  .S_AXI_HP0_awlen(AXI_HP0_awlen),
  .S_AXI_HP0_awlock(AXI_HP0_awlock),
  .S_AXI_HP0_awprot(AXI_HP0_awprot),
  .S_AXI_HP0_awqos(AXI_HP0_awqos),
  .S_AXI_HP0_awready(AXI_HP0_awready),
  .S_AXI_HP0_awsize(AXI_HP0_awsize),
  .S_AXI_HP0_awvalid(AXI_HP0_awvalid),
  .S_AXI_HP0_bid(AXI_HP0_bid),
  .S_AXI_HP0_bready(AXI_HP0_bready),
  .S_AXI_HP0_bresp(AXI_HP0_bresp),
  .S_AXI_HP0_bvalid(AXI_HP0_bvalid),
  .S_AXI_HP0_rdata(AXI_HP0_rdata),
  .S_AXI_HP0_rid(AXI_HP0_rid),
  .S_AXI_HP0_rlast(AXI_HP0_rlast),
  .S_AXI_HP0_rready(AXI_HP0_rready),
  .S_AXI_HP0_rresp(AXI_HP0_rresp),
  .S_AXI_HP0_rvalid(AXI_HP0_rvalid),
  .S_AXI_HP0_wdata(AXI_HP0_wdata),
  .S_AXI_HP0_wid(AXI_HP0_wid),
  .S_AXI_HP0_wlast(AXI_HP0_wlast),
  .S_AXI_HP0_wready(AXI_HP0_wready),
  .S_AXI_HP0_wstrb(AXI_HP0_wstrb),
  .S_AXI_HP0_wvalid(AXI_HP0_wvalid),

  .spi_1_io0_io(MOSI),
  .spi_1_io1_io(MISO),
  .spi_1_sck_io(SCK),
  .spi_1_ss_io(SS)//,

  //.test_led_tri_o(TEST_LED)
  );



GE_patch gep
   (
    .SYS_CLK(SYS_CLK),

    .GMII_TXCLK(GMII_TXCLK),
    .GMII_GTXCLK(GMII_GTXCLK),
    .GMII_GE_IND(GMII_GE_IND),
    
    .ENET0_GMII_TX_CLK(ENET0_GMII_TX_CLK),

    .ENET0_MDIO_I(ENET0_MDIO_I),
    .ENET0_MDIO_O(ENET0_MDIO_O),
    .ENET0_MDIO_T(ENET0_MDIO_T),

    .GMII_MDIO(GMII_MDIO)
  );

AXI2S a2s
  (
    .rst(rst),

    .Sclk(Sclk),

    .Sin(Sin),
    .Ien(Ien&sys_Ien),

    .Sout(Sout),
    .Oen(Oen&sys_Oen),
    .sync(sync),

    .ibase(AXI_IBASE),
    .isize(AXI_ISIZE),
    .obase(AXI_OBASE),
    .osize(AXI_OSIZE),
    .iacnt(AXI_IACNT),
    .ibcnt(AXI_IBCNT),
    .oacnt(AXI_OACNT),
    .obcnt(AXI_OBCNT),

    .AXI_clk(AXI_clk),
    .AXI_rst_n(axi_rst_n),
    .AXI_araddr(AXI_HP0_araddr),
    .AXI_arburst(AXI_HP0_arburst),
    .AXI_arcache(AXI_HP0_arcache),
    .AXI_arid(AXI_HP0_arid),
    .AXI_arlen(AXI_HP0_arlen),
    .AXI_arlock(AXI_HP0_arlock),
    .AXI_arprot(AXI_HP0_arprot),
    .AXI_arqos(AXI_HP0_arqos),
    .AXI_arready(AXI_HP0_arready),
    .AXI_arsize(AXI_HP0_arsize),
    .AXI_arvalid(AXI_HP0_arvalid),
    .AXI_awaddr(AXI_HP0_awaddr),
    .AXI_awburst(AXI_HP0_awburst),
    .AXI_awcache(AXI_HP0_awcache),
    .AXI_awid(AXI_HP0_awid),
    .AXI_awlen(AXI_HP0_awlen),
    .AXI_awlock(AXI_HP0_awlock),
    .AXI_awprot(AXI_HP0_awprot),
    .AXI_awqos(AXI_HP0_awqos),
    .AXI_awready(AXI_HP0_awready),
    .AXI_awsize(AXI_HP0_awsize),
    .AXI_awvalid(AXI_HP0_awvalid),
    .AXI_bid(AXI_HP0_bid),
    .AXI_bready(AXI_HP0_bready),
    .AXI_bresp(AXI_HP0_bresp),
    .AXI_bvalid(AXI_HP0_bvalid),
    .AXI_rdata(AXI_HP0_rdata),
    .AXI_rid(AXI_HP0_rid),
    .AXI_rlast(AXI_HP0_rlast),
    .AXI_rready(AXI_HP0_rready),
    .AXI_rresp(AXI_HP0_rresp),
    .AXI_rvalid(AXI_HP0_rvalid),
    .AXI_wdata(AXI_HP0_wdata),
    .AXI_wid(AXI_HP0_wid),
    .AXI_wlast(AXI_HP0_wlast),
    .AXI_wready(AXI_HP0_wready),
    .AXI_wstrb(AXI_HP0_wstrb),
    .AXI_wvalid(AXI_HP0_wvalid)
  );

AXI2SREG axi2s_reg_space
  (
    .clk(BRAM_PORTA_clk),
    .rst(BRAM_PORTA_rst),
    .en(BRAM_PORTA_en),
    .addr(BRAM_PORTA_addr),
    .din(BRAM_PORTA_din),
    .dout(AXI2S_REG_DOUT),
    .wen(BRAM_PORTA_we),
    .ien(sys_Ien),
    .oen(sys_Oen),
    .async(sys_async),
    .test(test),
    .ibase(AXI_IBASE),
    .isize(AXI_ISIZE),
    .obase(AXI_OBASE),
    .osize(AXI_OSIZE),
`ifdef DEBUG
    .axiwresp(axiwresp),
    .axirresp(axirresp),
    .axistatus(axistatus),
    .axiraddr(AXI_HP0_araddr),
    .axiwaddr(AXI_HP0_awaddr),
`endif
    .iacnt(AXI_IACNT),
    .ibcnt(AXI_IBCNT),
    .oacnt(AXI_OACNT),
    .obcnt(AXI_OBCNT)
  );

AD9361REG ad9361_reg_space
  (
    .clk(BRAM_PORTA_clk),
    .rst(BRAM_PORTA_rst),
    .en(BRAM_PORTA_en),
    .addr(BRAM_PORTA_addr),
    .din(BRAM_PORTA_din),
    .dout(AD9361_REG_DOUT),
    .wen(BRAM_PORTA_we),
    .ad9361_rstb(AD9361_RST),
    .ad9361_en(AD9361_EN),
    .ad9361_tx_rx(AD9361_Tx_Rx),
    .ad9361_en_agc(AD9361_EN_AGC),
    .rf_ctrl_in(RF_CTRL_IN),
    .pa_en(PA_EN),
    .rf_sw(RF_SW)
  );

CBusReadMerge cbmerge
  (
    .clk(BRAM_PORTA_clk),
    .rst(BRAM_PORTA_rst),
    .en(BRAM_PORTA_en),
    .addr(BRAM_PORTA_addr),
    .dout(BRAM_PORTA_dout),
    .axi2s_dout(AXI2S_REG_DOUT),
    .ad9361_dout(AD9361_REG_DOUT)  
  );

ad9361_1t1r ad_if
(
    .AD9361_RX_Frame_P(AD9361_RX_Frame_P),      
    .AD9361_RX_Frame_N(AD9361_RX_Frame_N),      
    .AD9361_DATA_CLK_P(AD9361_DATA_CLK_P),      
    .AD9361_DATA_CLK_N(AD9361_DATA_CLK_N),      
    .AD9361_RX_DATA_P(AD9361_RX_DATA_P),       
    .AD9361_RX_DATA_N(AD9361_RX_DATA_N),       

    .AD9361_TX_Frame_P(AD9361_TX_Frame_P),      
    .AD9361_TX_Frame_N(AD9361_TX_Frame_N),      
    .AD9361_FB_CLK_P(AD9361_FB_CLK_P),        
    .AD9361_FB_CLK_N(AD9361_FB_CLK_N),        
    .AD9361_TX_DATA_P(AD9361_TX_DATA_P),       
    .AD9361_TX_DATA_N(AD9361_TX_DATA_N),

    .clk(Sclk),
    .rst(rst),
    .rx_I(Rx_I),
    .rx_Q(Rx_Q),
    .tx_I(Sout[11:0]),
    .tx_Q(Sout[27:16]),
    .rx_ce(ad9361_Ien),
    .tx_ce(Oen)       
  );

edgesync #(.e("neg")) axi_sync
(   .clk(Sclk)
  , .async(sys_async)
  , .sync(sync)
);

assign     rst = 1'b0;
assign AXI_clk = FCLK_CLK1;

assign AD9361_SPI_CLK = SCK;
assign AD9361_SPI_DI  = MOSI;
assign AD9361_SPI_DO  = MISO;
assign AD9361_SPI_ENB = SS;
assign TEST_LED = 4'h0;


`ifdef DEBUG
AXIResp wresp
  (
  .clk(AXI_clk),
  .valid(AXI_HP0_bvalid),
  .resp(AXI_HP0_bresp),
  .ready(AXI_HP0_bready),
  .respOut(axiwresp)
  );
AXIResp rresp
  (
  .clk(AXI_clk),
  .valid(AXI_HP0_rvalid&AXI_HP0_rready),
  .resp(AXI_HP0_rresp),
  .respOut(axirresp)
  );
cntSrc testSrc
  (
    .clk(Sclk),
    .en(Ien&sys_Ien),
    .rst(1'b0),
    .Cout(testD)
  );
assign axistatus = { 24'h0
                  , AXI_HP0_arvalid
                  , AXI_HP0_arready
                  , AXI_HP0_awvalid
                  , AXI_HP0_awready
                  , AXI_HP0_rready
                  , AXI_HP0_rvalid
                  , AXI_HP0_wready
                  , AXI_HP0_wvalid
};
assign Sin = (test==1'b1)? testD : {Rx_Q[11],Rx_Q[11],Rx_Q[11],Rx_Q[11],Rx_Q[11:0],Rx_I[11],Rx_I[11],Rx_I[11],Rx_I[11],Rx_I[11:0]};
assign Ien = (test==1'b1)? 1'b1  : ad9361_Ien;
`else 
assign Sin = {Rx_Q[11],Rx_Q[11],Rx_Q[11],Rx_Q[11],Rx_Q[11:0],Rx_I[11],Rx_I[11],Rx_I[11],Rx_I[11],Rx_I[11:0]};
assign Ien = ad9361_Ien;
assign AXI_HP0_bready = 1'b1;
`endif

endmodule
