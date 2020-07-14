import numpy as np
from scipy import interpolate
from operator import add
import math
import readAsc as ra
import sys
import setFieldsDict as sfd
import blockMeshDict as bmd

def main(argv):
	map_name, region_map_name, cellsize, depthOfSnowCover, heightOfCalculationArea = ra.readFileNames(argv)
	slope = ra.asc(map_name, region_map_name)
	slope.am, slope.rg = ra.interpolateMap(slope.am, slope.rg, cellsize)
	bmd.createBlockMeshDictInclined(slope.am, height = slope.am.dx)
	#sfd.createSetFields(slope.am, slope.rg, height = 1)
	sfd.createInitialFields(slope.am, slope.rg, height = depthOfSnowCover)
	#sfd.createReleaseArea(slope.am, slope.rg, 2)

if __name__== "__main__":
	main(sys.argv)