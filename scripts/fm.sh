#! /bin/bash
hostip=$1
echo "init ad9361"
curl -F adscripts=@'AD9361/FM.reg' http://${hostip}:8080/misc
echo ""
echo "set rx fir"
curl -F chead=@'AD9361/200K_1920K.h' http://${hostip}:8080/fir
echo ""
echo "init"
curl http://${hostip}:8080/init?'rx&freq=103.9e6'
echo ""
echo "finished"
