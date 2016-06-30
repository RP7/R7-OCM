#! /bin/bash
hostip=$1
echo "init ad9361"
curl -F adscripts=@'AD9361/scan.reg' http://${hostip}:8080/misc
echo ""
echo ""
echo "init"
curl http://${hostip}:8080/init?'rx&gain=55&freq=939.8e6'
echo ""
