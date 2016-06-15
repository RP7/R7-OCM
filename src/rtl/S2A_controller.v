module S2A_controller(
	// system reset
  rst,
  // stream clk
  Sclk,
  // system sync(reset)
  sync,
  // Buffer write
  Ien,
  Iaddr,

  ibase,
  isize,

  iacnt,
  ibcnt,

  // AXI Bus Signal
  AXI_clk,
  AXI_rst_n,
  AXI_awaddr,
  AXI_awvalid,
  AXI_awready,
  AXI_wready,
  AXI_wvalid,
  AXI_wlast,
  // Buffer read
  s2a_addr,
  s2a_en
);

  parameter s0 = 3'd0;
  parameter s1 = 3'd1;
  parameter s2 = 3'd2;
  parameter s3 = 3'd3;

  input Sclk,rst,sync,Ien;
  output s2a_en;
  output reg[4:0] s2a_addr;
  output[4:0] Iaddr;
  
  input AXI_clk;
  input AXI_rst_n;
  input AXI_awready;
  input AXI_wready;

  output reg[31:0] AXI_awaddr;
  output reg AXI_awvalid,AXI_wvalid,AXI_wlast;

  reg[21:0] cnt;
  reg[31:0] bcnt;
  reg start;

  wire axi_start;
  reg [2:0]state;
  reg s2a_pre;
  reg [31:0]AXI_awaddr_reg;

  input [31:0]ibase;
  input [23:6]isize;

  output [23:6]iacnt;

  output [31:0]ibcnt;

assign Iaddr = cnt[4:0];
assign iacnt[23:6] = cnt[21:4];
assign ibcnt = bcnt;

always @(posedge Sclk or posedge rst)
begin
  if( rst==1'b1 ) begin
    start <= 1'b0;
    cnt <= 22'h0;
    bcnt <= 32'h0;
  end
  else begin
  	if ( sync==1'b1 ) begin
      start <= 1'b0;
      cnt <= 22'h0;
      bcnt <= 32'h0;
  	end
  	else if( Ien==1'b1 ) begin
  	  if( cnt[3:0]==4'hf ) begin
  	  	AXI_awaddr_reg[5:0] <= 6'b000000;
  	  	AXI_awaddr_reg[31:6] <= ibase[31:6] + cnt[21:4];
        cnt[3:0] <= 4'h0;
        if( cnt[21:4]==(isize[23:6]-1'b1) ) begin
          cnt[21:4] <= 18'h0;
          bcnt <= bcnt + 32'h1;
        end
        else cnt[21:4] <= cnt[21:4]+18'h1;
      end
      else cnt[3:0] <= cnt[3:0] + 4'h1;
  	end
  	if( Ien==1'b1 && 
  		  cnt[3:0]==4'hf && 
  		  start==1'b0 ) start <= 1'b1;
  	else start <= 1'b0;
 	end
end

assign s2a_en = (AXI_wvalid & AXI_wready & ~AXI_wlast) | s2a_pre;

edgesync #(.e("pos")) start_sync
(   .clk(AXI_clk)
  , .async(start)
  , .sync(axi_start)
);

always @(posedge AXI_clk)
begin
  if( !AXI_rst_n ) begin
    s2a_addr      <= 5'b00000;
    AXI_awvalid   <= 1'b0;
    AXI_wvalid    <= 1'b0;
    AXI_wlast     <= 1'b0;
    AXI_awaddr    <= ibase;
    state         <= s0;
  end
  else begin
  	if( axi_start==1'b1 ) begin
      AXI_awaddr <= AXI_awaddr_reg;
  		state <= s1;
  	end
  	else begin
  		case( state )
  			s0 : begin
  				AXI_wlast <= 1'b0;
  				AXI_awvalid <= 1'b0;
  			end
  			s1 : begin
  				AXI_awvalid <= 1'b1;
  				if( AXI_awready==1'b1 && AXI_awvalid==1'b1 ) begin
  					state <= s2;
  					AXI_awvalid <= 1'b0;
  					s2a_addr[4] <= AXI_awaddr[6];
  					s2a_addr[3:0] <= 4'h0;
  					s2a_pre <= 1'b1;
  				end
  			end
  			s2 : begin
  				s2a_pre <= 1'b0;
  				AXI_wvalid <= 1'b1;
  				if( s2a_en==1'b1 ) begin
  					s2a_addr[3:0] <= s2a_addr[3:0] + 1'b1;
 					if( s2a_addr[3:0]==4'hf ) begin
 						AXI_wlast <= 1'b1;
 						state <= s3;
  					end
  				end
  			end
  			s3 : begin
  				if( AXI_wvalid==1'b1 && AXI_wready==1'b1 ) begin
  					AXI_wlast <= 1'b0;
  					AXI_wvalid <= 1'b0;
  					state <= s0;
  				end
  			end
  		endcase
  	end 
  end
end

endmodule
