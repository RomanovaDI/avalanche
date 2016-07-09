#!/bin/bash
set -x

kx_ind="1 2 3 4 5 6"
kx[1]="200"
kx[2]="400"
kx[3]="1000"
kx[4]="2000"
kx[5]="4000"
kx[6]="10000"

ky_ind="1 2 3"
ky[1]="100"
ky[2]="200"
ky[3]="500"
ky[4]="1000"
ky[5]="2000"
ky[6]="5000"

kz_ind="1 2 3"
kz[1]="4"
kz[2]="8"
kz[3]="20"
kz[4]="40"
kz[5]="80"
kz[6]="200"

bl_pattern1="	hex (0 1 2 3 4 5 6 7) "
bl_pattern2=" simpleGrading (1 1 1) // 0"

for arg1 in $kx_ind
do
#for arg2 in $ky_ind
#do
#for arg3 in $kz_ind
#do
mkdir kx${kx[$arg1]}_ky${ky[$arg1]}_kz${kz[$arg1]}/
cp -r 30_angle_slope_proc32_modelHB_turbRAS_3.0.1_hex_nonortogonal_origin/* kx${kx[$arg1]}_ky${ky[$arg1]}_kz${kz[$arg1]}/
cd kx${kx[$arg1]}_ky${ky[$arg1]}_kz${kz[$arg1]}/
sed "s/bl_pattern/$bl_pattern1(${kx[$arg1]} ${ky[$arg1]} ${kz[$arg1]})$bl_pattern2/" system/blockMeshDict > tmp
mv tmp system/blockMeshDict
./run.sh
cd ../
done
#done
#done
