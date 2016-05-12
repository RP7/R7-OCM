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
		ad9361_en,
		ad9361_tx_rx,
    ad9361_en_agc,
    rf_ctrl_in,
    pa_en,
    rf_sw
	);

	parameter BASE = `AD9361REG_BASE;

	input clk,rst,en,wen;
	input [31:0]din;
	input [17:0]addr;

	output reg ad9361_en,ad9361_rstb;
	output [31:0]dout;
	output reg ad9361_tx_rx,ad9361_en_agc;
	output reg [3:0]rf_ctrl_in;
	output reg pa_en,rf_sw;
	
always @(posedge clk or posedge rst)
begin
	if(rst) begin
		ad9361_rstb   <= 1'b1;
		ad9361_en     <= 1'b0;
		ad9361_tx_rx  <= 1'b0;
		ad9361_en_agc <= 1'b0;
		rf_ctrl_in    <= 1'h0;
		rf_sw         <= 1'b0;
		pa_en         <= 1'b0;
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
					// define AD9361_TX_RX    18'h120
					`AD9361_TX_RX: ad9361_tx_rx <= din[0];
					// define AD9361_EN_AGC    18'h130
					`AD9361_EN_AGC: ad9361_en_agc <= din[0];
					// define RF_CTRL_IN    18'h140
					`RF_CTRL_IN: rf_ctrl_in <= din[3:0];
					// define RF_SW    18'h150
					`RF_SW: rf_sw <= din[0];
					// define PA_EN    18'h160
					`PA_EN: pa_en <= din[0];
				endcase
			end
		end
	end
end	

assign dout = 32'h0;	

endmodule
