#!/bin/bash
ls=`ls -1 processor0 | grep '^[0-9].\|^[0-9]'`
for arg1 in 0 1 2 3 4 5 6 7
do
for arg2 in $ls
do
cp processor$arg1/0/region processor$arg1/$arg2/region
done
done
