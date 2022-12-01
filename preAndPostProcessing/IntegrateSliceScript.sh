#!/bin/bash -i
source ~/.bashrc
set -x
ls1=`ls -1`
for arg1 in $ls1
do
cd $arg1
#mkdir data
pvpython ../../pics/IntegrateSlice.py
cd ..
done

