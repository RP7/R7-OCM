# RESTful API
## 读取频率

1. **tx** 

		curl http://192.168.1.110:8080/tx?freq
		{"data": {"freq": 800000000.0}, "ret": "ok"}

2. **rx** 
 
		curl http://192.168.1.110:8080/rx?freq
		return {"data": {"freq": 939999999.85098803}, "ret": "ok"}

## 设置频率

1. **tx** 

		curl http://192.168.1.110:8080/tx?freq=945e6
		return {'ret':'ok'}

2. **rx** 
 
		curl http://192.168.1.110:8080/rx?freq=940e6
		return {'ret':'ok'}

## 读取增益

1. **tx** 
		
		curl http://192.168.1.110:8080/tx?gain
		return {"data": {"gain": {"1": -10.0, "2": -10.0}}, "ret": "ok"}

1. **tx port1**

		curl -G -d 'port=1&gain' http://192.168.1.110:8080/tx
		return {"data": {"gain": {"1": -10.0}}, "ret": "ok"}

1. **rx** 

		curl http://192.168.1.110:8080/rx?gain
		return {"data": {"gain": {"1": 76, "2": 76}}, "ret": "ok"}

## 初始化

1. **url**

		curl -G -d 'IBASE=xxx&OBASE=xxx&&ISZIE=xxx&OSIZE=xxx&rx&freq=xxx&gain=xx&port=0|1'
		return {"data":{"IBASE":xxx,"OBASE"},"ret":"ok"}
		IBASE:option,default=0xfffc0000,如果用DRAM，可以改为0x1e000000 
		ISIZE:option,default=0x10000,64K,16Ksamples
		OBASE:option,default=0xfffd0000,如果用DRAM，可以改为0x1f000000 
		OSIZE:option,default=0x10000
		rx:option,表示修改接收配置
		freq:option,频率值，单位Hz，浮点数
		gain:option,增益，整数
		port:option,天线端口，如果不指定，两个天线的增益都修改

## 设置增益

1. **tx** 
		
		curl http://192.168.1.110:8080/tx?gain=-5
		return {'ret':'ok'}

1. **tx port1** 
		
		curl -G -d 'port=1&gain=-5' http://192.168.1.110:8080/tx
		return {'ret':'ok'}

1. **rx** 

		curl http://192.168.1.110:8080/rx?gain=50
		return {'ret':'ok'}

## 上传FIR滤波器系数

		curl -F fir=@'AD9361/LTE1p4_MHz.ftr' http://192.168.1.110:8080/fir
		return {"ret": "ok"}

		curl -F chead=@'AD9361/200K_1920K.h' http://192.168.1.110:8080/fir
		return {"ret": "ok"}

## 读取RX缓冲区

		curl -o temp/rx.dat -G -d 'samples=1920&start=0' http://192.168.1.110:8080/rxbuf
		return in rx.data
		sample 	         数据长度
		start            数据起点 
		frame            帧号，缺省当前帧 


## 填充TX缓冲区

		curl -F data=@tx.dat -F "samples=120" -F "frame=100" -F "start=0" http://192.168.1.110:8080/txbuf
		return {"ret": "ok"}
		数据在    tx.dat
		sample   数据长度
		start    数据起点 
		frame	 帧号 

## 读取频谱
		
		curl http://192.168.1.110:8080/data
		return {  "i": [2047, 2010, 1115, 1747, 2047, 391, -2048.....]
				, "q": [-1636, -2048, 123, 2047, 2047, 1255, 1771...]
				, "freq": [-500,-499...499,500]
				, "power": [100.03597595669271, 100.42172402828378, 98.85927007812113...]
				}

## 杂项

1. 版本

		curl -G -d 'fun=ver' http://192.168.1.110:8080/misc
		return {"data": "VER: 00000100-04c2fe7eb88757798a6a5927fdaa1e781664cb31", "ret": "ok"}

2. 运行ADI的脚本文件

		curl -F adscripts=@'AD9361/ad9361_config.reg' http://192.168.1.110:8080/misc
		return {"ret": "ok"}

2. 下载bit文件

		curl -F bit=@'R7OCM.runs/impl_1/R7OCM_top.bit' http://192.168.1.110:8080/misc
		return {"ret": "ok"}

2. 读AD9361寄存器

		curl -G -d 'fun=arreg&reg=109' http://192.168.1.110:8080/misc
		return {"data": "0x4cL", "ret": "ok"}

2. 写AD9361寄存器

		curl -G -d 'fun=awreg&reg=109&value=38' http://192.168.1.110:8080/misc
		return {"data": "0x4cL", "ret": "ok"}

2. 读寄存器

		curl -G -d 'fun=rreg&reg=VER_MAJOR' http://192.168.1.110:8080/misc
		return {"data": "0x100L", "ret": "ok"}

3. 写寄存器

		curl -G -d 'fun=wreg&reg=AXI2S_EN&value=3' http://192.168.1.110:8080/misc
		return {"ret": "ok"}
		错误
		curl -G -d 'fun=wreg&reg=AXI2S_EN' http://192.168.1.110:8080/misc
		return {"res": "reg or value not given", "ret": "err"}


4. 可读写的寄存器
		
		/* AXI2S Write only Reg */
		`define AXI2S_EN        18'h00000
		`define AXI2S_TEST      18'h00004
		`define AXI2S_IBASE     18'h00010
		`define AXI2S_ISIZE     18'h00014
		`define AXI2S_OBASE     18'h00018
		`define AXI2S_OSIZE     18'h0001C
		`define FRAME_LEN       18'h00020
		`define FRAME_ADJ       18'h00024
		`define TSTART          18'h00030
		`define TEND            18'h00034
		`define RSTART          18'h00038
		`define REND            18'h0003C
		
		/* AXI2S Read Only Reg */
		`define AXI2S_STATE     18'h00000
		`define AXI2S_IACNT     18'h00010
		`define AXI2S_IBCNT     18'h00014
		`define AXI2S_OACNT     18'h00018
		`define AXI2S_OBCNT     18'h0001c
		`define AXI_RRESP       18'h00020
		`define AXI_WRESP       18'h00024
		`define AXI_STATUS      18'h00028
		`define AXI_RADDR       18'h00030
		`define AXI_WADDR       18'h00034
		`define VER_MAJOR       18'h00040
		`define VER_MINOR0      18'h00050
		`define VER_MINOR1      18'h00054
		`define VER_MINOR2      18'h00058
		`define VER_MINOR3      18'h0005c
		`define VER_MINOR4      18'h00060
		
		/* AD9361 Control Signal Write only */
		`define AD9361_RST		18'h00100
		`define AD9361_EN		18'h00110
		`define AD9361_TX_RX    18'h00120
		`define AD9361_EN_AGC   18'h00130
		`define RF_CTRL_IN      18'h00140
		`define RF_SW           18'h00150
		`define PA_EN           18'h00160
