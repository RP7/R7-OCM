#! /bin/bash
hostip=$1
echo "init ad9361"
curl -F adscripts=@'AD9361/FM.reg' http://${hostip}:8080/misc
echo ""
echo "set rx fir"
curl -F chead=@'AD9361/30K_75K.h' http://${hostip}:8080/fir
echo ""
echo "set freq set agc"
curl http://${hostip}:8080/init?'rx&freq=97.4e6&gain=35'
echo ""
sleep 1
echo "start FM"
curl http://${hostip}:8080/FM?start
echo ""
echo "finished"
