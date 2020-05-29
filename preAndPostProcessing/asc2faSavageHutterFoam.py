import numpy as np
from scipy import interpolate
from operator import add
import math
import readAsc as ra
import sys

def createBMD_simple(am, height = 1, n_cells = 1): #am - altitude map, height1 - altitude of refinement area
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
			it.iternext()
	file_blockMeshDict.write("\t\t);\n\t}\n\tsides\n\t{\n\t\ttype patch;\n\t\tfaces\n\t\t(\n")
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
	print("Creating releaseArea file")
	contour = np.zeros_like(rg.region, dtype=int)
	#print(rg.region)
	with np.nditer(contour, flags=['multi_index'], op_flags=['writeonly']) as it:
		while not it.finished:
			if	rg.region[it.multi_index] == 0 and (\
				it.multi_index[0] + 1 >= rg.nx or\
				it.multi_index[1] + 1 >= rg.ny or\
				it.multi_index[0] - 1 < 0 or\
				it.multi_index[1] - 1 < 0 or\
				rg.region[it.multi_index[0]+1, it.multi_index[1]] == rg.NODATA_value or\
				rg.region[it.multi_index[0], it.multi_index[1]+1] == rg.NODATA_value or\
				rg.region[it.multi_index[0]-1, it.multi_index[1]] == rg.NODATA_value or\
				rg.region[it.multi_index[0], it.multi_index[1]-1] == rg.NODATA_value):
					it[0] = 1
			it.iternext()
	#print(contour)
	contour_num = np.sum(contour)
	#print(contour_num)
	ind = 1
	while ind != contour_num + 1:
		with np.nditer(contour, flags=['multi_index'], op_flags=['readwrite']) as it:
			while not it.finished:
				if	(ind == 1 and it[0] == 1) or (\
					ind > 1 and it[0] == 1 and (\
					it.multi_index[0] + 1 >= rg.nx or\
					it.multi_index[1] + 1 >= rg.ny or\
					it.multi_index[0] - 1 < 0 or\
					it.multi_index[1] - 1 < 0 or\
					contour[it.multi_index[0]+1, it.multi_index[1]+1] == ind or\
					contour[it.multi_index[0]-1, it.multi_index[1]+1] == ind or\
					contour[it.multi_index[0]-1, it.multi_index[1]-1] == ind or\
					contour[it.multi_index[0]+1, it.multi_index[1]-1] == ind or\
					contour[it.multi_index[0]+1, it.multi_index[1]] == ind or\
					contour[it.multi_index[0], it.multi_index[1]+1] == ind or\
					contour[it.multi_index[0]-1, it.multi_index[1]] == ind or\
					contour[it.multi_index[0], it.multi_index[1]-1] == ind)):
						ind += 1
						it[0] = ind
						#print(contour)
				it.iternext()
	ind = 1
	ind_s_x = 0
	ind_s_y = 0
	with np.nditer(contour, flags=['multi_index'], op_flags=['readwrite']) as it:
		while not it.finished:
			if ind == 1 and it[0] == 1:
				ind += 1
				it[0] = ind
				ind_s_x = it.multi_index[0]
				ind_s_y = it.multi_index[1]
				break
#	while ind != contour_num + 1:
#		neib = list(tuple(map(add, it.multi_index, (1, 1))),
#					tuple(map(add, it.multi_index, (-1, 1))),
#					tuple(map(add, it.multi_index, (-1, -1))),
#					tuple(map(add, it.multi_index, (1, -1))),
#					tuple(map(add, it.multi_index, (1, 0))),
#					tuple(map(add, it.multi_index, (0, 1))),
#					tuple(map(add, it.multi_index, (-1, 0))),
#					tuple(map(add, it.multi_index, (0, -1))))
#		for neib_t in neib:
#			if neib_t[0] >= 0 and neib_t[0] < rg.nx and neib_t[1] >= 0 and neib_t[1] < rg.ny and contour[neib_t] == 1:
#		with np.nditer(contour, flags=['multi_index'], op_flags=['readwrite']) as it:
#			while not it.finished:
#				if	(ind == 1 and it[0] == 1) or (\
#					ind > 1 and it[0] == 1 and (\
#					it.multi_index[0] + 1 >= rg.nx or\
#					it.multi_index[1] + 1 >= rg.ny or\
#					it.multi_index[0] - 1 < 0 or\
#					it.multi_index[1] - 1 < 0 or\
#					contour[it.multi_index[0]+1, it.multi_index[1]+1] == ind or\
#					contour[it.multi_index[0]-1, it.multi_index[1]+1] == ind or\
#					contour[it.multi_index[0]-1, it.multi_index[1]-1] == ind or\
#					contour[it.multi_index[0]+1, it.multi_index[1]-1] == ind or\
#					contour[it.multi_index[0]+1, it.multi_index[1]] == ind or\
#					contour[it.multi_index[0], it.multi_index[1]+1] == ind or\
#					contour[it.multi_index[0]-1, it.multi_index[1]] == ind or\
#					contour[it.multi_index[0], it.multi_index[1]-1] == ind)):
#						ind += 1
#						it[0] = ind
#						#print(contour)
#				it.iternext()
	#print(contour)
	print('Preprocessing is done')
	file = open("releaseArea", "w")
	file.write('FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tlocation\t"system";\n\tobject\treleaseArea;\n}')
	file.write('fields\n(\n\th\n\t{\n\t\tdefault 0;\n\t\tregions\n\t\t(')
	file.write('\t\t\treleaseArea1\n\t\t\t{\n\t\t\t\ttype polygon;\n\t\t\t\toffset (0 0 0);\n\t\t\t\tvertices\n\t\t\t\t(')
	for i in range(2, contour_num+2):
		with np.nditer(contour, flags=['multi_index'], op_flags=['readwrite']) as it:
			while not it.finished:
				if	it[0] == i:
					file.write('\t\t\t\t\t(%lf\t%lf\t0)' % (it.multi_index[0] * rg.dx, it.multi_index[1] * rg.dx))
					break
			it.iternext()
	file.write('\t\t\t\tvalue 0.5;\n\t\t\t}')
	file.write('\t\t);\n\t}\n);')
	file.close()
	print("releaseArea file is ready")

def createSetFields(am, rg, height = 2): #rg - region map, height - height of snow cover
	print("Creating setFieldsDict file.")
	file = open("setFieldsDict", "w")
	file.write('FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tlocation\t"system";\n\tobject\tsetFieldsDict;\n}')
	file.write('defaultFieldValues\n(\n\tvolScalarFieldValue h 0\n);\nregions\n(\n')
	with np.nditer(rg.region, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] == 0 and\
				am.altitude[it.multi_index] != am.NODATA_value:
				file.write('\tboxToCell\n\t{\n\t\tbox (%lf %lf %lf) (%lf %lf %lf);\n\t\tfieldValues\n\t\t(\n\t\t\tvolScalarFieldValue h 0.5\n\t\t);\n\t}' % (\
					it.multi_index[0] * am.dx, it.multi_index[1] * am.dx ,am.altitude[it.multi_index],\
					(it.multi_index[0] + 1) * am.dx, (it.multi_index[1] + 1) * am.dx, am.altitude[it.multi_index] + height))
			it.iternext()
	file.write(');')
	file.close()
	print("setFieldsDict file is ready")

def createInitialFields(am, rg, height = 0.5): #rg - region map, height - height of snow cover
	print("Creating initial fields files.")
	#np.savetxt('tmp.out', rg.region)
	number = 0
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]] != am.NODATA_value and\
				am.altitude[it.multi_index[0],it.multi_index[1]+1] != am.NODATA_value and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]+1] != am.NODATA_value:
					number += 1
			it.iternext()
	file = open("h", "w")
	file.write('FoamFile\n{\n\tversion\t2.0;\n\t format\tascii;\n\tclass\tareaScalarField;\n\tlocation\t"0";\n\tobject\th;\n}\n')
	file.write('dimensions\t[0 1 0 0 0 0 0];\ninternalField\tnonuniform List<scalar>\n')
	file.write('%d\n(\n' % (number))
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]] != am.NODATA_value and\
				am.altitude[it.multi_index[0],it.multi_index[1]+1] != am.NODATA_value and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]+1] != am.NODATA_value:
				value = height if rg.region[it.multi_index] == 0 else 0
				file.write('%lf\n' % (value))
			it.iternext()
	file.write(')\n;\n')
	file.write('boundaryField\n{\n\tsides\n\t{\n\t\ttype\t\tinletOutlet;\n\t\tphi\t\tphis;\n\t\tinletValue\t\tuniform 0;\n\t\tvalue\t\tuniform 0;\n\t}\n}\n')
	file.close()
	file = open("H", "w")
	file.write('FoamFile\n{\n\tversion\t2.0;\n\t format\tascii;\n\tclass\tareaScalarField;\n\tlocation\t"0";\n\tobject\th;\n}\n')
	file.write('dimensions\t[0 1 0 0 0 0 0];\ninternalField\tuniform 0;\n')
	file.write('boundaryField\n{\n\tsides\n\t{\n\t\ttype\t\tcalculated;\n\t\tvalue\t\tuniform 0;\n\t}\n')
	file.write('\tslope\n\t{\n\t\ttype\t\tcalculated;\n\t\tvalue\t\tnonuniform List<scalar>\n')
	file.write('%d\n(\n' % (number))
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]] != am.NODATA_value and\
				am.altitude[it.multi_index[0],it.multi_index[1]+1] != am.NODATA_value and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]+1] != am.NODATA_value:
				value = height if rg.region[it.multi_index] == 0 else 0
				file.write('%lf\n' % (value))
			it.iternext()
	file.write(')\n;\n\t}\n')
	file.write('\tatmosphere\n\t{\n\t\ttype\t\tcalculated;\n\t\tvalue\t\tuniform 0;\n\t}\n}\n')
	file.close()
	file = open("Us", "w")
	file.write('FoamFile\n{\n\tversion\t2.0;\n\t format\tascii;\n\tclass\tareaVectorField;\n\tlocation\t"0";\n\tobject\tUs;\n}\n')
	file.write('dimensions\t[0 1 -1 0 0 0 0];\ninternalField\tuniform (0 0 0);\n')
	file.write('boundaryField\n{\n\tsides\n\t{\n\t\ttype\t\tinletOutlet;\n\t\tphi\t\tphis;\n\t\tinletValue\t\tuniform (0 0 0);\n\t\tvalue\t\tuniform (0 0 0);\n\t}\n}\n')
	file.close()
	print("Initial fields files are ready")

def main(argv):
	map_name, region_map_name, cellsize = ra.readFileNames(argv)
	slope = ra.asc(map_name, region_map_name)
	slope.am, slope.rg = ra.interpolateMap(slope.am, slope.rg, cellsize)
	createBMD_simple(slope.am, height = 1, n_cells = 1)
	createSetFields(slope.am, slope.rg, height = 1)
	createInitialFields(slope.am, slope.rg, height = 0.5)
	#createReleaseArea(slope.am, slope.rg, 2)

if __name__== "__main__":
	main(sys.argv)