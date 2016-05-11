# R7-OCM
Q7 board OCM reference design

这是一个Open5G R7开源硬件的参考设计，包含OCM的使用和AD9361的使用。

目录说明
AD9361     AD9361开发工具的工程和配置寄存器的脚本。
dts        本设计对应zync的设备树，用于配置Linux操作系统
scripts    tcl脚本，用于生成vivado project
src        源程序
	rtl    FPGA代码
	c      C代码
	python python代码
test       测试用代码
xdc        约束文件

Quick Start

> git clone http://github.com/RP7/R7-OCM
> start vivado 2014.4
> source scripts/R7OCM.tcl
> Generate Bitstream
> download
> copy src to R7 /home/root
> copy AD9361 to R7 /home/root
> In R7
> cd src/python
> python adscripts.py

R7需要预装SDK环境


