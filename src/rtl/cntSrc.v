module cntSrc 
	(
		clk,
		en,
		rst,
		Cout
	);

	input clk,rst,en;
	output reg [31:0]Cout;

  parameter up = 1'b0;

always @(posedge clk or posedge rst)
begin
	if( rst ) Cout <= 32'h0;
	else if(en) begin
		if( up ) Cout <= Cout+1'b1;
		else Cout <= Cout-1'b1;
	end
end

endmodule
