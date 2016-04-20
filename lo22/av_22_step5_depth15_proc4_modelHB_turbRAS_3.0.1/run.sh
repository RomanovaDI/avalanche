#!/bin/bash
./delete.sh
cp 0/alpha.water.org 0/alpha.water
cp 0/region.org 0/region
decomposePar
mpirun -np 4 setFields -parallel
mpirun -np 4 interFoam -parallel
./crutch_for_region.sh
reconstructPar
#pvpython script.py
