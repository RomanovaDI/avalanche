#!/bin/bash
set -x

depth_ind="1"
depth[1]="6"

kx_ind="1"
kx[1]="1"

ky_ind="1"
ky[1]="1"

kz_ind="1 2 3 4 5 6"
kz[1]="3"
kz[2]="4"
kz[3]="5"
kz[4]="6"
kz[5]="7"
kz[6]="8"

#rm -rf map_effect_research
#mkdir map_effect_research
cd mesh_effect_research
mkdir sets

#before="./a.out"
#after="./a.out relief_22.asc ${depth[$arg1]} region.asc ${kx[$arg2]} ${ky[$arg3]} ${kz[$arg4]}"

max_time_steps_quantity="0 1 2 3 4 5 6 7 8 9 10"

for arg1 in $depth_ind
do
for arg2 in $kx_ind
do
for arg3 in $ky_ind
do
#for arg4 in $kz_ind
#do
for arg5 in $max_time_steps_quantity
do
#cp -r ../av_22_proc32_modelHB_turbRAS_3.0.1_origin depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[$arg4]}
#cp ../av_22_proc32_modelHB_turbRAS_3.0.1_origin/system/controlDict depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[$arg4]}/system/controlDict
#cp ../av_22_proc32_modelHB_turbRAS_3.0.1_origin/execute1.sh depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[$arg4]}/execute.sh
#cd depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[$arg4]}
#sed "s/.\/a.out/.\/a.out relief_22.asc ${depth[$arg1]} region.asc ${kx[$arg2]} ${ky[$arg3]} ${kz[$arg4]}/" execute.sh > tmp
#mv tmp execute.sh
#chmod a+x execute.sh
#/run.sh
#pvpython script4.py
#cd ..
#montage depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[1]}/pics/$arg5.png -tile 1x1 -geometry 1871x1062+0+0 depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[1]}/pics/$arg5.png
#montage depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[2]}/pics/$arg5.png -tile 1x1 -geometry 1871x1062+0+0 depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[1]}/pics/$arg5.png
#montage depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[3]}/pics/$arg5.png -tile 1x1 -geometry 1871x1062+0+0 depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[1]}/pics/$arg5.png
#montage depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[4]}/pics/$arg5.png -tile 1x1 -geometry 1871x1062+0+0 depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[1]}/pics/$arg5.png
#montage depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[5]}/pics/$arg5.png -tile 1x1 -geometry 1871x1062+0+0 depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[1]}/pics/$arg5.png
#montage depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[6]}/pics/$arg5.png -tile 1x1 -geometry 1871x1062+0+0 depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[1]}/pics/$arg5.png
convert -resize x600 depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[1]}/pics/$arg5.png depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[1]}/pics/$arg5.png
convert -resize x600 depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[2]}/pics/$arg5.png depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[2]}/pics/$arg5.png
convert -resize x600 depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[3]}/pics/$arg5.png depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[3]}/pics/$arg5.png
convert -resize x600 depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[4]}/pics/$arg5.png depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[4]}/pics/$arg5.png
convert -resize x600 depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[5]}/pics/$arg5.png depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[5]}/pics/$arg5.png
convert -resize x600 depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[6]}/pics/$arg5.png depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[6]}/pics/$arg5.png
montage depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[1]}/pics/$arg5.png depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[2]}/pics/$arg5.png depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[3]}/pics/$arg5.png depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[4]}/pics/$arg5.png depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[5]}/pics/$arg5.png depth${depth[$arg1]}_kx${kx[$arg2]}_ky${ky[$arg3]}_kz${kz[6]}/pics/$arg5.png -tile 3x2 -geometry '800x600+0+0<' -mode Concatenate  sets/$arg5.png
done
done
done
done
#done

cd ..
