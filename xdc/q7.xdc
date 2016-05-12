
set_property PACKAGE_PIN D15 [get_ports SYS_CLK]
set_property IOSTANDARD LVCMOS18 [get_ports SYS_CLK]
create_clock -period 40.000 -name SYS_CLK [get_ports SYS_CLK]

set_property PACKAGE_PIN A15 [get_ports {RF_CTRL_IN[0]}]
set_property IOSTANDARD LVCMOS18 [get_ports {RF_CTRL_IN[0]}]
#	AD9361-ctrl
set_property PACKAGE_PIN B15 [get_ports {RF_CTRL_IN[1]}]
set_property IOSTANDARD LVCMOS18 [get_ports {RF_CTRL_IN[1]}]
#	AD9361-ctrl
set_property PACKAGE_PIN A14 [get_ports {RF_CTRL_IN[2]}]
set_property IOSTANDARD LVCMOS18 [get_ports {RF_CTRL_IN[2]}]
#	AD9361-ctrl
set_property PACKAGE_PIN B14 [get_ports {RF_CTRL_IN[3]}]
set_property IOSTANDARD LVCMOS18 [get_ports {RF_CTRL_IN[3]}]

set_property IOSTANDARD LVCMOS33 [get_ports PA_EN]
set_property PACKAGE_PIN AE11 [get_ports PA_EN]

set_property IOSTANDARD LVCMOS33 [get_ports RF_SW]
set_property PACKAGE_PIN AE10 [get_ports RF_SW]


set_property PACKAGE_PIN K2 [get_ports {TEST_LED[0]}]
set_property IOSTANDARD LVCMOS18 [get_ports {TEST_LED[0]}]
set_property PACKAGE_PIN K1 [get_ports {TEST_LED[1]}]
set_property IOSTANDARD LVCMOS18 [get_ports {TEST_LED[1]}]
set_property PACKAGE_PIN H2 [get_ports {TEST_LED[2]}]
set_property IOSTANDARD LVCMOS18 [get_ports {TEST_LED[2]}]
set_property PACKAGE_PIN G1 [get_ports {TEST_LED[3]}]
set_property IOSTANDARD LVCMOS18 [get_ports {TEST_LED[3]}]

set_property PACKAGE_PIN F10 [get_ports AD9361_SPI_CLK]
set_property IOSTANDARD LVCMOS18 [get_ports AD9361_SPI_CLK]

set_property PACKAGE_PIN B6 [get_ports AD9361_SPI_ENB]
set_property IOSTANDARD LVCMOS18 [get_ports AD9361_SPI_ENB]

set_property PACKAGE_PIN H7 [get_ports AD9361_SPI_DI]
set_property IOSTANDARD LVCMOS18 [get_ports AD9361_SPI_DI]

set_property PACKAGE_PIN B12 [get_ports AD9361_SPI_DO]
set_property IOSTANDARD LVCMOS18 [get_ports AD9361_SPI_DO]

set_property PACKAGE_PIN C11 [get_ports AD9361_RST]
set_property IOSTANDARD LVCMOS18 [get_ports AD9361_RST]

set_property PACKAGE_PIN A5 [get_ports AD9361_EN]
set_property IOSTANDARD LVCMOS18 [get_ports AD9361_EN]

set_property PACKAGE_PIN H6 [get_ports AD9361_Tx_Rx]
set_property IOSTANDARD LVCMOS18 [get_ports AD9361_Tx_Rx]

set_property PACKAGE_PIN E10 [get_ports AD9361_EN_AGC]
set_property IOSTANDARD LVCMOS18 [get_ports AD9361_EN_AGC]

set_property IOSTANDARD LVDS [get_ports AD9361_TX_Frame_P]
set_property PACKAGE_PIN D5 [get_ports AD9361_TX_Frame_N]
set_property IOSTANDARD LVDS [get_ports AD9361_TX_Frame_N]

set_property IOSTANDARD LVDS [get_ports AD9361_FB_CLK_P]
set_property PACKAGE_PIN G5 [get_ports AD9361_FB_CLK_N]
set_property IOSTANDARD LVDS [get_ports AD9361_FB_CLK_N]

set_property IOSTANDARD LVDS [get_ports {AD9361_TX_DATA_P[0]}]
set_property PACKAGE_PIN D8 [get_ports {AD9361_TX_DATA_N[0]}]
set_property IOSTANDARD LVDS [get_ports {AD9361_TX_DATA_N[0]}]

set_property IOSTANDARD LVDS [get_ports {AD9361_TX_DATA_P[1]}]
set_property PACKAGE_PIN E8 [get_ports {AD9361_TX_DATA_N[1]}]
set_property IOSTANDARD LVDS [get_ports {AD9361_TX_DATA_N[1]}]

set_property IOSTANDARD LVDS [get_ports {AD9361_TX_DATA_P[2]}]
set_property PACKAGE_PIN A7 [get_ports {AD9361_TX_DATA_N[2]}]
set_property IOSTANDARD LVDS [get_ports {AD9361_TX_DATA_N[2]}]

set_property IOSTANDARD LVDS [get_ports {AD9361_TX_DATA_P[3]}]
set_property PACKAGE_PIN A8 [get_ports {AD9361_TX_DATA_N[3]}]
set_property IOSTANDARD LVDS [get_ports {AD9361_TX_DATA_N[3]}]

set_property IOSTANDARD LVDS [get_ports {AD9361_TX_DATA_P[4]}]
set_property PACKAGE_PIN B9 [get_ports {AD9361_TX_DATA_N[4]}]
set_property IOSTANDARD LVDS [get_ports {AD9361_TX_DATA_N[4]}]

set_property IOSTANDARD LVDS [get_ports {AD9361_TX_DATA_P[5]}]
set_property PACKAGE_PIN A10 [get_ports {AD9361_TX_DATA_N[5]}]
set_property IOSTANDARD LVDS [get_ports {AD9361_TX_DATA_N[5]}]

set_property IOSTANDARD LVDS [get_ports AD9361_RX_Frame_P]
set_property DIFF_TERM TRUE [get_ports AD9361_RX_Frame_P]
set_property PACKAGE_PIN C6 [get_ports AD9361_RX_Frame_N]
set_property IOSTANDARD LVDS [get_ports AD9361_RX_Frame_N]
set_property DIFF_TERM TRUE [get_ports AD9361_RX_Frame_N]

set_property IOSTANDARD LVDS [get_ports AD9361_DATA_CLK_P]
set_property PACKAGE_PIN C7 [get_ports AD9361_DATA_CLK_N]
set_property IOSTANDARD LVDS [get_ports AD9361_DATA_CLK_N]

set_property IOSTANDARD LVDS [get_ports {AD9361_RX_DATA_N[0]}]
set_property DIFF_TERM TRUE [get_ports {AD9361_RX_DATA_N[0]}]
set_property PACKAGE_PIN F5 [get_ports {AD9361_RX_DATA_P[0]}]
set_property IOSTANDARD LVDS [get_ports {AD9361_RX_DATA_P[0]}]
set_property DIFF_TERM TRUE [get_ports {AD9361_RX_DATA_P[0]}]

set_property IOSTANDARD LVDS [get_ports {AD9361_RX_DATA_N[1]}]
set_property DIFF_TERM TRUE [get_ports {AD9361_RX_DATA_N[1]}]
set_property PACKAGE_PIN A4 [get_ports {AD9361_RX_DATA_P[1]}]
set_property IOSTANDARD LVDS [get_ports {AD9361_RX_DATA_P[1]}]
set_property DIFF_TERM TRUE [get_ports {AD9361_RX_DATA_P[1]}]

set_property IOSTANDARD LVDS [get_ports {AD9361_RX_DATA_N[2]}]
set_property DIFF_TERM TRUE [get_ports {AD9361_RX_DATA_N[2]}]
set_property PACKAGE_PIN C4 [get_ports {AD9361_RX_DATA_P[2]}]
set_property IOSTANDARD LVDS [get_ports {AD9361_RX_DATA_P[2]}]
set_property DIFF_TERM TRUE [get_ports {AD9361_RX_DATA_P[2]}]

set_property IOSTANDARD LVDS [get_ports {AD9361_RX_DATA_N[3]}]
set_property DIFF_TERM TRUE [get_ports {AD9361_RX_DATA_N[3]}]
set_property PACKAGE_PIN C2 [get_ports {AD9361_RX_DATA_P[3]}]
set_property IOSTANDARD LVDS [get_ports {AD9361_RX_DATA_P[3]}]
set_property DIFF_TERM TRUE [get_ports {AD9361_RX_DATA_P[3]}]

set_property IOSTANDARD LVDS [get_ports {AD9361_RX_DATA_N[4]}]
set_property DIFF_TERM TRUE [get_ports {AD9361_RX_DATA_N[4]}]
set_property PACKAGE_PIN B2 [get_ports {AD9361_RX_DATA_P[4]}]
set_property IOSTANDARD LVDS [get_ports {AD9361_RX_DATA_P[4]}]
set_property DIFF_TERM TRUE [get_ports {AD9361_RX_DATA_P[4]}]

set_property IOSTANDARD LVDS [get_ports {AD9361_RX_DATA_N[5]}]
set_property DIFF_TERM TRUE [get_ports {AD9361_RX_DATA_N[5]}]
set_property PACKAGE_PIN B5 [get_ports {AD9361_RX_DATA_P[5]}]
set_property IOSTANDARD LVDS [get_ports {AD9361_RX_DATA_P[5]}]
set_property DIFF_TERM TRUE [get_ports {AD9361_RX_DATA_P[5]}]

create_clock -period 6.667 -name AD9361_DATA_CLK_P [get_ports AD9361_DATA_CLK_P]
create_clock -period 6.667 -name AD9361_DATA_CLK_N [get_ports AD9361_DATA_CLK_N]
set_input_delay -clock [get_clocks AD9361_DATA_CLK_P] -max 1.250 [get_ports {AD9361_RX_DATA_P[0] AD9361_RX_DATA_P[1] AD9361_RX_DATA_P[2] AD9361_RX_DATA_P[3] AD9361_RX_DATA_P[4] AD9361_RX_DATA_P[5] AD9361_RX_Frame_P}]
set_input_delay -clock [get_clocks AD9361_DATA_CLK_P] -clock_fall -max -add_delay 1.250 [get_ports {AD9361_RX_DATA_P[0] AD9361_RX_DATA_P[1] AD9361_RX_DATA_P[2] AD9361_RX_DATA_P[3] AD9361_RX_DATA_P[4] AD9361_RX_DATA_P[5] AD9361_RX_Frame_P}]
set_input_delay -clock [get_clocks AD9361_DATA_CLK_P] -min 0.250 [get_ports {AD9361_RX_DATA_P[0] AD9361_RX_DATA_P[1] AD9361_RX_DATA_P[2] AD9361_RX_DATA_P[3] AD9361_RX_DATA_P[4] AD9361_RX_DATA_P[5] AD9361_RX_Frame_P}]
set_input_delay -clock [get_clocks AD9361_DATA_CLK_P] -clock_fall -min -add_delay 0.250 [get_ports {AD9361_RX_DATA_P[0] AD9361_RX_DATA_P[1] AD9361_RX_DATA_P[2] AD9361_RX_DATA_P[3] AD9361_RX_DATA_P[4] AD9361_RX_DATA_P[5] AD9361_RX_Frame_P}]
set_input_delay -clock [get_clocks AD9361_DATA_CLK_N] -max 1.250 [get_ports {AD9361_DATA_CLK_N[0] AD9361_DATA_CLK_N[1] AD9361_DATA_CLK_N[2] AD9361_DATA_CLK_N[3] AD9361_DATA_CLK_N[4] AD9361_DATA_CLK_N[5] AD9361_RX_Frame_N}]
set_input_delay -clock [get_clocks AD9361_DATA_CLK_N] -clock_fall -max -add_delay 1.250 [get_ports {AD9361_DATA_CLK_N[0] AD9361_DATA_CLK_N[1] AD9361_DATA_CLK_N[2] AD9361_DATA_CLK_N[3] AD9361_DATA_CLK_N[4] AD9361_DATA_CLK_N[5] AD9361_RX_Frame_N}]
set_input_delay -clock [get_clocks AD9361_DATA_CLK_N] -min 0.250 [get_ports {AD9361_DATA_CLK_N[0] AD9361_DATA_CLK_N[1] AD9361_DATA_CLK_N[2] AD9361_DATA_CLK_N[3] AD9361_DATA_CLK_N[4] AD9361_DATA_CLK_N[5] AD9361_RX_Frame_N}]
set_input_delay -clock [get_clocks AD9361_DATA_CLK_N] -clock_fall -min -add_delay 0.250 [get_ports {AD9361_DATA_CLK_N[0] AD9361_DATA_CLK_N[1] AD9361_DATA_CLK_N[2] AD9361_DATA_CLK_N[3] AD9361_DATA_CLK_N[4] AD9361_DATA_CLK_N[5] AD9361_RX_Frame_N}]


# GMII

# GMII_GTXCLK
set_property PACKAGE_PIN AC23 [get_ports GMII_GTXCLK]
set_property IOSTANDARD LVCMOS33 [get_ports GMII_GTXCLK]
# GMII_TXCLK
set_property PACKAGE_PIN AD23 [get_ports GMII_TXCLK]
set_property IOSTANDARD LVCMOS33 [get_ports GMII_TXCLK]
# GMII_TX_EN
set_property PACKAGE_PIN AE22 [get_ports GMII_TX_EN]
set_property IOSTANDARD LVCMOS33 [get_ports GMII_TX_EN]
# GMII_TX_ER
set_property PACKAGE_PIN AF22 [get_ports GMII_TX_ER]
set_property IOSTANDARD LVCMOS33 [get_ports GMII_TX_ER]
# GMII_TXD[0..7]
set_property PACKAGE_PIN AF23 [get_ports {GMII_TXD[0]}]
set_property IOSTANDARD LVCMOS33 [get_ports {GMII_TXD[0]}]
set_property PACKAGE_PIN AE23 [get_ports {GMII_TXD[1]}]
set_property IOSTANDARD LVCMOS33 [get_ports {GMII_TXD[1]}]
set_property PACKAGE_PIN AF24 [get_ports {GMII_TXD[2]}]
set_property IOSTANDARD LVCMOS33 [get_ports {GMII_TXD[2]}]
set_property PACKAGE_PIN AF25 [get_ports {GMII_TXD[3]}]
set_property IOSTANDARD LVCMOS33 [get_ports {GMII_TXD[3]}]
set_property PACKAGE_PIN AE25 [get_ports {GMII_TXD[4]}]
set_property IOSTANDARD LVCMOS33 [get_ports {GMII_TXD[4]}]
set_property PACKAGE_PIN AE26 [get_ports {GMII_TXD[5]}]
set_property IOSTANDARD LVCMOS33 [get_ports {GMII_TXD[5]}]
set_property PACKAGE_PIN AD25 [get_ports {GMII_TXD[6]}]
set_property IOSTANDARD LVCMOS33 [get_ports {GMII_TXD[6]}]
set_property PACKAGE_PIN AD26 [get_ports {GMII_TXD[7]}]
set_property IOSTANDARD LVCMOS33 [get_ports {GMII_TXD[7]}]
# GMII_RXCLK
set_property PACKAGE_PIN AD20 [get_ports GMII_RXCLK]
set_property IOSTANDARD LVCMOS33 [get_ports GMII_RXCLK]
# GMII_RX_DV
set_property PACKAGE_PIN AB25 [get_ports GMII_RX_DV]
set_property IOSTANDARD LVCMOS33 [get_ports GMII_RX_DV]
# GMII_RX_ER
set_property PACKAGE_PIN AC26 [get_ports GMII_RX_ER]
set_property IOSTANDARD LVCMOS33 [get_ports GMII_RX_ER]
# GMII_RXD[0..7]
set_property PACKAGE_PIN W20 [get_ports {GMII_RXD[0]}]
set_property IOSTANDARD LVCMOS33 [get_ports {GMII_RXD[0]}]
set_property PACKAGE_PIN Y20 [get_ports {GMII_RXD[1]}]
set_property IOSTANDARD LVCMOS33 [get_ports {GMII_RXD[1]}]
set_property PACKAGE_PIN AA25 [get_ports {GMII_RXD[2]}]
set_property IOSTANDARD LVCMOS33 [get_ports {GMII_RXD[2]}]
set_property PACKAGE_PIN AA23 [get_ports {GMII_RXD[3]}]
set_property IOSTANDARD LVCMOS33 [get_ports {GMII_RXD[3]}]
set_property PACKAGE_PIN AA22 [get_ports {GMII_RXD[4]}]
set_property IOSTANDARD LVCMOS33 [get_ports {GMII_RXD[4]}]
set_property PACKAGE_PIN AB22 [get_ports {GMII_RXD[5]}]
set_property IOSTANDARD LVCMOS33 [get_ports {GMII_RXD[5]}]
set_property PACKAGE_PIN AB21 [get_ports {GMII_RXD[6]}]
set_property IOSTANDARD LVCMOS33 [get_ports {GMII_RXD[6]}]
set_property PACKAGE_PIN AB26 [get_ports {GMII_RXD[7]}]
set_property IOSTANDARD LVCMOS33 [get_ports {GMII_RXD[7]}]
# GMII_MDIO_MDC
set_property PACKAGE_PIN AB24 [get_ports GMII_MDIO_MDC]
set_property IOSTANDARD LVCMOS33 [get_ports GMII_MDIO_MDC]
# GMII_MDIO
set_property PACKAGE_PIN AF18 [get_ports GMII_MDIO]
set_property IOSTANDARD LVCMOS33 [get_ports GMII_MDIO]
# GMII_GE_IND
set_property PACKAGE_PIN AA24 [get_ports GMII_GE_IND]
set_property IOSTANDARD LVCMOS33 [get_ports GMII_GE_IND]




create_debug_core u_ila_0 ila
set_property ALL_PROBE_SAME_MU true [get_debug_cores u_ila_0]
set_property ALL_PROBE_SAME_MU_CNT 1 [get_debug_cores u_ila_0]
set_property C_ADV_TRIGGER false [get_debug_cores u_ila_0]
set_property C_DATA_DEPTH 1024 [get_debug_cores u_ila_0]
set_property C_EN_STRG_QUAL false [get_debug_cores u_ila_0]
set_property C_INPUT_PIPE_STAGES 0 [get_debug_cores u_ila_0]
set_property C_TRIGIN_EN false [get_debug_cores u_ila_0]
set_property C_TRIGOUT_EN false [get_debug_cores u_ila_0]
set_property port_width 1 [get_debug_ports u_ila_0/clk]
connect_debug_port u_ila_0/clk [get_nets [list Sclk]]
set_property port_width 7 [get_debug_ports u_ila_0/probe0]
connect_debug_port u_ila_0/probe0 [get_nets [list {ad_if/tx[7]} {ad_if/tx[8]} {ad_if/tx[9]} {ad_if/tx[10]} {ad_if/tx[11]} {ad_if/tx[12]} {ad_if/tx[13]}]]
create_debug_port u_ila_0 probe
set_property port_width 24 [get_debug_ports u_ila_0/probe1]
connect_debug_port u_ila_0/probe1 [get_nets [list {ad_if/dina[0]} {ad_if/dina[1]} {ad_if/dina[2]} {ad_if/dina[3]} {ad_if/dina[4]} {ad_if/dina[5]} {ad_if/dina[6]} {ad_if/dina[7]} {ad_if/dina[8]} {ad_if/dina[9]} {ad_if/dina[10]} {ad_if/dina[11]} {ad_if/dina[12]} {ad_if/dina[13]} {ad_if/dina[14]} {ad_if/dina[15]} {ad_if/dina[16]} {ad_if/dina[17]} {ad_if/dina[18]} {ad_if/dina[19]} {ad_if/dina[20]} {ad_if/dina[21]} {ad_if/dina[22]} {ad_if/dina[23]}]]
create_debug_port u_ila_0 probe
set_property port_width 14 [get_debug_ports u_ila_0/probe2]
connect_debug_port u_ila_0/probe2 [get_nets [list {ad_if/rx[0]} {ad_if/rx[1]} {ad_if/rx[2]} {ad_if/rx[3]} {ad_if/rx[4]} {ad_if/rx[5]} {ad_if/rx[6]} {ad_if/rx[7]} {ad_if/rx[8]} {ad_if/rx[9]} {ad_if/rx[10]} {ad_if/rx[11]} {ad_if/rx[12]} {ad_if/rx[13]}]]
create_debug_port u_ila_0 probe
set_property port_width 12 [get_debug_ports u_ila_0/probe3]
connect_debug_port u_ila_0/probe3 [get_nets [list {ad_if/doutb[0]} {ad_if/doutb[1]} {ad_if/doutb[2]} {ad_if/doutb[3]} {ad_if/doutb[4]} {ad_if/doutb[5]} {ad_if/doutb[6]} {ad_if/doutb[7]} {ad_if/doutb[8]} {ad_if/doutb[9]} {ad_if/doutb[10]} {ad_if/doutb[11]}]]
create_debug_port u_ila_0 probe
set_property port_width 1 [get_debug_ports u_ila_0/probe4]
connect_debug_port u_ila_0/probe4 [get_nets [list ad_if/Ien]]
create_debug_port u_ila_0 probe
set_property port_width 1 [get_debug_ports u_ila_0/probe5]
connect_debug_port u_ila_0/probe5 [get_nets [list ad_if/Oen]]
create_debug_port u_ila_0 probe
set_property port_width 1 [get_debug_ports u_ila_0/probe6]
connect_debug_port u_ila_0/probe6 [get_nets [list {ad_if/n_2_tx[7]_i_1}]]
create_debug_port u_ila_0 probe
set_property port_width 1 [get_debug_ports u_ila_0/probe7]
connect_debug_port u_ila_0/probe7 [get_nets [list {ad_if/n_2_tx[8]_i_1}]]
create_debug_port u_ila_0 probe
set_property port_width 1 [get_debug_ports u_ila_0/probe8]
connect_debug_port u_ila_0/probe8 [get_nets [list {ad_if/n_2_tx[9]_i_1}]]
create_debug_port u_ila_0 probe
set_property port_width 1 [get_debug_ports u_ila_0/probe9]
connect_debug_port u_ila_0/probe9 [get_nets [list {ad_if/n_2_tx[10]_i_1}]]
create_debug_port u_ila_0 probe
set_property port_width 1 [get_debug_ports u_ila_0/probe10]
connect_debug_port u_ila_0/probe10 [get_nets [list {ad_if/n_2_tx[11]_i_1}]]
create_debug_port u_ila_0 probe
set_property port_width 1 [get_debug_ports u_ila_0/probe11]
connect_debug_port u_ila_0/probe11 [get_nets [list {ad_if/n_2_tx[12]_i_1}]]
set_property C_CLK_INPUT_FREQ_HZ 300000000 [get_debug_cores dbg_hub]
set_property C_ENABLE_CLK_DIVIDER false [get_debug_cores dbg_hub]
set_property C_USER_SCAN_CHAIN 1 [get_debug_cores dbg_hub]
connect_debug_port dbg_hub/clk [get_nets Sclk]
