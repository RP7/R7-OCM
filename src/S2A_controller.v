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
  // AXI Bus Signal
  AXI_clk,
  AXI_waddr,
  AXI_awvalid,
  AXI_awready,
  AXI_wready,
  AXI_wvalid,
  AXI_wlast,
  // Buffer read
  s2a_addr,
  s2a_en,
  // input counter
  s2a_cnt
);

  parameter ocm_haddr = 32'hfffc0000;
  parameter ocm_width = 16;
  
  parameter s0 = 3'd0;
  parameter s1 = 3'd1;
  parameter s2 = 3'd2;
  parameter s3 = 3'd3;

  input Sclk,rst,sync,Ien;
  output s2a_en;
  output reg[4:0] s2a_addr;
  output[4:0] Iaddr;
  
  input AXI_clk;
  input AXI_awready;
  input AXI_wready;

  output reg[31:0] AXI_waddr;
	output reg AXI_awvalid,AXI_wvalid,AXI_wlast;

  output[31:0] s2a_cnt;
  reg[35:0] cnt;
  reg start;

  reg start_d0,start_d1,axi_start;


assign Iaddr = cnt[4:0];
assign s2a_cnt = cnt[35:4];

always @(posedge Sclk or rst)
begin
  if( rst==1'b1 ) begin
    start <= 1'b0;
    cnt <= 36'h000000000;
  end
  else begin
  	if ( sync==1'b1 ) begin
      start <= 1'b0;
      cnt <= 36'h000000000;
  	end
  	else if( Ien==1'b1 ) begin
  	  cnt <= cnt + 1'b1;
  	  if( cnt[3:0]==4'hf ) begin
  	  	AXI_waddr[1:0] <= 2'b00;
  	  	AXI_waddr[31:2] <= ocm_haddr[31:2] + cnt[ocm_width-2-1+4:0+4];
  	  end
  	end
  	if( Ien==1'b1 && 
  		  cnt[3:0]==4'hf && 
  		  start==1'b0 ) start <= 1'b1;
  	else start <= 1'b0;
 	end
end

assign s2a_en = (AXI_wvalid & AXI_wready & ~AXI_wlast) | s2a_pre;

always @(posedge AXI_clk or rst)
begin
  if( rst==1'b1 ) begin
    start_d0      <= 1'b0;
    start_d1      <= 1'b0;
    axi_start     <= 1'b0;

    s2a_addr      <= 5'b00000;

    AXI_awvalid   <= 1'b0;
    AXI_wvalid    <= 1'b0;
    AXI_wlast     <= 1'b0;

    state         <= s0;
  end
  else begin
  	start_d0 <= start;
  	start_d1 <= start_d0;
  	axi_start <= (~start_d1) & start_d0;
  	if( axi_start==1'b1 ) begin
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
  					AXI_awvaild <= 1'b0;
  					s2a_addr[4] <= AXI_waddr[6];
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
