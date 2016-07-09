#!/bin/bash
set -x

kx_ind="1 2 3"
kx[1]="200"
kx[2]="400"
kx[3]="800"

ky_ind="1 2 3"
ky[1]="100"
ky[2]="200"
ky[3]="400"

kz_ind="1 2 3"
kz[1]="4"
kz[2]="8"
kz[3]="16"

bl_pattern1="	hex (0 1 2 3 4 5 6 7) "
bl_pattern2=" simpleGrading (1 1 1) // 0"

for arg1 in $kx_ind
do
for arg2 in $ky_ind
do
for arg3 in $kz_ind
do
mkdir kx${kx[$arg1]}_ky${ky[$arg2]}_kz${kz[$arg3]}/
cp -r 30_angle_slope_proc32_modelHB_turbRAS_3.0.1_hex_nonortogonal_origin/* kx${kx[$arg1]}_ky${ky[$arg2]}_kz${kz[$arg3]}/
cd kx${kx[$arg1]}_ky${ky[$arg2]}_kz${kz[$arg3]}/
sed "s/bl_pattern/$bl_pattern1(${kx[$arg1]} ${ky[$arg2]} ${kz[$arg3]})$bl_pattern2/" system/blockMeshDict > tmp
mv tmp system/blockMeshDict
./run.sh
cd ../
done
done
done
