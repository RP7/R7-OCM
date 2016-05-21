#! /bin/bash
echo "pack project"
make backup
echo "make dir in tmp"
ssh root@192.168.1.110 'mkdir /tmp/R7OCM'
echo "copy project"
scp ../R7OCM.tgz root@192.168.1.110:/tmp/R7OCM
echo "copy bit"
scp R7OCM.runs/impl_1/R7OCM_top.bit root@192.168.1.110:/tmp/R7OCM
echo "extrace project"
ssh root@192.168.1.110 'cd /tmp/R7OCM; tar -xzf R7OCM.tgz'
echo "download bit"
ssh root@192.168.1.110 'cd /tmp/R7OCM; cat R7OCM_top.bit > /dev/xdevcfg'
echo "check version"
ssh root@192.168.1.110 'cd /tmp/R7OCM/src/python;python axi2s_c.py OCM'
echo "finished"
