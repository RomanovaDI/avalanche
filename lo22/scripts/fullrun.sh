#!/bin/bash
set -x

rho_ind="2"
rho_pattern="    rho             rho [ 1 -3 0 0 0 0 0 ] "
rho[1]="300"
rho[2]="200"

nu0_ind="1 2 3 4 5"
nu0_pattern="		nu0             nu0   [ 0 2 -1 0 0 0 0 ] "
nu0[1]="1e5"
nu0[2]="5e5"
nu0[3]="1e6"
nu0[4]="5e4"
nu0[5]="1e4"

tau0_ind="1 2 3 4 5 6 7 8 9"
tau0_pattern="		tau0            tau0  [ 0 2 -2 0 0 0 0 ] "
tau0[1]="1e1"
tau0[2]="9"
tau0[3]="8"
tau0[4]="7"
tau0[5]="6"
tau0[6]="11"
tau0[7]="12"
tau0[8]="13"
tau0[9]="14"

k_ind="1 2 3"
k_pattern="		k               k     [ 0 2 -1 0 0 0 0 ] "
k[1]="5"
k[2]="4"
k[3]="6"

n_ind="2"
n_pattern="		n               n     [ 0 0  0 0 0 0 0 ] "
n[1]="2"
n[2]="5e-1"

for arg1 in $rho_ind
do
for arg2 in $nu0_ind
do
for arg3 in $tau0_ind
do
for arg4 in $k_ind
do
for arg5 in $n_ind
do
mkdir rho${rho[$arg1]}_nu0${nu0[$arg2]}_tau0${tau0[$arg3]}_k${k[$arg4]}_n${n[$arg5]}/
cp -r av_22_step5_depth6_proc32_modelHB_turbRAS_3.0.1_original/* rho${rho[$arg1]}_nu0${nu0[$arg2]}_tau0${tau0[$arg3]}_k${k[$arg4]}_n${n[$arg5]}/
cd rho${rho[$arg1]}_nu0${nu0[$arg2]}_tau0${tau0[$arg3]}_k${k[$arg4]}_n${n[$arg5]}/
sed "s/rho_pattern/$rho_pattern${rho[$arg1]};/" constant/transportProperties > tmp
mv tmp constant/transportProperties
sed "s/nu0_pattern/$nu0_pattern${nu0[$arg2]};/" constant/transportProperties > tmp
mv tmp constant/transportProperties
sed "s/tau0_pattern/$tau0_pattern${tau0[$arg3]};/" constant/transportProperties > tmp
mv tmp constant/transportProperties
sed "s/k_pattern/$k_pattern${k[$arg4]};/" constant/transportProperties > tmp
mv tmp constant/transportProperties
sed "s/n_pattern/$n_pattern${n[$arg5]};/" constant/transportProperties > tmp
mv tmp constant/transportProperties
./run.sh
cd ../
done
done
done
done
done
