import numpy as np
from scipy import interpolate
from operator import add
import math
import readAsc as ra

def createBMD_simple(am, height = 20, n_cells = 1): #am - altitude map, height1 - altitude of refinement area
	print("Creating blockMeshDict file")
	blockMeshDictFileName = "blockMeshDict"
	file_blockMeshDict = open(blockMeshDictFileName, "w")
	file_blockMeshDict.write("FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tobject\tblockMeshDict;\n}\n\nconvertToMeters 1.0;\n\n")
	file_blockMeshDict.write("vertices\n(\n")
	alt_ind = np.zeros_like(am.altitude)
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]] != am.NODATA_value and\
				am.altitude[it.multi_index[0],it.multi_index[1]+1] != am.NODATA_value and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]+1] != am.NODATA_value:# and\
				#it.multi_index[1] - it.multi_index[0] * am.ny / am.nx - 0.3 * am.ny < 0 and\
				#it.multi_index[1] - it.multi_index[0] * am.ny / am.nx + 0.4 * am.ny > 0 and\
				#it.multi_index[1] + it.multi_index[0] * am.ny / am.nx - 1.5 * am.ny < 0: #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! last 3 lines only for 22 slope
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
	with np.nditer(alt_ind, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] != -1:
				file_blockMeshDict.write("\t(%f\t%f\t%f)\n" % (it.multi_index[0] * am.dx, it.multi_index[1] * am.dx, am.altitude[it.multi_index]))
				file_blockMeshDict.write("\t(%f\t%f\t%f)\n" % (it.multi_index[0] * am.dx, it.multi_index[1] * am.dx, am.altitude[it.multi_index] + height))
			it.iternext()
	file_blockMeshDict.write(");\n\nblocks\n(\n")
	with np.nditer(alt_ind, flags=['multi_index'], op_flags=["readonly"]) as it:
		while not it.finished:
			if	it[0] != -1 and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				alt_ind[it.multi_index[0]+1,it.multi_index[1]] != -1 and\
				alt_ind[it.multi_index[0],it.multi_index[1]+1] != -1 and\
				alt_ind[it.multi_index[0]+1,it.multi_index[1]+1] != -1:
					vert0 = 2 * alt_ind[it.multi_index]
					vert1 = 2 * alt_ind[tuple(map(add, it.multi_index, (1, 0)))]
					vert2 = 2 * alt_ind[tuple(map(add, it.multi_index, (1, 1)))]
					vert3 = 2 * alt_ind[tuple(map(add, it.multi_index, (0, 1)))]
					file_blockMeshDict.write("\thex (%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d)\t(1 1 %d) simpleGrading (1 1 1)\n" % \
						(vert0, vert1, vert2, vert3, vert0 + 1, vert1 + 1, vert2 + 1, vert3 + 1, n_cells))
			it.iternext()
	file_blockMeshDict.write(");\n\nedges\n(\n);\n\nboundary\n(\n\tslope\n\t{\n\t\ttype wall;\n\t\tfaces\n\t\t(\n")
	with np.nditer(alt_ind, flags=['multi_index'], op_flags=["readonly"]) as it:
		while not it.finished:
			if	it[0] != -1 and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				alt_ind[it.multi_index[0]+1,it.multi_index[1]] != -1 and\
				alt_ind[it.multi_index[0],it.multi_index[1]+1] != -1 and\
				alt_ind[it.multi_index[0]+1,it.multi_index[1]+1] != -1:
					vert0 = 2 * alt_ind[it.multi_index]
					vert1 = 2 * alt_ind[tuple(map(add, it.multi_index, (1, 0)))]
					vert2 = 2 * alt_ind[tuple(map(add, it.multi_index, (1, 1)))]
					vert3 = 2 * alt_ind[tuple(map(add, it.multi_index, (0, 1)))]
					file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vert3, vert2, vert1, vert0))
			it.iternext()
	file_blockMeshDict.write("\t\t);\n\t}\n\tatmosphere\n\t{\n\t\ttype patch;\n\t\tfaces\n\t\t(\n")
	with np.nditer(alt_ind, flags=['multi_index'], op_flags=["readonly"]) as it:
		while not it.finished:
			if	it[0] != -1 and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				alt_ind[it.multi_index[0]+1,it.multi_index[1]] != -1 and\
				alt_ind[it.multi_index[0],it.multi_index[1]+1] != -1 and\
				alt_ind[it.multi_index[0]+1,it.multi_index[1]+1] != -1:
					vert0 = 2 * alt_ind[it.multi_index]
					vert1 = 2 * alt_ind[tuple(map(add, it.multi_index, (1, 0)))]
					vert2 = 2 * alt_ind[tuple(map(add, it.multi_index, (1, 1)))]
					vert3 = 2 * alt_ind[tuple(map(add, it.multi_index, (0, 1)))]
					file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vert0 + 1, vert1 + 1, vert2 + 1, vert3 + 1))
					neighbour_ind1 = tuple(map(add, it.multi_index, (-1, 0)))
					neighbour_ind2 = tuple(map(add, it.multi_index, (-1, 1)))
					if neighbour_ind1[0] < 0 or alt_ind[neighbour_ind1] == -1 or alt_ind[neighbour_ind2] == -1:
						file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vert0, vert0 + 1, vert3 + 1, vert3))
					neighbour_ind1 = tuple(map(add, it.multi_index, (2, 0)))
					neighbour_ind2 = tuple(map(add, it.multi_index, (2, 1)))
					if neighbour_ind1[0] >= am.nx or alt_ind[neighbour_ind1] == -1 or alt_ind[neighbour_ind2] == -1:
						file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vert1, vert2, vert2 + 1, vert1 + 1))
					neighbour_ind1 = tuple(map(add, it.multi_index, (0, -1)))
					neighbour_ind2 = tuple(map(add, it.multi_index, (1, -1)))
					if neighbour_ind1[1] < 0 or alt_ind[neighbour_ind1] == -1 or alt_ind[neighbour_ind2] == -1:
						file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vert0, vert1, vert1 + 1, vert0 + 1))
					neighbour_ind1 = tuple(map(add, it.multi_index, (0, 2)))
					neighbour_ind2 = tuple(map(add, it.multi_index, (1, 2)))
					if neighbour_ind1[1] >= am.ny or alt_ind[neighbour_ind1] == -1 or alt_ind[neighbour_ind2] == -1:
						file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vert2, vert3, vert3 + 1, vert2 + 1))
			it.iternext()
	file_blockMeshDict.write("\t\t);\n\t}\n);\n\nmergePatchPairs\n(\n);\n")
	file_blockMeshDict.close()
	print("blockMeshDict file is ready")

def createReleaseArea(am, rg, height = 2):#rg - region map, height - height of snow cover
	print("Creating releaseArea file.")
	file = open("releaseArea", "w")
	file.write('FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tlocation\t"system";\n\tobject\treleaseArea;\n}')
	file.write('fields\n(\n\th\n\t{\n\t\tdefault 0;\n\t\tregions\n\t\t(')
	file.write('\t\t\treleaseArea1\n\t\t\t{\n\t\t\t\ttype polygon;\n\t\t\t\toffset (0 0 0);\n\t\t\t\tvertices\n\t\t\t\t(')
	file.write('\t\t\t\t\t(%lf\t%lf\t%lf)\n\t\t\t\t\t(%lf\t%lf\t%lf)\n\t\t\t\t\t(%lf\t%lf\t%lf)\n\t\t\t\t\t(%lf\t%lf\t%lf)\n\t\t\t\t);\n\t\t\t\tvalue 0.5;\n\t\t\t}' %\
		(it.multi_index[0] * am.dx, it.multi_index[1] * am.dx, 0, (it.multi_index[0] + 1) * am.dx, it.multi_index[1] * am.dx, 0,\
		(it.multi_index[0] + 1) * am.dx, (it.multi_index[1] + 1) * am.dx, 0, it.multi_index[0] * am.dx, (it.multi_index[1] + 1) * am.dx, 0))
	file.write('\t\t);\n\t}\n);')

	file.write('defaultFieldValues\n(\n\tvolScalarFieldValue alpha.water 0\n);\nregions\n(\n')
	with np.nditer(rg.region, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] == 0 and\
				am.altitude[it.multi_index] != am.NODATA_value:
				file.write('\tboxToCell\n\t{\n\t\tbox (%lf %lf %lf) (%lf %lf %lf);\n\t\tfieldValues\n\t\t(\n\t\t\tvolScalarFieldValue alpha.water 1\n\t\t);\n\t}' % (\
					it.multi_index[0] * am.dx, it.multi_index[1] * am.dx ,am.altitude[it.multi_index],\
					(it.multi_index[0] + 1) * am.dx, (it.multi_index[1] + 1) * am.dx, am.altitude[it.multi_index] + height))
			it.iternext()
	file.write(');')
	file.close()
	print("releaseArea file is ready")

def main():
	map_name, region_map_name = ra.readFileNames()
	slope = ra.asc(map_name, region_map_name)
	createBMD_simple(slope.am, height = 10, n_cells = 1)
	createReleaseArea(slope.am, slope.rg, 2)

if __name__== "__main__":
	main()