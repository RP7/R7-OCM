module ad9361_1t1r
(
		AD9361_RX_Frame_P,			
		AD9361_RX_Frame_N,			
		AD9361_DATA_CLK_P,			
		AD9361_DATA_CLK_N, 			
		AD9361_RX_DATA_P,				
		AD9361_RX_DATA_N,				
		
		AD9361_TX_Frame_P,			
		AD9361_TX_Frame_N,			
		AD9361_FB_CLK_P,				
		AD9361_FB_CLK_N,				
		AD9361_TX_DATA_P,				
		AD9361_TX_DATA_N,

		clk,
		rst,
		rx_I,
		rx_Q,
		tx_I,
		tx_Q,
		rx_ce,
		tx_ce				
	);

	input  AD9361_RX_Frame_P;			//					: in  	std_logic;
	input  AD9361_RX_Frame_N;			//					: in 	std_logic;
	input  AD9361_DATA_CLK_P;			//					: in 	std_logic;
	input  AD9361_DATA_CLK_N;			// 					: in	std_logic;
	input  [5:0]AD9361_RX_DATA_P;	//					: in 	std_logic_vector(5 downto 0);
	input  [5:0]AD9361_RX_DATA_N;	//					: in 	std_logic_vector(5 downto 0);

	output AD9361_TX_Frame_P;			//					: out 	std_logic;
	output AD9361_TX_Frame_N;			//					: out 	std_logic;
	output AD9361_FB_CLK_P;				//					: out 	std_logic;
	output AD9361_FB_CLK_N;				//					: out	std_logic;
	output [5:0]AD9361_TX_DATA_P;	//					: out 	std_logic_vector(5 downto 0);
	output [5:0]AD9361_TX_DATA_N;	//					: out 	std_logic_vector(5 downto 0);

	output clk;
	input  rst;
	output reg [11:0]rx_I;
	output reg [11:0]rx_Q;
	input  [11:0]tx_I;
	input  [11:0]tx_Q;
	output reg rx_ce;
	output reg tx_ce;
	
	wire clk_out;
	wire [13:0]rx;

	reg [13:0]rx_h;
	reg [13:0]tx;
	reg [11:0]tx_I_reg;
	reg [11:0]tx_Q_reg;

ddr_rx rx_if (
  .data_in_from_pins_p({AD9361_RX_Frame_P,AD9361_RX_DATA_P}),  // input wire [6 : 0] data_in_from_pins_p
  .data_in_from_pins_n({AD9361_RX_Frame_N,AD9361_RX_DATA_N}),  // input wire [6 : 0] data_in_from_pins_n
  .clk_in_p(AD9361_DATA_CLK_P),                        // input wire clk_in_p
  .clk_in_n(AD9361_DATA_CLK_N),                        // input wire clk_in_n
  .io_reset(rst),                        // input wire io_reset
  .clk_out(clk_out),                          // output wire clk_out
  .data_in_to_device(rx)      // output wire [13 : 0] data_in_to_device
);
ddr_tx tx_if (
  .data_out_to_pins_p({AD9361_TX_Frame_P,AD9361_TX_DATA_P}),      // output wire [6 : 0] data_out_to_pins_p
  .data_out_to_pins_n({AD9361_TX_Frame_N,AD9361_TX_DATA_N}),      // output wire [6 : 0] data_out_to_pins_n
  .clk_in(clk_out),                              // input wire clk_in
  .data_out_from_device(tx),  // input wire [13 : 0] data_out_from_device
  .clk_reset(rst),                        // input wire clk_reset
  .io_reset(rst),                          // input wire io_reset
  .clk_to_pins_p(AD9361_FB_CLK_P),                // output wire clk_to_pins_p
  .clk_to_pins_n(AD9361_FB_CLK_N)                // output wire clk_to_pins_n
);
always @(posedge clk_out or posedge rst) begin
	if (rst) begin
		rx_h <= 14'h0;
		rx_I <= 12'h0;
		rx_Q <= 12'h0;
		rx_ce <= 1'b0;
	end
	else if (rx[13]==1'b1) begin
		rx_ce <= 1'b1;
		rx_h <= rx;
	end
	else if(rx_ce==1'b1) begin
		rx_ce <= 1'b0;
		rx_I[11:6] = rx_h[5:0];
		rx_Q[11:6] = rx_h[12:7];
		rx_I[5:0]  = rx[5:0];
		rx_Q[5:0]  = rx[12:7];
	end
end

assign clk = clk_out;

always @(posedge clk_out or posedge rst) begin
	if (rst) begin
		tx_ce    <= 1'b0;
		tx       <= 14'h0;
		tx_I_reg <= 12'h0;
		tx_Q_reg <= 12'h0;
	end
	else if (tx_ce==1'b1) begin
		tx_ce    <= 1'b0;
		tx_I_reg <= tx_I;
		tx_Q_reg <= tx_Q;
		tx[5:0]  <= tx_I[11:6];
		tx[12:7] <= tx_Q[11:6];
		tx[6]    <= 1'b1;
		tx[13]   <= 1'b1;
	end
	else begin
		tx_ce    <= 1'b1;
		tx[5:0]  <= tx_I_reg[5:0];
		tx[12:7] <= tx_Q_reg[5:0];
		tx[6]    <= 1'b0;
		tx[13]   <= 1'b0;
	end
end

endmodule
