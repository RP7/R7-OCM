`timescale 1 ps / 1 ps

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

  output [3:0]TEST_LED;

// internal signal

  wire clk_125M;
  wire pll_locked;
  wire pll_reset;
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

  reg GMII_GE_IND_reg;
  reg[27:0] GMII_GE_TIMER;
  wire ENET0_GMII_TX_CLK;

// AXI HP wire
  wire [31:0]S_AXI_HP0_araddr;
  wire [1:0]S_AXI_HP0_arburst;
  wire [3:0]S_AXI_HP0_arcache;
  wire [5:0]S_AXI_HP0_arid;
  wire [3:0]S_AXI_HP0_arlen;
  wire [1:0]S_AXI_HP0_arlock;
  wire [2:0]S_AXI_HP0_arprot;
  wire [3:0]S_AXI_HP0_arqos;
  wire S_AXI_HP0_arready;
  wire [2:0]S_AXI_HP0_arsize;
  wire S_AXI_HP0_arvalid;
  wire [31:0]S_AXI_HP0_awaddr;
  wire [1:0]S_AXI_HP0_awburst;
  wire [3:0]S_AXI_HP0_awcache;
  wire [5:0]S_AXI_HP0_awid;
  wire [3:0]S_AXI_HP0_awlen;
  wire [1:0]S_AXI_HP0_awlock;
  wire [2:0]S_AXI_HP0_awprot;
  wire [3:0]S_AXI_HP0_awqos;
  wire S_AXI_HP0_awready;
  wire [2:0]S_AXI_HP0_awsize;
  wire S_AXI_HP0_awvalid;
  wire [5:0]S_AXI_HP0_bid;
  wire S_AXI_HP0_bready;
  wire [1:0]S_AXI_HP0_bresp;
  wire S_AXI_HP0_bvalid;
  wire [31:0]S_AXI_HP0_rdata;
  wire [5:0]S_AXI_HP0_rid;
  wire S_AXI_HP0_rlast;
  wire S_AXI_HP0_rready;
  wire [1:0]S_AXI_HP0_rresp;
  wire S_AXI_HP0_rvalid;
  wire [31:0]S_AXI_HP0_wdata;
  wire [5:0]S_AXI_HP0_wid;
  wire S_AXI_HP0_wlast;
  wire S_AXI_HP0_wready;
  wire [3:0]S_AXI_HP0_wstrb;
  wire S_AXI_HP0_wvalid;
  
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
  
  .ENET0_GMII_RXD(ENET0_GMII_RXD),
  .ENET0_GMII_RX_CLK(ENET0_GMII_RX_CLK),
  .ENET0_GMII_RX_DV(ENET0_GMII_RX_DV),
  .ENET0_GMII_RX_ER(ENET0_GMII_RX_ER),
  .ENET0_GMII_TXD(ENET0_GMII_TXD),
  .ENET0_GMII_TX_CLK(ENET0_GMII_TX_CLK),
  .ENET0_GMII_TX_EN(ENET0_GMII_TX_EN),
  .ENET0_GMII_TX_ER(ENET0_GMII_TX_ER),
  .ENET0_MDIO_I(ENET0_MDIO_I),
  .ENET0_MDIO_MDC(ENET0_MDIO_MDC),
  .ENET0_MDIO_O(ENET0_MDIO_O),
  .ENET0_MDIO_T(ENET0_MDIO_T),
  
  .FIXED_IO_ddr_vrn(FIXED_IO_ddr_vrn),
  .FIXED_IO_ddr_vrp(FIXED_IO_ddr_vrp),
  .FIXED_IO_mio(FIXED_IO_mio),
  .FIXED_IO_ps_clk(FIXED_IO_ps_clk),
  .FIXED_IO_ps_porb(FIXED_IO_ps_porb),
  .FIXED_IO_ps_srstb(FIXED_IO_ps_srstb),
  
  .S_AXI_HP0_araddr(S_AXI_HP0_araddr),
  .S_AXI_HP0_arburst(S_AXI_HP0_arburst),
  .S_AXI_HP0_arcache(S_AXI_HP0_arcache),
  .S_AXI_HP0_arid(S_AXI_HP0_arid),
  .S_AXI_HP0_arlen(S_AXI_HP0_arlen),
  .S_AXI_HP0_arlock(S_AXI_HP0_arlock),
  .S_AXI_HP0_arprot(S_AXI_HP0_arprot),
  .S_AXI_HP0_arqos(S_AXI_HP0_arqos),
  .S_AXI_HP0_arready(S_AXI_HP0_arready),
  .S_AXI_HP0_arsize(S_AXI_HP0_arsize),
  .S_AXI_HP0_arvalid(S_AXI_HP0_arvalid),
  .S_AXI_HP0_awaddr(S_AXI_HP0_awaddr),
  .S_AXI_HP0_awburst(S_AXI_HP0_awburst),
  .S_AXI_HP0_awcache(S_AXI_HP0_awcache),
  .S_AXI_HP0_awid(S_AXI_HP0_awid),
  .S_AXI_HP0_awlen(S_AXI_HP0_awlen),
  .S_AXI_HP0_awlock(S_AXI_HP0_awlock),
  .S_AXI_HP0_awprot(S_AXI_HP0_awprot),
  .S_AXI_HP0_awqos(S_AXI_HP0_awqos),
  .S_AXI_HP0_awready(S_AXI_HP0_awready),
  .S_AXI_HP0_awsize(S_AXI_HP0_awsize),
  .S_AXI_HP0_awvalid(S_AXI_HP0_awvalid),
  .S_AXI_HP0_bid(S_AXI_HP0_bid),
  .S_AXI_HP0_bready(S_AXI_HP0_bready),
  .S_AXI_HP0_bresp(S_AXI_HP0_bresp),
  .S_AXI_HP0_bvalid(S_AXI_HP0_bvalid),
  .S_AXI_HP0_rdata(S_AXI_HP0_rdata),
  .S_AXI_HP0_rid(S_AXI_HP0_rid),
  .S_AXI_HP0_rlast(S_AXI_HP0_rlast),
  .S_AXI_HP0_rready(S_AXI_HP0_rready),
  .S_AXI_HP0_rresp(S_AXI_HP0_rresp),
  .S_AXI_HP0_rvalid(S_AXI_HP0_rvalid),
  .S_AXI_HP0_wdata(S_AXI_HP0_wdata),
  .S_AXI_HP0_wid(S_AXI_HP0_wid),
  .S_AXI_HP0_wlast(S_AXI_HP0_wlast),
  .S_AXI_HP0_wready(S_AXI_HP0_wready),
  .S_AXI_HP0_wstrb(S_AXI_HP0_wstrb),
  .S_AXI_HP0_wvalid(S_AXI_HP0_wvalid),

  .TEST_LED_tri_o(TEST_LED)
  );

clk_wiz_0 pll
  (
  .clk_in1(SYS_CLK),
  .clk_out1(SYS_CLK),
  .reset(pll_reset), 
  .locked(pll_locked)            
  );

iobuf GMII_MDIO_BUF
  (
  .I(ENET0_MDIO_O)
  .IO(GMII_MDIO)
  .O(ENET0_MDIO_I)
  .T(ENET0_MDIO_T)
  );

always @ posedge(clk_125M)
begin
  if ( GMII_GE_IND==1'b1 ) begin
    GMII_GE_IND_reg <= 1'b1;
    GMII_GE_TIMER <= 28'h0000000;
  end
  else begin
    if ( GMII_GE_TIMER==28'hffffff ) GMII_GE_IND_reg <= 1'b0;
    else GMII_GE_TIMER <= GMII_GE_TIMER+1'b1;
  end
end

assign GMII_GTXCLK = clk_125M;

always @(GMII_GE_IND_reg or clk_125M or GMII_TXCLK) 
begin
  if (GMII_GE_IND_reg==1'b1) ENET0_GMII_TX_CLK <= clk_125M;
  else ENET0_GMII_TX_CLK <= GMII_TXCLK;
end

endmodule
