# create_bd_cell -type ip -vlnv xilinx.com:ip:processing_system7:5.5 processing_system7_0

start_gui
create_project R7OCM . -part xc7z030ffg676-1 -force
add_files -fileset constrs_1 -norecurse xdc/q7.xdc
set_property target_language verilog [current_project]

create_bd_design "armocm"

startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:processing_system7:5.5 processing_system7_0
apply_bd_automation -rule xilinx.com:bd_rule:processing_system7 -config {make_external "FIXED_IO, DDR" apply_board_preset "1" Master "Disable" Slave "Disable" }  [get_bd_cells processing_system7_0]
startgroup

startgroup
set_property -dict [list CONFIG.PCW_SDIO_PERIPHERAL_FREQMHZ {50} CONFIG.PCW_FPGA0_PERIPHERAL_FREQMHZ {40} CONFIG.PCW_UIPARAM_DDR_ENABLE {1} CONFIG.PCW_UIPARAM_DDR_PARTNO {MT41K256M16 RE-125} CONFIG.PCW_SD0_PERIPHERAL_ENABLE {1} CONFIG.PCW_SD0_GRP_CD_ENABLE {1} CONFIG.PCW_SD0_GRP_CD_IO {MIO 46} CONFIG.PCW_SD0_GRP_WP_ENABLE {1} CONFIG.PCW_SD0_GRP_WP_IO {MIO 47} CONFIG.PCW_SD0_GRP_POW_ENABLE {1} CONFIG.PCW_SD0_GRP_POW_IO {MIO 48} CONFIG.PCW_USB0_PERIPHERAL_ENABLE {1}] [get_bd_cells processing_system7_0]
endgroup

startgroup
set_property -dict [list CONFIG.PCW_UART0_PERIPHERAL_ENABLE {0} CONFIG.PCW_UART1_PERIPHERAL_ENABLE {1} CONFIG.PCW_UART1_UART1_IO {MIO 52 .. 53}] [get_bd_cells processing_system7_0]
endgroup

startgroup
set_property -dict [list CONFIG.PCW_NAND_PERIPHERAL_ENABLE {1} CONFIG.PCW_QSPI_PERIPHERAL_ENABLE {0} CONFIG.PCW_ENET0_PERIPHERAL_ENABLE {1} CONFIG.PCW_ENET0_ENET0_IO {EMIO} CONFIG.PCW_SD0_SD0_IO {MIO 40 .. 45} CONFIG.PCW_SPI0_PERIPHERAL_ENABLE {1} CONFIG.PCW_SPI0_SPI0_IO {MIO 16 .. 21} CONFIG.PCW_SPI0_GRP_SS1_ENABLE {1} CONFIG.PCW_SPI0_GRP_SS2_ENABLE {1} CONFIG.PCW_CAN0_PERIPHERAL_ENABLE {1} CONFIG.PCW_CAN0_CAN0_IO {MIO 26 .. 27} CONFIG.PCW_I2C0_PERIPHERAL_ENABLE {1} CONFIG.PCW_I2C0_I2C0_IO {MIO 22 .. 23} CONFIG.PCW_I2C1_PERIPHERAL_ENABLE {1} CONFIG.PCW_I2C1_I2C1_IO {MIO 24 .. 25}] [get_bd_cells processing_system7_0]
endgroup

startgroup
set_property -dict [list CONFIG.PCW_USB0_PERIPHERAL_ENABLE {1} CONFIG.PCW_USB0_RESET_ENABLE {1} CONFIG.PCW_USB0_RESET_IO {MIO 49} CONFIG.PCW_GPIO_MIO_GPIO_ENABLE {1}] [get_bd_cells processing_system7_0]
endgroup

startgroup
set_property -dict [list CONFIG.PCW_TTC0_PERIPHERAL_ENABLE {1}] [get_bd_cells processing_system7_0]
endgroup

create_bd_cell -type ip -vlnv xilinx.com:ip:axi_gpio:2.0 axi_gpio_0
endgroup
startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:axi_bram_ctrl:4.0 axi_bram_ctrl_0
endgroup
set_property -dict [list CONFIG.SINGLE_PORT_BRAM {1}] [get_bd_cells axi_bram_ctrl_0]
startgroup
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config {Master "/processing_system7_0/M_AXI_GP0" Clk "Auto" }  [get_bd_intf_pins axi_gpio_0/S_AXI]
apply_bd_automation -rule xilinx.com:bd_rule:board  [get_bd_intf_pins axi_gpio_0/GPIO]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config {Master "/processing_system7_0/M_AXI_GP0" Clk "Auto" }  [get_bd_intf_pins axi_bram_ctrl_0/S_AXI]
endgroup
set_property range 256K [get_bd_addr_segs {processing_system7_0/Data/SEG_axi_bram_ctrl_0_Mem0}]
set_property -dict [list CONFIG.C_GPIO_WIDTH {4} CONFIG.C_ALL_OUTPUTS {1}] [get_bd_cells axi_gpio_0]

set_property name TEST_LED [get_bd_intf_ports gpio_rtl]

startgroup
create_bd_intf_port -mode Master -vlnv xilinx.com:interface:bram_rtl:1.0 BRAM_PORTA
set_property CONFIG.MASTER_TYPE [get_property CONFIG.MASTER_TYPE [get_bd_intf_pins axi_bram_ctrl_0/BRAM_PORTA]] [get_bd_intf_ports BRAM_PORTA]
connect_bd_intf_net [get_bd_intf_pins axi_bram_ctrl_0/BRAM_PORTA] [get_bd_intf_ports BRAM_PORTA]
endgroup

startgroup
set_property -dict [list CONFIG.PCW_USE_S_AXI_HP0 {1} CONFIG.PCW_S_AXI_HP0_DATA_WIDTH {32}] [get_bd_cells processing_system7_0]
endgroup

startgroup
set_property -dict [list CONFIG.PCW_USE_M_AXI_GP1 {0} CONFIG.PCW_USE_S_AXI_HP0 {1}] [get_bd_cells processing_system7_0]
endgroup

startgroup
create_bd_intf_port -mode Slave -vlnv xilinx.com:interface:aximm_rtl:1.0 S_AXI_HP0
set_property -dict [list CONFIG.DATA_WIDTH [get_property CONFIG.DATA_WIDTH [get_bd_intf_pins processing_system7_0/S_AXI_HP0]] CONFIG.PROTOCOL [get_property CONFIG.PROTOCOL [get_bd_intf_pins processing_system7_0/S_AXI_HP0]] CONFIG.ID_WIDTH [get_property CONFIG.ID_WIDTH [get_bd_intf_pins processing_system7_0/S_AXI_HP0]] CONFIG.NUM_READ_OUTSTANDING [get_property CONFIG.NUM_READ_OUTSTANDING [get_bd_intf_pins processing_system7_0/S_AXI_HP0]] CONFIG.NUM_WRITE_OUTSTANDING [get_property CONFIG.NUM_WRITE_OUTSTANDING [get_bd_intf_pins processing_system7_0/S_AXI_HP0]] CONFIG.MAX_BURST_LENGTH [get_property CONFIG.MAX_BURST_LENGTH [get_bd_intf_pins processing_system7_0/S_AXI_HP0]]] [get_bd_intf_ports S_AXI_HP0]
connect_bd_intf_net [get_bd_intf_pins processing_system7_0/S_AXI_HP0] [get_bd_intf_ports S_AXI_HP0]
endgroup

startgroup
set_property -dict [list CONFIG.PCW_USE_HIGH_OCM {1}] [get_bd_cells processing_system7_0]
endgroup
assign_bd_address [get_bd_addr_segs {processing_system7_0/S_AXI_HP0/HP0_HIGH_OCM }]

startgroup
set_property -dict [list CONFIG.PCW_FPGA1_PERIPHERAL_FREQMHZ {100} CONFIG.PCW_EN_CLK1_PORT {1}] [get_bd_cells processing_system7_0]
endgroup
connect_bd_net [get_bd_pins processing_system7_0/FCLK_CLK1] [get_bd_pins processing_system7_0/S_AXI_HP0_ACLK]

startgroup
set_property -dict [list CONFIG.PCW_SPI_PERIPHERAL_FREQMHZ {200} CONFIG.PCW_SPI1_PERIPHERAL_ENABLE {1}] [get_bd_cells processing_system7_0]
endgroup

startgroup
create_bd_intf_port -mode Master -vlnv xilinx.com:interface:spi_rtl:1.0 SPI_1
connect_bd_intf_net [get_bd_intf_pins processing_system7_0/SPI_1] [get_bd_intf_ports SPI_1]
endgroup

startgroup
create_bd_port -dir O -from 0 -to 0 ENET0_GMII_TX_EN
connect_bd_net [get_bd_pins /processing_system7_0/ENET0_GMII_TX_EN] [get_bd_ports ENET0_GMII_TX_EN]
endgroup

startgroup
create_bd_port -dir O -from 0 -to 0 ENET0_GMII_TX_ER
connect_bd_net [get_bd_pins /processing_system7_0/ENET0_GMII_TX_ER] [get_bd_ports ENET0_GMII_TX_ER]
endgroup

startgroup
create_bd_port -dir O -from 7 -to 0 ENET0_GMII_TXD
connect_bd_net [get_bd_pins /processing_system7_0/ENET0_GMII_TXD] [get_bd_ports ENET0_GMII_TXD]
endgroup

startgroup
create_bd_port -dir I ENET0_GMII_RX_CLK
connect_bd_net [get_bd_pins /processing_system7_0/ENET0_GMII_RX_CLK] [get_bd_ports ENET0_GMII_RX_CLK]
endgroup

startgroup
create_bd_port -dir I ENET0_GMII_RX_DV
connect_bd_net [get_bd_pins /processing_system7_0/ENET0_GMII_RX_DV] [get_bd_ports ENET0_GMII_RX_DV]
endgroup
startgroup
create_bd_port -dir I ENET0_GMII_RX_ER
connect_bd_net [get_bd_pins /processing_system7_0/ENET0_GMII_RX_ER] [get_bd_ports ENET0_GMII_RX_ER]
endgroup
startgroup
create_bd_port -dir I ENET0_GMII_TX_CLK
connect_bd_net [get_bd_pins /processing_system7_0/ENET0_GMII_TX_CLK] [get_bd_ports ENET0_GMII_TX_CLK]
endgroup
startgroup
create_bd_port -dir I -from 7 -to 0 ENET0_GMII_RXD
connect_bd_net [get_bd_pins /processing_system7_0/ENET0_GMII_RXD] [get_bd_ports ENET0_GMII_RXD]
endgroup
startgroup
create_bd_port -dir O ENET0_MDIO_MDC
connect_bd_net [get_bd_pins /processing_system7_0/ENET0_MDIO_MDC] [get_bd_ports ENET0_MDIO_MDC]
endgroup
startgroup
create_bd_port -dir O ENET0_MDIO_O
connect_bd_net [get_bd_pins /processing_system7_0/ENET0_MDIO_O] [get_bd_ports ENET0_MDIO_O]
endgroup
startgroup
create_bd_port -dir O ENET0_MDIO_T
connect_bd_net [get_bd_pins /processing_system7_0/ENET0_MDIO_T] [get_bd_ports ENET0_MDIO_T]
endgroup
startgroup
create_bd_port -dir I ENET0_MDIO_I
connect_bd_net [get_bd_pins /processing_system7_0/ENET0_MDIO_I] [get_bd_ports ENET0_MDIO_I]
endgroup

startgroup
set_property -dict [list CONFIG.PCW_EN_RST1_PORT {1}] [get_bd_cells processing_system7_0]
endgroup
startgroup
create_bd_port -dir O -type rst FCLK_RESET1_N
connect_bd_net [get_bd_pins /processing_system7_0/FCLK_RESET1_N] [get_bd_ports FCLK_RESET1_N]
endgroup
startgroup
create_bd_port -dir O -type clk FCLK_CLK1
connect_bd_net [get_bd_pins /processing_system7_0/FCLK_CLK1] [get_bd_ports FCLK_CLK1]
endgroup

regenerate_bd_layout
save_bd_design
generate_target all [get_files  R7OCM.srcs/sources_1/bd/armocm/armocm.bd]
make_wrapper -files [get_files R7OCM.srcs/sources_1/bd/armocm/armocm.bd] -top
add_files -norecurse R7OCM.srcs/sources_1/bd/armocm/hdl/armocm_wrapper.v

create_ip -name clk_wiz -vendor xilinx.com -library ip -version 5.1 -module_name clk_wiz_0
set_property -dict [list CONFIG.PRIM_IN_FREQ {25} CONFIG.CLKOUT1_REQUESTED_OUT_FREQ {125.000} CONFIG.CLKIN1_JITTER_PS {400.0} CONFIG.MMCM_CLKFBOUT_MULT_F {40.000} CONFIG.MMCM_CLKIN1_PERIOD {40.0} CONFIG.MMCM_CLKOUT0_DIVIDE_F {8.000} CONFIG.CLKOUT1_JITTER {220.126} CONFIG.CLKOUT1_PHASE_ERROR {237.727}] [get_ips clk_wiz_0]
set_property -dict [list CONFIG.USE_LOCKED {false} CONFIG.USE_RESET {false}] [get_ips clk_wiz_0]
generate_target {instantiation_template} [get_files R7OCM.srcs/sources_1/ip/clk_wiz_0/clk_wiz_0.xci]

create_ip -name blk_mem_gen -vendor xilinx.com -library ip -version 8.2 -module_name blk_mem_axi2s
set_property -dict [list CONFIG.Interface_Type {Native} CONFIG.Memory_Type {Simple_Dual_Port_RAM} CONFIG.Assume_Synchronous_Clk {false} CONFIG.Write_Depth_A {32} CONFIG.Register_PortB_Output_of_Memory_Primitives {false} CONFIG.Use_AXI_ID {false} CONFIG.Enable_32bit_Address {false} CONFIG.Use_Byte_Write_Enable {false} CONFIG.Byte_Size {9} CONFIG.Write_Width_A {32} CONFIG.Read_Width_A {32} CONFIG.Operating_Mode_A {NO_CHANGE} CONFIG.Write_Width_B {32} CONFIG.Read_Width_B {32} CONFIG.Operating_Mode_B {WRITE_FIRST} CONFIG.Enable_B {Use_ENB_Pin} CONFIG.Register_PortA_Output_of_Memory_Primitives {false} CONFIG.Use_RSTB_Pin {false} CONFIG.Reset_Type {SYNC} CONFIG.Port_B_Clock {100} CONFIG.Port_B_Enable_Rate {100}] [get_ips blk_mem_axi2s]
generate_target {instantiation_template} [get_files R7OCM.srcs/sources_1/ip/blk_mem_axi2s/blk_mem_axi2s.xci]
create_ip_run [get_files -of_objects [get_fileset sources_1] R7OCM.srcs/sources_1/ip/blk_mem_axi2s/blk_mem_axi2s.xci]
launch_run  blk_mem_axi2s_synth_1

generate_target all [get_files R7OCM.srcs/sources_1/ip/clk_wiz_0/clk_wiz_0.xci]
create_ip_run [get_files -of_objects [get_fileset sources_1] R7OCM.srcs/sources_1/ip/clk_wiz_0/clk_wiz_0.xci]
launch_run  clk_wiz_0_synth_1

add_files -norecurse src/rtl/R7OCM_top.v
add_files -norecurse src/rtl/GE_patch.v
add_files -norecurse src/rtl/A2S_controller.v
add_files -norecurse src/rtl/S2A_controller.v
add_files -norecurse src/rtl/AXI2S.v
add_files -norecurse src/rtl/AXI2SREG.v
add_files -norecurse src/rtl/reg_define.v
add_files -norecurse src/rtl/CBusReadMerge.v
add_files -norecurse src/rtl/AD9361REG.v
add_files -norecurse test/cntSrc.v

set_property top R7OCM_top [current_fileset]

update_compile_order -fileset sources_1
update_compile_order -fileset sim_1
