#!/bin/bash
set -x

rho_ind="1 2"
rho_pattern="    rho             rho [ 1 -3 0 0 0 0 0 ] "
rho[1]="300"
rho[2]="200"

nu0_ind="1 2 3"
nu0_pattern="		nu0             nu0   [ 0 2 -1 0 0 0 0 ] "
nu0[1]="1e2"
nu0[2]="1e5"
nu0[3]="1e-2"

tau0_ind="1 2 3"
tau0_pattern="		tau0            tau0  [ 0 2 -2 0 0 0 0 ] "
tau0[1]="1"
tau0[2]="1e-1"
tau0[3]="1e1"

k_ind="1 2 3"
k_pattern="		k               k     [ 0 2 -1 0 0 0 0 ] "
k[1]="1e-5"
k[2]="1e-4"
k[3]="1e-6"

n_ind="1 2"
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
montage rho${rho[$arg1]}_nu0${nu0[$arg2]}_tau0${tau0[$arg3]}_k${k[$arg4]}_n${n[1]}/pics/3.png  rho${rho[$arg1]}_nu0${nu0[$arg2]}_tau0${tau0[$arg3]}_k${k[$arg4]}_n${n[2]}/pics/3.png -tile 1x2 -geometry +0+0 setv/rho${rho[$arg1]}_nu0${nu0[$arg2]}_tau0${tau0[$arg3]}_k${k[$arg4]}.png
done
done
done
done

for arg1 in $rho_ind
do
for arg2 in $nu0_ind
do
for arg3 in $tau0_ind
do
for arg5 in $n_ind
do
montage rho${rho[$arg1]}_nu0${nu0[$arg2]}_tau0${tau0[$arg3]}_k${k[1]}_n${n[$arg5]}/pics/3.png rho${rho[$arg1]}_nu0${nu0[$arg2]}_tau0${tau0[$arg3]}_k${k[2]}_n${n[$arg5]}/pics/3.png  rho${rho[$arg1]}_nu0${nu0[$arg2]}_tau0${tau0[$arg3]}_k${k[3]}_n${n[$arg5]}/pics/3.png -tile 1x3 -geometry +0+0 setv/rho${rho[$arg1]}_nu0${nu0[$arg2]}_tau0${tau0[$arg3]}_n${n[$arg5]}.png
done
done
done
done

for arg1 in $rho_ind
do
for arg2 in $nu0_ind
do
for arg4 in $k_ind
do
for arg5 in $n_ind
do
montage rho${rho[$arg1]}_nu0${nu0[$arg2]}_tau0${tau0[1]}_k${k[$arg4]}_n${n[$arg5]}/pics/3.png rho${rho[$arg1]}_nu0${nu0[$arg2]}_tau0${tau0[2]}_k${k[$arg4]}_n${n[$arg5]}/pics/3.png  rho${rho[$arg1]}_nu0${nu0[$arg2]}_tau0${tau0[3]}_k${k[$arg4]}_n${n[$arg5]}/pics/3.png -tile 1x3 -geometry +0+0 setv/rho${rho[$arg1]}_nu0${nu0[$arg2]}_k${k[$arg4]}_n${n[$arg5]}.png
done
done
done
done

for arg1 in $rho_ind
do
for arg3 in $tau0_ind
do
for arg4 in $k_ind
do
for arg5 in $n_ind
do
montage rho${rho[$arg1]}_nu0${nu0[1]}_tau0${tau0[$arg3]}_k${k[$arg4]}_n${n[$arg5]}/pics/3.png rho${rho[$arg1]}_nu0${nu0[2]}_tau0${tau0[$arg3]}_k${k[$arg4]}_n${n[$arg5]}/pics/3.png  rho${rho[$arg1]}_nu0${nu0[3]}_tau0${tau0[$arg3]}_k${k[$arg4]}_n${n[$arg5]}/pics/3.png -tile 1x3 -geometry +0+0 setv/rho${rho[$arg1]}_tau0${tau0[$arg3]}_k${k[$arg4]}_n${n[$arg5]}.png
done
done
done
done

for arg2 in $nu0_ind
do
for arg3 in $tau0_ind
do
for arg4 in $k_ind
do
for arg5 in $n_ind
do
montage rho${rho[1]}_nu0${nu0[$arg2]}_tau0${tau0[$arg3]}_k${k[$arg4]}_n${n[$arg5]}/pics/3.png  rho${rho[2]}_nu0${nu0[$arg2]}_tau0${tau0[$arg3]}_k${k[$arg4]}_n${n[$arg5]}/pics/3.png -tile 1x2 -geometry +0+0 setv/nu0${nu0[$arg2]}_tau0${tau0[$arg3]}_k${k[$arg4]}_n${n[$arg5]}.png
done
done
done
done
