#! /bin/bash
echo "pack project"
make backup
echo "copy project"
scp ../R7OCM.tgz root@192.168.1.110:/home/root
echo "copy bit"
scp R7OCM.runs/impl_1/R7OCM_top.bit root@192.168.1.110:/home/root
echo "extrace project"
ssh root@192.168.1.110 'tar -xzf R7OCM.tgz'
echo "download bit"
ssh root@192.168.1.110 'cat R7OCM_top.bit > /dev/xdevcfg'
echo "check version"
ssh root@192.168.1.110 'cd src/python;python axi2s_c.py OCM'
echo "finished"
