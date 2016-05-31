`include "reg_define.v"
`include "version.v"

module AXI2SREG
	(
		clk,
		rst,
		en,
		wen,
		din,
		dout,
		addr,
		ien,
		oen,
		async,
		tddmode,
		ibase,
		isize,
		obase,
		osize,
		frame_len,
		frame_adj,
		tstart,
		tend,
		rstart,
		rend,
		iacnt,
		ibcnt,
		oacnt,
		obcnt,
		test,
		axiwresp,
    axirresp,
    axistatus,
    axiraddr,
    axiwaddr,
		adj_pending
	);

	parameter BASE = `AXI2SREG_BASE;

	input clk,rst,en,wen;
	input [31:0]din;
	input [17:0]addr;

	output reg ien,oen,async,tddmode;
	output reg [31:0]dout;
	output reg [31:0]ibase;
	output reg [31:0]obase;
	output reg [23:6]isize;
	output reg [23:6]osize;

	output reg [23:0]frame_len;
	output reg [23:0]tstart;
	output reg [23:0]tend;
	output reg [23:0]rstart;
	output reg [23:0]rend;
	
	output reg [23:0]frame_adj;

	output reg test;

	input [23:6]iacnt;
	input [23:6]oacnt;

	input [31:0]ibcnt;
	input [31:0]obcnt;

	input [31:0]axiwresp;
	input [31:0]axirresp;
	input [31:0]axistatus;

	input [31:0]axiraddr;
	input [31:0]axiwaddr;

	input adj_pending;
  wire [159:0]version_git;

  reg [31:0]ibcnt_reg;
  reg [31:0]obcnt_reg;
	
always @(posedge clk or posedge rst)
begin
	if(rst) begin
		ien       <= 1'b0;
		oen       <= 1'b0;
		tddmode   <= 1'b0;
		ibase     <= 32'hfffc0000;
		isize     <= 18'h400;
		obase     <= 32'hfffd0000;
		osize     <= 18'h400;
		frame_len <= 24'd1920;
		frame_len <= 24'd1920;
		tstart    <= 24'h0;
		tend      <= 24'd1919;
		rstart    <= 24'h0;
		rend      <= 24'd1919;
		test  		<= 1'b0;
	end	
	else if(clk) begin
		if( en==1'b1 ) begin
			// write
			if( wen==1'b1 ) begin
				case( addr )
					// define AXI2S_EN        18'h00
					`AXI2S_EN: begin
						ien <= din[0];
						oen <= din[1];
						async <= din[2];
						tddmode <= din[3];
					end
					// define AXI2S_TEST        18'h04
					`AXI2S_TEST: begin
						test <= din[0];
					end
					// define AXI2S_IBASE     18'h10
					`AXI2S_IBASE: begin
						ibase <= din;
					end
					// define AXI2S_ISIZE     18'h14
					`AXI2S_ISIZE: begin
						isize <= din[23:6];
					end
					// define AXI2S_OBASE     18'h18
					`AXI2S_OBASE: begin
						obase <= din;
					end
					// define AXI2S_OSIZE     18'h1C
					`AXI2S_OSIZE: begin
						osize <= din[23:6];
					end
					// define FRAME_LEN       18'h20
					`FRAME_LEN: begin
						frame_len <= din[23:0];
					end
					// define FRAME_ADJ       18'h24
					`FRAME_ADJ: begin
						frame_adj <= din[23:0];
					end
					// define TSTART          18'h30
					`TSTART: begin
						tstart <= din[23:0];
					end
					// define TEND            18'h34
					`TEND: begin
						tend <= din[23:0];
					end
					// define RSTART          18'h38
					`RSTART: begin
						rstart <= din[23:0];
					end
					// define REND            18'h3C
					`REND: begin
						rend <= din[23:0];
					end
				endcase
			end
		end
	end
end

always @(posedge clk) begin
	if(addr[17:8]==BASE[17:8] && en==1'b1 ) begin
		case( addr )
			// define AXI2S_IACNT     18'h10
			`AXI2S_IACNT: begin
				ibcnt_reg <= ibcnt;
			end
			// define AXI2S_OACNT     18'h18
			`AXI2S_OACNT: begin
				obcnt_reg <= obcnt;
			end
		endcase
	end
end

always @(*) begin
	if(addr[17:8]==BASE[17:8] && en==1'b1 ) begin
		case( addr )
			// define AXI2S_STATE     18'h00
			`AXI2S_STATE: begin
				dout[0] <= ien;
				dout[1] <= oen;
				dout[2] <= tddmode;
				dout[3] <= adj_pending;
				dout[31:4] <= 28'd0;
			end
			
			// define AXI2S_IACNT     18'h10
			`AXI2S_IACNT: begin
				dout[23:6] <= iacnt;
				dout[31:24] <= 8'd0;
				dout[5:0] <= 6'd0;
			end
			// define AXI2S_IBCNT     18'h14
			`AXI2S_IBCNT: begin
				dout <= ibcnt_reg;
			end
			// define AXI2S_OACNT     18'h18
			`AXI2S_OACNT: begin
				dout[23:6] <= oacnt;
				dout[31:24] <= 8'd0;
				dout[5:0] <= 6'd0;
			end
			// define AXI2S_OBCNT     18'h1c
			`AXI2S_OBCNT: begin
				dout <= obcnt_reg;
			end
`ifdef DEBUG
			// define AXI_RRESP       18'h20
			`AXI_RRESP: begin
				dout <= axirresp;
			end
			// define AXI_WRESP       18'h24
			`AXI_WRESP: begin
				dout <= axiwresp;
			end
			// define AXI_STATUS      18'h28
			`AXI_STATUS: begin
				dout <= axistatus;
			end
			// define AXI_RADDR       18'h30
			`AXI_RADDR: begin
				dout <= axiraddr;
			end
			// define AXI_WADDR       18'h34
			`AXI_WADDR: begin
				dout <= axiwaddr;
			end
`endif			
			// define VER_MAJOR       18'h40
			`VER_MAJOR: begin
				dout <= `VERSION_MAJOR;
			end
			// define VER_MINOR0       18'h50
     `VER_MINOR0: begin
      	dout <= version_git[31:0];
      end
			// define VER_MINOR1       18'h54
     `VER_MINOR1: begin
      	dout <= version_git[63:32];
      end
			// define VER_MINOR2       18'h58
     `VER_MINOR2: begin
      	dout <= version_git[95:64];
      end
			// define VER_MINOR3       18'h5c
     `VER_MINOR3: begin
      	dout <= version_git[127:96];
      end
			// define VER_MINOR4       18'h60
     `VER_MINOR4: begin
      	dout <= version_git[159:128];
      end
		endcase
	end
	else dout <= 32'h0;	
end

assign version_git = `VERSION; 

endmodule


