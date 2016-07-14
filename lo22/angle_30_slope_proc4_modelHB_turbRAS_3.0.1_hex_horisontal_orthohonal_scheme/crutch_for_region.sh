#!/bin/bash
ls1=`ls -1 | grep '^[0-9].\|^[1-9]'`
for arg2 in $ls1
do
cp 0/region $arg2/region
done
