`include "reg_define.v"

module CBusReadMerge
	(
		clk,
		rst,
		en,
		addr,
		dout,
		axi2s_dout,
		ad9361_dout
	);

	input clk,rst,en;
	input [31:0]axi2s_dout;
	input [31:0]ad9361_dout;
	
	input [17:0]addr;
	output reg[31:0] dout;

always @(posedge clk or posedge rst) begin
	if (rst) begin
		dout <= 32'h0;
	end
	else if (en==1'b1) begin
		case( addr&18'h3ff00 )
			`AXI2SREG_BASE:  dout<=axi2s_dout;
			`AD9361REG_BASE: dout<=ad9361_dout;
			default: dout<=32'h0;
		endcase
	end
end

endmodule
