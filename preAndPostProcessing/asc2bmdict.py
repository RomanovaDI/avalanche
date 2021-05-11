import numpy as np
from scipy import interpolate
from operator import add
import math
import sys
import readAsc as ra
import setFieldsDict as sfd
import blockMeshDict as bmd

def main(argv):
	map_name, region_map_name, cellsize, depthOfSnowCover, heightOfCalculationArea = ra.readFileNames(argv)
	slope = ra.asc(map_name, region_map_name)
	slope.am, slope.rg = ra.interpolateMap(slope.am, slope.rg, cellsize)
	#bmd.createBlockMeshDict(slope.am, height=heightOfCalculationArea)
	bmd.createBlockMeshDictInclined(slope.am, height=heightOfCalculationArea)
#	sfd.createSetFieldsFourPhasesRotated(slope.am, slope.rg, height=depthOfSnowCover)
#	sfd.createSetFieldsRotated(slope.am, slope.rg, height=depthOfSnowCover)
	sfd.createSetFieldsRotatedStartFinish(slope.am, slope.rg, height=depthOfSnowCover)
	#sfd.createSetFields(slope.am, slope.rg, height=heightOfCalculationArea)
	sfd.createTopoSetRotatedStartFinish(slope.am, slope.rg, height=heightOfCalculationArea)

if __name__== "__main__":
	main(sys.argv)
