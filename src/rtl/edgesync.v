/*--------------------------
 *                        *
 *                        *
 *                        *
--------------------------*/
module edgesync
(
	clk,
	async,
	sync
);

parameter e = "pos";

input clk,async;
output reg sync;
reg d0,d1;

always @(posedge clk)
begin
  	d0 <= async;
  	d1 <= d0;
  	if (e=="pos") sync <= (~d1) & d0;	
  	else sync <= (~d0) & d1;
end

endmodule
