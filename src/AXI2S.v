module AXI2S
   (
   	rst,

   	Sclk,

   	Sin,
   	Ien,

   	Sout,
   	Oen,
   	sync,

    AXI_clk,
    AXI_araddr,
    AXI_arburst,
    AXI_arcache,
    AXI_arid,
    AXI_arlen,
    AXI_arlock,
    AXI_arprot,
    AXI_arqos,
    AXI_arready,
    AXI_arsize,
    AXI_arvalid,
    AXI_awaddr,
    AXI_awburst,
    AXI_awcache,
    AXI_awid,
    AXI_awlen,
    AXI_awlock,
    AXI_awprot,
    AXI_awqos,
    AXI_awready,
    AXI_awsize,
    AXI_awvalid,
    AXI_bid,
    AXI_bready,
    AXI_bresp,
    AXI_bvalid,
    AXI_rdata,
    AXI_rid,
    AXI_rlast,
    AXI_rready,
    AXI_rresp,
    AXI_rvalid,
    AXI_wdata,
    AXI_wid,
    AXI_wlast,
    AXI_wready,
    AXI_wstrb,
    AXI_wvalid
  );
  
  input rst;
  input Sclk;
  input [31:0]Sin;
  input Ien;
  output [31:0]Sout;
  input Oen;
  input sync;

  input AXI_clk;
  output [31:0]AXI_araddr;
  output [1:0]AXI_arburst;
  output [3:0]AXI_arcache;
  output [11:0]AXI_arid;
  output [3:0]AXI_arlen;
  output [1:0]AXI_arlock;
  output [2:0]AXI_arprot;
  output [3:0]AXI_arqos;
  input AXI_arready;
  output [2:0]AXI_arsize;
  output AXI_arvalid;
  output [31:0]AXI_awaddr;
  output [1:0]AXI_awburst;
  output [3:0]AXI_awcache;
  output [11:0]AXI_awid;
  output [3:0]AXI_awlen;
  output [1:0]AXI_awlock;
  output [2:0]AXI_awprot;
  output [3:0]AXI_awqos;
  input AXI_awready;
  output [2:0]AXI_awsize;
  output AXI_awvalid;
  input [11:0]AXI_bid;
  output AXI_bready;
  input [1:0]AXI_bresp;
  input AXI_bvalid;
  input [31:0]AXI_rdata;
  input [11:0]AXI_rid;
  input AXI_rlast;
  output AXI_rready;
  input [1:0]AXI_rresp;
  input AXI_rvalid;
  output [31:0]AXI_wdata;
  output [11:0]AXI_wid;
  output AXI_wlast;
  input AXI_wready;
  output [3:0]AXI_wstrb;
  output AXI_wvalid;

blk_mem_axi2s s2axi (
  .clka(Sclk),    // input wire clka
  .ena(Ien),      // input wire ena
  .wea(s2a_wea),      // input wire [0 : 0] wea
  .addra(IAddr),  // input wire [4 : 0] addra
  .dina(Sin),    // input wire [31 : 0] dina
  .clkb(AXI_clk),    // input wire clkb
  .enb(s2a_en),      // input wire enb
  .addrb(s2a_addr),  // input wire [4 : 0] addrb
  .doutb(AXI_wdata)  // output wire [31 : 0] doutb
);

blk_mem_axi2s axi2s (
  .clka(AXI_clk),    // input wire clka
  .ena(a2s_en),      // input wire ena
  .wea(a2s_wea),      // input wire [0 : 0] wea
  .addra(a2s_addr),  // input wire [4 : 0] addra
  .dina(AXI_rdata),    // input wire [31 : 0] dina
  .clkb(Sclk),    // input wire clkb
  .enb(Oen),      // input wire enb
  .addrb(Oaddr),  // input wire [4 : 0] addrb
  .doutb(Sout)  // output wire [31 : 0] doutb
);

assign AXI_arlen = 4'hf;

endmodule