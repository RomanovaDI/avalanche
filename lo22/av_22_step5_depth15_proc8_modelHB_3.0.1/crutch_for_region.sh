#!/bin/bash
for arg1 in 0 1 2 3 4 5 6 7
do
for arg2 in 1 2 3 4 5 6 7 8 9
do
cp processor$arg1/0/region processor$arg1/0.$arg2/region
done
cp processor$arg1/0/region processor$arg1/1/region
done
