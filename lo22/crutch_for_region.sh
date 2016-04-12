#!/bin/bash
ls1=`ls -1 processor0 | grep '^[0-9].\|^[0-9]'`
ls2=`ls -1 | grep processor`
for arg1 in $ls2
do
for arg2 in $ls1
do
cp $arg1/0/region $arg1/$arg2/region
done
done
