`include "reg_define.v"

module AD9361REG
	(
		clk,
		rst,
		en,
		wen,
		din,
		dout,
		addr,
		ad9361_rstb,
		ad9361_en
	);

	parameter BASE = `AD9361REG_BASE;

	input clk,rst,en,wen;
	input [31:0]din;
	input [17:0]addr;

	output reg ad9361_en,ad9361_rstb;
	output [31:0]dout;
	
always @(posedge clk or posedge rst)
begin
	if(rst) begin
		ad9361_rstb <= 1'b1;
		ad9361_en   <= 1'b0;
	end	
	else if(clk) begin
		if( en==1'b1 ) begin
			// write
			if( wen==1'b1 ) begin
				case( addr )
					// define AD9361_RST      18'h100
					`AD9361_RST: ad9361_rstb  <= din[0];
					// define AD9361_EN       18'h110
					`AD9361_EN: ad9361_en 		<= din[0]; 
				endcase
			end
		end
	end
end	

assign dout = 32'h0;	

endmodule
