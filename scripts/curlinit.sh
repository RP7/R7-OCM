#! /bin/bash
hostip=$1
echo ${hostip}
echo "init ad9361"
curl -F adscripts=@'AD9361/ad9361_config.reg' http://${hostip}:8080/misc
echo ""
echo "init"
curl http://${hostip}:8080/init?'rx&gain=55&freq=939.8e6'
echo ""
echo "AFC"
curl http://${hostip}:8080/misc?'fun=awreg&reg=18&value=0x1f'
echo ""
sleep 1
echo "udp service start"
curl http://${hostip}:8080/udp?port=10000
echo ""
echo "finished"
