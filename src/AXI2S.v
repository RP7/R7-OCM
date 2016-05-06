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

wire [4:0] Iaddr,Oaddr,s2a_addr,a2s_addr;
wire s2a_en,s2a_wea,a2s_en,a2s_wea;
wire [31:0] s2a_cnt,a2s_cnt;
wire a2s_err;

assign s2a_wea = Ien;
assign a2s_wea = a2s_en;

blk_mem_axi2s s2axi (
  .ena(Ien),         // input wire ena
  .wea(s2a_wea),     // input wire [0 : 0] wea
  .addra(Iaddr),     // input wire [4 : 0] addra
  .dina(Sin),        // input wire [31 : 0] dina
  .clka(Sclk),       // input wire clka
  .clkb(AXI_clk),    // input wire clkb
  .enb(s2a_en),      // input wire enb
  .addrb(s2a_addr),  // input wire [4 : 0] addrb
  .doutb(AXI_wdata)  // output wire [31 : 0] doutb
);

blk_mem_axi2s axi2s (
  .clka(AXI_clk),    // input wire clka
  .ena(a2s_en),      // input wire ena
  .wea(a2s_wea),     // input wire [0 : 0] wea
  .addra(a2s_addr),  // input wire [4 : 0] addra
  .dina(AXI_rdata),  // input wire [31 : 0] dina
  .clkb(Sclk),       // input wire clkb
  .enb(Oen),         // input wire enb
  .addrb(Oaddr),     // input wire [4 : 0] addrb
  .doutb(Sout)       // output wire [31 : 0] doutb
);

assign AXI_arid      = 12'hfff;
assign AXI_arlen     = 4'hf;
assign AXI_arsize    = 3'b010;   //size: 4byte
assign AXI_arburst   = 2'b01;    //"01";    --incr
assign AXI_arlock    = 2'b00;    //"00";
assign AXI_arcache   = 4'h0;     //x"0";
assign AXI_arprot    = 3'b000;   //"000";
assign AXI_arqos     = 4'h0;     //x"0";

assign AXI_awid      = 12'hfff; 
assign AXI_awlen     = 4'hf;     //x"F"; burst length: 16
assign AXI_awsize    = 3'b010;   //size: 4byte     
assign AXI_awburst   = 2'b01;    //"01";    --incr            
assign AXI_awlock    = 2'b00;    //"00";
assign AXI_awcache   = 4'h0;     //x"0";
assign AXI_awprot    = 3'b000;   //"000";
assign AXI_awqos     = 4'h0;     //x"0";
assign AXI_bready    = 1'b1;     //'1';
 

S2A_controller #(.ocm_haddr(32'hfffc0000),.ocm_width(16)) cs2a(
  .Sclk(Sclk),
  .rst(rst),
  .sync(sync),
  .Ien(Ien),
  .Iaddr(Iaddr),
  .AXI_clk(AXI_clk),
  .AXI_awaddr(AXI_awaddr),
  .AXI_awvalid(AXI_awvalid),
  .AXI_awready(AXI_awready),
  .AXI_wready(AXI_wready),
  .AXI_wvalid(AXI_wvalid),
  .AXI_wlast(AXI_wlast),
  .s2a_addr(s2a_addr),
  .s2a_en(s2a_en),
  .s2a_cnt(s2a_cnt)
  );

A2S_controller #(.ocm_haddr(32'hfffc0000),.ocm_width(16)) ca2s(
  .rst(rst),
  .Sclk(Sclk),
  .sync(sync),
  .Oen(Oen),
  .Oaddr(Oaddr),
  .AXI_clk(AXI_clk),
  .AXI_araddr(AXI_araddr),
  .AXI_arvalid(AXI_arvalid),
  .AXI_arready(AXI_arready),
  .AXI_rready(AXI_rready),
  .AXI_rvalid(AXI_rvalid),
  .AXI_rlast(AXI_rlast),
  .a2s_addr(a2s_addr),
  .a2s_en(a2s_en),
  .a2s_cnt(a2s_cnt),
  .a2s_err(a2s_err)
  );

`ifdef TEST
ila_0 ILA_AIX (
  .clk(AXI_clk), // input wire clk

  .probe0(a2s_addr), // input wire [4:0]  probe0  
  .probe1(s2a_addr), // input wire [4:0]  probe1 
  .probe2(AXI_araddr), // input wire [31:0]  probe2 
  .probe3(AXI_awaddr), // input wire [31:0]  probe3 
  .probe4(AXI_arvalid), // input wire [0:0]  probe4 
  .probe5(AXI_arready), // input wire [0:0]  probe5 
  .probe6(AXI_rvalid), // input wire [0:0]  probe6 
  .probe7(AXI_rready), // input wire [0:0]  probe7 
  .probe8(AXI_rlast), // input wire [0:0]  probe8 
  .probe9(AXI_awvalid), // input wire [0:0]  probe9 
  .probe10(AXI_awready), // input wire [0:0]  probe10 
  .probe11(AXI_wready), // input wire [0:0]  probe11 
  .probe12(AXI_wvalid), // input wire [0:0]  probe12 
  .probe13(AXI_wlast), // input wire [0:0]  probe13 
  .probe14(a2s_en), // input wire [0:0]  probe14 
  .probe15(s2a_en) // input wire [0:0]  probe15
);

ila_0 ILA_S (
  .clk(Sclk), // input wire clk

  .probe0(Iaddr), // input wire [4:0]  probe0  
  .probe1(Oaddr), // input wire [4:0]  probe1 
  .probe2(Sin), // input wire [31:0]  probe2 
  .probe3(Sout),
  .probe4(a2s_err), // input wire [0:0]  probe4 
  .probe5(s2a_cnt[0]), // input wire [0:0]  probe5 
  .probe6(s2a_cnt[1]), // input wire [0:0]  probe6 
  .probe7(s2a_cnt[2]), // input wire [0:0]  probe7 
  .probe8(s2a_cnt[3]), // input wire [0:0]  probe8 
  .probe9(s2a_cnt[4]), // input wire [0:0]  probe9 
  .probe10(s2a_cnt[5]), // input wire [0:0]  probe10 
  .probe11(s2a_cnt[6]), // input wire [0:0]  probe11 
  .probe12(s2a_cnt[7]), // input wire [0:0]  probe12 
  .probe13(s2a_cnt[8]), // input wire [0:0]  probe13 
  .probe14(s2a_cnt[9]), // input wire [0:0]  probe14 
  .probe15(s2a_cnt[10]) // input wire [0:0]  probe15
);
`endif
endmodule