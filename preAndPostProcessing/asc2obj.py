import numpy as np
from scipy import interpolate
from operator import add
import math
import readAsc as ra

def createOBJ(am, height = 16, height1 = 2, indent = 10): #am - altitude map
	print("Creating OBJ file.")
	indent = int(math.ceil(indent / am.dx) * am.dx)
	file_obj = open("slope.obj", "w")
	alt_ind = np.zeros_like(am.altitude)
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]] != am.NODATA_value and\
				am.altitude[it.multi_index[0],it.multi_index[1]+1] != am.NODATA_value and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]+1] != am.NODATA_value and\
				it.multi_index[1] - it.multi_index[0] * am.ny / am.nx - 0.3 * am.ny < 0 and\
				it.multi_index[1] - it.multi_index[0] * am.ny / am.nx + 0.4 * am.ny > 0 and\
				it.multi_index[1] + it.multi_index[0] * am.ny / am.nx - 1.5 * am.ny < 0:
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
	n_layers = 2
	with np.nditer(alt_ind, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if it[0] > -1:
				file_obj.write('v %f %f %f\n' % (am.dx * it.multi_index[0] + indent, am.dx * it.multi_index[1] + indent,\
					am.altitude[it.multi_index] - am.alt_min + indent))
				file_obj.write('v %f %f %f\n' % (am.dx * it.multi_index[0] + indent, am.dx * it.multi_index[1] + indent,\
					am.alt_max - am.alt_min + height + indent))
					#am.altitude[it.multi_index] - am.alt_min + height + indent))
				if fl == 0:
					print("Point inside the calculation area: (%f %f %f)" % (am.dx * it.multi_index[0] + indent + 0.1 * am.dx,\
						am.dx * it.multi_index[1] + indent + 0.1 * am.dx, am.altitude[it.multi_index] - am.alt_min + indent + 0.5 * am.dx))
					fl = 1
			it.iternext()
	file_obj.write('g slope\n')
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
	print("OBJ file is ready")
	print("Creating refine OBJ file.")
	indent = int(math.ceil(indent / am.dx) * am.dx)
	file_obj = open("refineSlope.obj", "w")
	alt_ind = np.zeros_like(am.altitude)
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]] != am.NODATA_value and\
				am.altitude[it.multi_index[0],it.multi_index[1]+1] != am.NODATA_value and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]+1] != am.NODATA_value and\
				it.multi_index[1] - it.multi_index[0] * am.ny / am.nx - 0.3 * am.ny < 0 and\
				it.multi_index[1] - it.multi_index[0] * am.ny / am.nx + 0.4 * am.ny > 0 and\
				it.multi_index[1] + it.multi_index[0] * am.ny / am.nx - 1.5 * am.ny < 0:
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
				file_obj.write('v %f %f %f\n' % (am.dx * it.multi_index[0] + indent, am.dx * it.multi_index[1] + indent,\
					am.altitude[it.multi_index] - am.alt_min + indent))
				file_obj.write('v %f %f %f\n' % (am.dx * it.multi_index[0] + indent, am.dx * it.multi_index[1] + indent,\
					am.altitude[it.multi_index] - am.alt_min + height1 + indent))
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
	print("Creating blockMeshDict file")
	max_x = am.nx * am.dx + 2 * indent
	max_y = am.ny * am.dx + 2 * indent
	max_z = am.alt_max - am.alt_min + 2 * indent
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

def main():
	map_name, region_map_name = ra.readFileNames()
	slope = ra.asc(map_name, region_map_name)
	createOBJ(slope.am, 10)

if __name__== "__main__":
	main()