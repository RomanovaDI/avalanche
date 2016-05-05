#!/bin/bash
set -x
./delete.sh
#cp 0/alpha.water.org 0/alpha.water
#cp 0/region.org 0/region
cd map_creating
#cp ../../asc2dicts2.c .
#gcc asc2dicts2.c
./a.out
#./a.out relief_22.asc.txt 15 region.asc.txt 1 1 4
cd ../
cp map_creating/blockMeshDict system/blockMeshDict
cp map_creating/alpha.water 0/alpha.water.org
cp map_creating/region 0/region.org
cp map_creating/alpha.water 0/alpha.water
cp map_creating/region 0/region
blockMesh
decomposePar
#mpirun -np 4 setFields -parallel
mpirun -np 32 interFoam -parallel
reconstructPar
./crutch_for_region.sh
mkdir pics
pvpython script4.py
