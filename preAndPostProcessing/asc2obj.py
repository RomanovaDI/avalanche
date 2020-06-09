import numpy as np
from scipy import interpolate
from operator import add
import math
import readAsc as ra
import sys

def createSmall22(am): #am - altitude map
	file_slope = open("relief_22_s.asc", "w")
	file_slope.write('ncols         257\nnrows         227\nxllcorner     530195,48752344\nyllcorner     7503727,4955134\ncellsize      5\nNODATA_value  -9999\n')
	i = 0
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if i != it.multi_index[0]:
				i = it.multi_index[0]
				file_slope.write('\n')
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]] != am.NODATA_value and\
				am.altitude[it.multi_index[0],it.multi_index[1]+1] != am.NODATA_value and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]+1] != am.NODATA_value and\
				it.multi_index[1] - it.multi_index[0] * am.ny / am.nx - 0.3 * am.ny < 0 and\
				it.multi_index[1] - it.multi_index[0] * am.ny / am.nx + 0.4 * am.ny > 0 and\
				it.multi_index[1] + it.multi_index[0] * am.ny / am.nx - 1.5 * am.ny < 0:
					file_slope.write('%lf ' % (it[0]))
			else:
				file_slope.write('%d ' % (int(am.NODATA_value)))
			it.iternext()
	file_slope.close()

def createOBJ(am, height = 20): #am - altitude map
	print("Creating OBJ file.")
	file_obj = open("slope.obj", "w")
	file_obj_slope = open("slopeslope.obj", "w")
	alt_ind = np.zeros_like(am.altitude)
	i = 0
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]] != am.NODATA_value and\
				am.altitude[it.multi_index[0],it.multi_index[1]+1] != am.NODATA_value and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]+1] != am.NODATA_value:
					alt_ind[it.multi_index] = alt_ind[it.multi_index[0]+1,it.multi_index[1]] =\
						alt_ind[it.multi_index[0],it.multi_index[1]+1] = alt_ind[it.multi_index[0]+1,it.multi_index[1]+1] = 1
			it.iternext()
	n_vertices = 0
	for it in np.nditer(alt_ind, op_flags=['readwrite']):
		if it == 0:
			it[...] = -1
		else:
			it[...] = n_vertices
			n_vertices += 1
	fl = 0
	with np.nditer(alt_ind, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if it[0] > -1:
				file_obj.write('v %f %f %f\n' % (am.dx * it.multi_index[0], am.dx * it.multi_index[1],\
					am.altitude[it.multi_index] - am.alt_min))
				file_obj.write('v %f %f %f\n' % (am.dx * it.multi_index[0], am.dx * it.multi_index[1],\
					#am.alt_max - am.alt_min + height))
					am.altitude[it.multi_index] - am.alt_min + height))
				file_obj_slope.write('v %f %f %f\n' % (am.dx * it.multi_index[0], am.dx * it.multi_index[1],\
					am.altitude[it.multi_index] - am.alt_min))
				if fl == 0:
					print("Point inside the calculation area: (%f %f %f)" % (am.dx * it.multi_index[0] + 0.1 * am.dx,\
						am.dx * it.multi_index[1] + 0.1 * am.dx, am.altitude[it.multi_index] - am.alt_min + 0.5 * am.dx))
					fl = 1
			it.iternext()
	file_obj.write('g slope\n')
	n_layers = 2
	l1 = 1
	l2 = 2
	with np.nditer(alt_ind, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] > -1 and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				alt_ind[it.multi_index[0]+1,it.multi_index[1]] != -1 and\
				alt_ind[it.multi_index[0],it.multi_index[1]+1] != -1 and\
				alt_ind[it.multi_index[0]+1,it.multi_index[1]+1] != -1:
					file_obj.write('f %d %d %d\nf %d %d %d\n' % (it[0]*n_layers+l1, alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l1,\
						alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l1, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l1,\
						alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l1, alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*n_layers+l1))
			it.iternext()
	file_obj.write('g sides\n')
	with np.nditer(alt_ind, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] > -1 and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				alt_ind[it.multi_index[0]+1,it.multi_index[1]] != -1 and\
				alt_ind[it.multi_index[0],it.multi_index[1]+1] != -1 and\
				alt_ind[it.multi_index[0]+1,it.multi_index[1]+1] != -1:
					if	it.multi_index[1]-1 < 0 or\
						alt_ind[it.multi_index[0],it.multi_index[1]-1] == -1 or\
						alt_ind[it.multi_index[0]+1,it.multi_index[1]-1] == -1:
							file_obj.write('f %d %d %d\nf %d %d %d\n' % (it[0]*n_layers+l1, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l1,\
								it[0]*n_layers+l2, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l1,\
								alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l2, it[0]*n_layers+l2))
					if	it.multi_index[0]-1 < 0 or\
						alt_ind[it.multi_index[0]-1,it.multi_index[1]] == -1 or\
						alt_ind[it.multi_index[0]-1,it.multi_index[1]+1] == -1:
							file_obj.write('f %d %d %d\nf %d %d %d\n' % (it[0]*n_layers+l1, it[0]*n_layers+l2,\
								alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l1,\
								alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l1,\
								it[0]*n_layers+l2, alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l2))
					if	it.multi_index[1]+2 >= am.ny or\
						alt_ind[it.multi_index[0],it.multi_index[1]+2] == -1 or\
						alt_ind[it.multi_index[0]+1,it.multi_index[1]+2] == -1:
							file_obj.write('f %d %d %d\nf %d %d %d\n' % (alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l1,\
								alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l2, alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*n_layers+l1,\
								alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*n_layers+l1, alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l2,\
								alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*n_layers+l2))
					if	it.multi_index[0]+2 >= am.nx or\
						alt_ind[it.multi_index[0]+2,it.multi_index[1]] == -1 or\
						alt_ind[it.multi_index[0]+2,it.multi_index[1]+1] == -1:
							file_obj.write('f %d %d %d\nf %d %d %d\n' % (alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l1,\
								alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*n_layers+l1, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l2,\
								alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*n_layers+l1, alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*n_layers+l2,\
								alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l2))
			it.iternext()
	file_obj.write('g atmosphere\n')
	with np.nditer(alt_ind, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] > -1 and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				alt_ind[it.multi_index[0]+1,it.multi_index[1]] != -1 and\
				alt_ind[it.multi_index[0],it.multi_index[1]+1] != -1 and\
				alt_ind[it.multi_index[0]+1,it.multi_index[1]+1] != -1:
					file_obj.write('f %d %d %d\nf %d %d %d\n' % (it[0]*n_layers+l2, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l2,\
						alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l2, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l2,\
						alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*n_layers+l2, alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l2))
			it.iternext()
	file_obj.close()
	file_obj_slope.write('g slope\n')
	n_layers = 1
	l1 = 1
	with np.nditer(alt_ind, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] > -1 and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				alt_ind[it.multi_index[0]+1,it.multi_index[1]] != -1 and\
				alt_ind[it.multi_index[0],it.multi_index[1]+1] != -1 and\
				alt_ind[it.multi_index[0]+1,it.multi_index[1]+1] != -1:
					file_obj_slope.write('f %d %d %d\nf %d %d %d\n' % (it[0]*n_layers+l1, alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l1,\
						alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l1, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l1,\
						alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l1, alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*n_layers+l1))
			it.iternext()
	file_obj_slope.close()
	print("OBJ file is ready")

def createOBJrefine(am, height1 = 1): #am - altitude map, height1 - altitude of refinement area
	print("Creating refine OBJ file.")
	file_obj = open("refineSlope.obj", "w")
	alt_ind = np.zeros_like(am.altitude)
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]] != am.NODATA_value and\
				am.altitude[it.multi_index[0],it.multi_index[1]+1] != am.NODATA_value and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]+1] != am.NODATA_value:
					alt_ind[it.multi_index] = alt_ind[it.multi_index[0]+1,it.multi_index[1]] =\
						alt_ind[it.multi_index[0],it.multi_index[1]+1] = alt_ind[it.multi_index[0]+1,it.multi_index[1]+1] = 1
			it.iternext()
	n_vertices = 0
	for it in np.nditer(alt_ind, op_flags=['readwrite']):
		if it == 0:
			it[...] = -1
		else:
			it[...] = n_vertices
			n_vertices += 1
	n_layers = 2
	with np.nditer(alt_ind, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if it[0] > -1:
				file_obj.write('v %f %f %f\n' % (am.dx * it.multi_index[0], am.dx * it.multi_index[1],\
					am.altitude[it.multi_index] - am.alt_min))
				file_obj.write('v %f %f %f\n' % (am.dx * it.multi_index[0], am.dx * it.multi_index[1],\
					am.altitude[it.multi_index] - am.alt_min + height1))
			it.iternext()
	file_obj.write('g refineSlope\n')
	l1 = 1
	l2 = 2
	with np.nditer(alt_ind, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] > -1 and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				alt_ind[it.multi_index[0]+1,it.multi_index[1]] != -1 and\
				alt_ind[it.multi_index[0],it.multi_index[1]+1] != -1 and\
				alt_ind[it.multi_index[0]+1,it.multi_index[1]+1] != -1:
					file_obj.write('f %d %d %d\nf %d %d %d\n' % (it[0]*n_layers+l1, alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l1,\
						alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l1, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l1,\
						alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l1, alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*n_layers+l1))
					file_obj.write('f %d %d %d\nf %d %d %d\n' % (it[0]*n_layers+l2, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l2,\
						alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l2, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l2,\
						alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*n_layers+l2, alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l2))
					if	it.multi_index[1]-1 < 0 or\
						alt_ind[it.multi_index[0],it.multi_index[1]-1] == -1 or\
						alt_ind[it.multi_index[0]+1,it.multi_index[1]-1] == -1:
							file_obj.write('f %d %d %d\nf %d %d %d\n' % (it[0]*n_layers+l1, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l1,\
								it[0]*n_layers+l2, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l1,\
								alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l2, it[0]*n_layers+l2))
					if	it.multi_index[0]-1 < 0 or\
						alt_ind[it.multi_index[0]-1,it.multi_index[1]] == -1 or\
						alt_ind[it.multi_index[0]-1,it.multi_index[1]+1] == -1:
							file_obj.write('f %d %d %d\nf %d %d %d\n' % (it[0]*n_layers+l1, it[0]*n_layers+l2,\
								alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l1,\
								alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l1,\
								it[0]*n_layers+l2, alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l2))
					if	it.multi_index[1]+2 >= am.ny or\
						alt_ind[it.multi_index[0],it.multi_index[1]+2] == -1 or\
						alt_ind[it.multi_index[0]+1,it.multi_index[1]+2] == -1:
							file_obj.write('f %d %d %d\nf %d %d %d\n' % (alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l1,\
								alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l2, alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*n_layers+l1,\
								alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*n_layers+l1, alt_ind[it.multi_index[0],it.multi_index[1]+1]*n_layers+l2,\
								alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*n_layers+l2))
					if	it.multi_index[0]+2 >= am.nx or\
						alt_ind[it.multi_index[0]+2,it.multi_index[1]] == -1 or\
						alt_ind[it.multi_index[0]+2,it.multi_index[1]+1] == -1:
							file_obj.write('f %d %d %d\nf %d %d %d\n' % (alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l1,\
								alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*n_layers+l1, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l2,\
								alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*n_layers+l1, alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*n_layers+l2,\
								alt_ind[it.multi_index[0]+1,it.multi_index[1]]*n_layers+l2))
			it.iternext()
	file_obj.close()
	print("Refine OBJ file is ready")

def createBMD(am, height = 20): #am - altitude map, height1 - altitude of refinement area
	print("Creating blockMeshDict file")
	max_x = am.nx * am.dx
	max_y = am.ny * am.dx
	max_z = am.alt_max - am.alt_min + height
	blockMeshDictFileName = "blockMeshDict"
	file_blockMeshDict = open(blockMeshDictFileName, "w")
	file_blockMeshDict.write("FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tobject\tblockMeshDict;\n}\n\nconvertToMeters 1.0;\n\n")
	file_blockMeshDict.write("vertices\n(\n")
	file_blockMeshDict.write("\t(0\t0\t0)\n")
	file_blockMeshDict.write("\t(%f\t0\t0)\n" % (max_x))
	file_blockMeshDict.write("\t(%f\t%f\t0)\n" % (max_x, max_y))
	file_blockMeshDict.write("\t(0\t%f\t0)\n" % (max_y))
	file_blockMeshDict.write("\t(0\t0\t%f)\n" % (max_z))
	file_blockMeshDict.write("\t(%f\t0\t%f)\n" % (max_x, max_z))
	file_blockMeshDict.write("\t(%f\t%f\t%f)\n" % (max_x, max_y, max_z))
	file_blockMeshDict.write("\t(0\t%f\t%f)\n" % (max_y, max_z))
	file_blockMeshDict.write(");\n\nblocks\n(\n")
	file_blockMeshDict.write("\thex (0\t1\t2\t3\t4\t5\t6\t7)\t(%d %d %d) simpleGrading (1 1 1)\n" % \
		(math.ceil(max_x / am.dx), math.ceil(max_y / am.dx), math.ceil(max_z / am.dx)))
	file_blockMeshDict.write(");\n\nedges\n(\n);\n\nboundary\n(\n\allBoundary\n\t{\n\t\ttype patch;\n\t\tfaces\n\t\t(\n")
	file_blockMeshDict.write("\t\t\t(3 7 6 2)\n")
	file_blockMeshDict.write("\t\t\t(0 4 7 3)\n")
	file_blockMeshDict.write("\t\t\t(2 6 5 1)\n")
	file_blockMeshDict.write("\t\t\t(1 5 4 0)\n")
	file_blockMeshDict.write("\t\t\t(0 3 2 1)\n")
	file_blockMeshDict.write("\t\t\t(4 5 6 7)\n")
	file_blockMeshDict.write("\t\t);\n\t}\n);\n\nmergePatchPairs\n(\n);\n")
	file_blockMeshDict.close()
	print("blockMeshDict file is ready")

def createSetFields(am, rg, height = 2): #rg - region map, height - height of snow cover
	print("Creating setFieldsDict file.")
	file = open("setFieldsDict", "w")
	file.write('FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tlocation\t"system";\n\tobject\tsetFieldsDict;\n}\n')
	file.write('defaultFieldValues\n(\n\tvolScalarFieldValue alpha.water 0\n);\nregions\n(\n')
	with np.nditer(rg.region, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] == 0 and\
				am.altitude[it.multi_index] != am.NODATA_value:
				file.write('\tboxToCell\n\t{\n\t\tbox (%lf %lf %lf) (%lf %lf %lf);\n\t\tfieldValues\n\t\t(\n\t\t\tvolScalarFieldValue alpha.water 1\n\t\t);\n\t}\n' % (\
					it.multi_index[0] * am.dx, it.multi_index[1] * am.dx ,am.altitude[it.multi_index] - 1 - am.alt_min,\
					(it.multi_index[0] + 1) * am.dx, (it.multi_index[1] + 1) * am.dx, am.altitude[it.multi_index] - am.alt_min + height))
			it.iternext()
	file.write(');')
	file.close()
	print("setFieldsDict file is ready")

def main(argv):
	map_name, region_map_name, cellsize = ra.readFileNames(argv)
	slope = ra.asc(map_name, region_map_name)
	slope.am, slope.rg = ra.interpolateMap(slope.am, slope.rg, cellsize)
	createOBJ(slope.am, height = 20)
	createOBJrefine(slope.am, height1 = 1)
	createBMD(slope.am, height = 20)
	createSetFields(slope.am, slope.rg, height = 2)
	#createSmall22(slope.am)

if __name__== "__main__":
	main(sys.argv)