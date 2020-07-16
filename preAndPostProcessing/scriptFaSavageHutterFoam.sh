#!/bin/bash
#python3 asc2faSavageHutterFoam.py -m relief_22.asc -r region_22.asc -s 1.0
#python3 asc2faSavageHutterFoam.py -m relief_22.asc -r region_22.asc -s 2 -z 5
python3 asc2faSavageHutterFoam.py -m relief_22_s.asc -r region_22.asc -s 2 -z 5
#python3 asc2faSavageHutterFoam.py -m slope.asc -r slope_region.asc -s 2 -z 5