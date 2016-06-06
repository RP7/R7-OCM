#! /bin/bash
hostip=$1
echo "pack project"
make backup
echo "make dir in tmp"
ssh root@${hostip} 'mkdir /tmp/R7OCM'
echo "copy project"
scp ../R7OCM.tgz root@${hostip}:/tmp/R7OCM
echo "copy bit"
scp R7OCM.runs/impl_$2/R7OCM_top.bit root@${hostip}:/tmp/R7OCM
echo "extrace project"
ssh root@${hostip} 'cd /tmp/R7OCM; tar -xzf R7OCM.tgz'
echo "make"
ssh root@${hostip} "mkdir -p /tmp/R7OCM/lib; cd /tmp/R7OCM; make"
echo "download bit"
ssh root@${hostip} 'cd /tmp/R7OCM; cat R7OCM_top.bit > /dev/xdevcfg'
echo "check version"
ssh root@${hostip} 'cd /tmp/R7OCM/src/python;python axi2s_c.py OCM'
echo "start web"
ssh root@${hostip} 'cd /tmp/R7OCM/src/python;python q7web.py'
echo "finished"
