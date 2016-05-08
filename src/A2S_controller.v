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

  obase,
  osize,

  oacnt,
  obcnt,

  // AXI Bus Signal
  AXI_clk,
  AXI_araddr,
  AXI_arvalid,
  AXI_arready,
  AXI_rready,
  AXI_rvalid,
  AXI_rlast,
	// Buffer write  
  a2s_addr,
  a2s_en,
  // output counter
  a2s_cnt,
  a2s_err
);

  parameter s0 = 3'd0;
  parameter s1 = 3'd1;
  parameter s2 = 3'd2;
  parameter s3 = 3'd3;

  input rst,Sclk,sync,Oen;
  output[4:0] Oaddr;

  input AXI_clk;
  output reg[31:0] AXI_araddr;
  input AXI_arready,AXI_rvalid;
  output reg AXI_rready,AXI_arvalid;
  output reg a2s_err;

  input AXI_rlast;

  output reg[4:0] a2s_addr;
  output a2s_en;
  
  reg[21:0] cnt;
  reg[31:0] bcnt;

  reg start,start_d0,start_d1;
  reg axi_start;
  reg [2:0]state;
  reg [31:0]AXI_araddr_reg;

  input [31:0]obase;
  input [23:6]osize;

  output [23:6]oacnt;
  output [31:0]obcnt;


assign Oaddr = cnt[4:0];
assign oacnt[23:6] = cnt[21:4];
assign obcnt <= bcnt;

always @(posedge Sclk or posedge rst)
begin
  if( rst==1'b1 ) begin
    start <= 1'b0;
    cnt <= 22'h0;
    bcnt <= 32'h0;
  end
  else if(Sclk) begin
  	if ( sync==1'b1 ) begin
      start <= 1'b0;
      cnt <= 22'h0;
      bcnt <= 32'h0;
  	end
  	else if( Oen==1'b1 ) begin
      if( cnt[3:0]==4'hf ) begin
        AXI_araddr_reg[5:0] <= 6'b000000;
        AXI_araddr_reg[31:6] <= obase[31:6] + cnt[21:4];
        cnt[3:0] <= 4'h0;
        if( cnt[21:4]==(osize[23:6]-1'b1) ) begin
          cnt[21:4] <= 18'h0;
          bcnt <= bcnt + 32'h1;
        end
        else cnt[21:4] <= cnt[21:4]+18'h1;
      end
      else cnt[3:0] <= cnt[3:0] + 4'h1;
  	end
  	if( Oen==1'b1 && cnt[3:0]==4'hf && start==1'b0 ) start <= 1'b1;
  	else start <= 1'b0;
 	end
end

assign a2s_en = AXI_rvalid & AXI_rready;

always @(posedge AXI_clk or posedge rst)
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
  else if(AXI_clk) begin
  	start_d0 <= start;
  	start_d1 <= start_d0;
  	axi_start <= (~start_d1) & start_d0;
  	if( axi_start==1'b1 ) begin
  		state <= s1;
      AXI_araddr <= AXI_araddr_reg;
  	end
  	else begin
  		case( state )
  			s0 : begin
          AXI_rready <= AXI_rvalid;
  			end
  			s1 : begin
  				AXI_arvalid <= 1'b1;
  				if( AXI_arready==1'b1 && AXI_arvalid==1'b1 ) begin
  					state <= s2;
  					AXI_arvalid <= 1'b0;
  					a2s_addr[4] <= AXI_araddr[6];
  					a2s_addr[3:0] <= 4'h0;
  					AXI_rready <= 1'b1;
  				end
  			end
  			s2 : begin
  				if( a2s_en==1'b1 ) begin
  					a2s_addr[3:0] <= a2s_addr[3:0] + 1'b1;
    				if( AXI_rlast==1'b1 ) begin
    					state <= s0;
    					AXI_rready <= 1'b0;
              if( a2s_addr[3:0]==4'hf ) a2s_err <= 1'b0;
              else a2s_err <= 1'b1;
  				  end
  				end
  			end
  		endcase
  	end 
  end
end

endmodule
