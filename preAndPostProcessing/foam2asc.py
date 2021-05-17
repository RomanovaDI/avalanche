import numpy as np
from scipy import interpolate
from operator import add
import math
import readAsc as ra
import blockMeshDict as bmd
import sys

def foam2asc(slopeAsc, depositField, height = 2): #slopeAsc - slope ASCII input, depositField - field of snow volume fraction
	print("Converting OpenFOAM calculation results to ASCII file.")
	inFile = open(depositField, "r")
	inFile.readline()
	inFile.readline()
	outFile = open("depositZoneOF.asc", "w")
	outFile.write('ncols         %f\nnrows         %f\nxllcorner     %f\nyllcorner     %f\ncellsize      %f\nNODATA_value  %f\n' % (\
				slopeAsc.ncols, slopeAsc.nrows, slopeAsc.xllcorner, slopeAsc.yllcorner,\
				slopeAsc.cellsize, slopeAsc.NODATA_value))
	am = slopeAsc.am
	ba = bmd.prepareSlopeData(am, height) # blockMeshDict array
	dep = np.full(am.altitude.shape, slopeAsc.region_NODATA_value)
	indent = 0
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			dep[it.multi_index] = folat(inFile.readline().split()[3])
			vert0 = it.multi_index
			vert1 = tuple(map(add, it.multi_index, (1, 0)))
			vert2 = tuple(map(add, it.multi_index, (1, 1)))
			vert3 = tuple(map(add, it.multi_index, (0, 1)))
			if	it[0] == 0 and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				rg.region[vert1] == 0 and\
				rg.region[vert2] == 0 and\
				rg.region[vert3] == 0:
					file.write('\trotatedBoxToCell\n\t{\n\t\torigin (%f %f %f);\n\t\ti (%f %f %f);\n\t\tj (%f %f %f);\n\t\tk (%f %f %f);\n\t\tfieldValues\n\t\t(\n\t\t\tvolScalarFieldValue alpha.water 1\n\t\t);\n\t}\n' % (\
						it.multi_index[0] * am.dx, it.multi_index[1] * am.dx, am.altitude[vert0] - am.alt_min + indent,\
						am.dx, 0, am.altitude[vert1] - am.altitude[vert0],\
						0, am.dx, am.altitude[vert3] - am.altitude[vert0],\
						0, 0, height))
			it.iternext()
	file.write(');')
	file.close()
	print("setFieldsDict file is ready")
