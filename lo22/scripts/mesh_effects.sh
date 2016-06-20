#!/bin/bash
set -x

depth_ind="1"
depth[1]="6"

kx_ind="1 2 3 4"
kx[1]="1"
kx[2]="2"
kx[3]="3"
kx[4]="4"

ky_ind="1"
ky[1]="1"
ky[2]="2"
ky[3]="3"
ky[4]="4"

kz_ind="1 2 3 4 5 6"
kz[1]="1"
kz[2]="2"
kz[3]="3"
kz[4]="4"
kz[5]="5"
kz[6]="6"

rm -rf map_effect_research
mkdir map_effect_research
cd map_effect_research

#before="./a.out"
#after="./a.out relief_22.asc ${depth[$arg1]} region.asc ${kx[$arg2]} ${ky[$arg3]} ${kz[$arg4]}"

for arg1 in $depth_ind
do
for arg2 in $kx_ind
do
for arg3 in $ky_ind
do
for arg4 in $kz_ind
do
cp -r ../av_22_proc32_modelHB_turbRAS_3.0.1_triangle_origin depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg2]}_kz${kz[$arg4]}
cd depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg2]}_kz${kz[$arg4]}
#sed "s/.\/a.out/.\/a.out relief_22.asc ${depth[$arg1]} region.asc ${kx[$arg2]} ${ky[$arg3]} ${kz[$arg4]}/" execute.sh > tmp
#mv tmp execute.sh
#chmod a+x execute.sh
./run.sh ${kx[$arg2]} ${ky[$arg2]} ${kz[$arg4]}
cd ..
done
done
done
done
