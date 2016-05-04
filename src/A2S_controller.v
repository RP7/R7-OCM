module A2S_controller(
	// system reset
  rst,
  // stream clk
  Sclk,
  // system sync(reset)
  sync,
  // Buffer read
  Oen,
  Oaddr,
  // AXI Bus Signal
  AXI_clk,
  AXI_raddr,
  AXI_arvalid,
  AXI_arready,
  AXI_rready,
  AXI_rvalid,
  AXI_rlast,
	// Buffer write  
  a2s_addr,
  a2s_en,
  // output counter
  a2s_cnt
);

  parameter ocm_haddr = 32'hfffc0000;
  parameter ocm_width = 16;
  
  parameter s0 = 3'd0;
  parameter s1 = 3'd1;
  parameter s2 = 3'd2;
  parameter s3 = 3'd3;

  input rst,Sclk,sync,Oen;
  output[4:0] Oaddr;

  input AXI_clk;
  output reg[31:0] AXI_raddr;
  input AXI_arready,AXI_rvalid;
  output reg AXI_rready,AXI_arvalid;

  input AXI_rlast;

  output reg[4:0] a2s_addr;
  output a2s_en;
  output [31:0]a2s_cnt;

assign Oaddr = cnt[4:0];
assign a2s_cnt = cnt[35:4];

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
  	else if( Oen==1'b1 ) begin
  	  cnt <= cnt + 1'b1;
  	  if( cnt[3:0]==4'hf ) begin
  	  	AXI_raddr[1:0] <= 2'b00;
  	  	AXI_raddr[31:2] <= ocm_haddr[31:2] + cnt[ocm_width-2-1+4:0+4];
  	  end
  	end
  	if( Oen==1'b1 && 
  		  cnt[3:0]==4'hf && 
  		  start==1'b0 ) start <= 1'b1;
  	else start <= 1'b0;
 	end
end

assign a2s_en = AXI_rvalid & AXI_rready;

always @(posedge AXI_clk or rst)
begin
  if( rst==1'b1 ) begin
    start_d0      <= 1'b0;
    start_d1      <= 1'b0;
    axi_start     <= 1'b0;

    a2s_addr      <= 5'b00000;

    AXI_arvalid   <= 1'b0;
    AXI_rready    <= 1'b0;
    
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
  				AXI_rready <= 1'b0;
  			end
  			s1 : begin
  				AXI_arvalid <= 1'b1;
  				if( AXI_arready==1'b1 && AXI_arvalid==1'b1 ) begin
  					state <= s2;
  					AXI_arvaild <= 1'b0;
  					a2s_addr[4] <= AXI_waddr[6];
  					a2s_addr[3:0] <= 4'h0;
  					AXI_rready <= 1'b1;
  				end
  			end
  			s2 : begin
  				if( a2s_en==1'b1 ) begin
  					a2s_addr[3:0] <= a2s_addr[3:0] + 1'b1;
    				if( a2s_addr[3:0]==4'hf ) begin
    					state <= s0;
    					AXI_rready <= 1'b0;
    					a2s_err <= AXI_rlast;
  				  end
  				end
  			end
  		endcase
  	end 
  end
end

endmodule
