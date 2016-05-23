#! /bin/bash
hostip=$1
echo "download bit"
echo ${hostip}
curl -F bit=@'R7OCM.runs/impl_1/R7OCM_top.bit' http://${hostip}:8080/misc
echo ""
echo "wait 2 s"
sleep 2
echo "init ad9361"
curl -F adscripts=@'AD9361/ad9361_config.reg' http://${hostip}:8080/misc
echo ""
echo "enable AXI_DMA"
curl -G -d 'fun=wreg&reg=AXI2S_EN&value=0' http://${hostip}:8080/misc
echo ""
curl -G -d 'fun=wreg&reg=AXI2S_IBASE&value=0xfffc0000' http://${hostip}:8080/misc
echo ""
curl -G -d 'fun=wreg&reg=AXI2S_ISIZE&value=0x10000' http://${hostip}:8080/misc
echo ""
curl -G -d 'fun=wreg&reg=AXI2S_OBASE&value=0xfffd0000' http://${hostip}:8080/misc
echo ""
curl -G -d 'fun=wreg&reg=AXI2S_OSIZE&value=0x10000' http://${hostip}:8080/misc
echo ""
curl -G -d 'fun=wreg&reg=AXI2S_EN&value=3' http://${hostip}:8080/misc
echo ""
echo "enable AD9361"
curl -G -d 'fun=wreg&reg=AD9361_EN&value=1' http://${hostip}:8080/misc
echo ""
echo "finished"
