module cntSrc 
	(
		clk,
		rst,
		Cout
	);

	input clk,rst;
	output reg [15:0]Cout;

  parameter up = 1'b0;

always @(posedge clk or rst)
begin
	if( rst ) Cout <= 16'b0000;
	else begin
		if( up ) Cout <= Cout+1'b1;
		else Cout <= Cout-1'b1;
	end
end

endmodule
