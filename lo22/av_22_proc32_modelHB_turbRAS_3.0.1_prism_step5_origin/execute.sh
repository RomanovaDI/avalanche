#!/bin/bash
set -x
./delete.sh
cp 0/alpha.water.org 0/alpha.water
cp 0/region.org 0/region
#cd map_creating
#cp ../../asc2dicts2.c .
#gcc asc2dicts2.c
#./a.out
#gcc asc2dicts3 -o asc2dicts3 -lm
#gcc asc2dicts4 -o asc2dicts4 -lm
#./asc2dicts4 relief_22.asc 1  6 region.asc
#./asc2dicts3 relief_22.asc 6 region.asc $1 $2 $3 20
#cd ../
#cp map_creating/blockMeshDict system/
#cp map_creating/setFieldsDict system/
#cp map_creating/alpha.water 0/alpha.water.org
#cp map_creating/region 0/region.org
#cp map_creating/alpha.water 0/alpha.water
#cp map_creating/region 0/region
blockMesh
decomposePar
mpirun -np 32 setFields -parallel
mpirun -np 32 interFoam -parallel
./crutch_for_region_setFields.sh
reconstructPar
mkdir pics
#pvpython script4.py
