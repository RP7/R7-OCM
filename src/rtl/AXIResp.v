module AXIResp
(
	clk,
	valid,
	resp,
	ready,
	respOut
	);

input clk,valid;
input [1:0]resp;
output ready;
output [31:0]respOut;

reg [7:0]ok;
reg [7:0]exok;
reg [7:0]slverr;
reg [7:0]decerr;

always @(posedge clk) begin
	if (valid) begin
		case(resp)
			2'b00: ok<=ok+1'b1;
			2'b01: exok<=exok+1'b1;
			2'b10: slverr<=slverr+1'b1;
			2'b11: decerr<=decerr+1'b1;
		endcase
	end
end

assign respOut = {decerr,slverr,exok,ok};
assign ready = 1'b1;

endmodule
