import numpy as np
from scipy import interpolate
from operator import add
import math
import readAsc as ra
import sys

def writeFacet(file, v1, v2, v3):
	v1 = np.array(v1)
	v2 = np.array(v2)
	v3 = np.array(v3)
	n = np.cross(v2-v1, v3-v1)
	n = n / n.sum()
	file.write('facet normal %lf %lf %lf\n  outer loop\n    vertex %lf %lf %lf\n    vertex %lf %lf %lf\n    vertex %lf %lf %lf\n  endloop\nendfacet\n' %\
		(n[0], n[1], n[2], v1[0], v1[1], v1[2], v2[0], v2[1], v2[2], v3[0], v3[1], v3[2]))

def createASCII_STL(am, height_area = 20, height_refinement = 1):
	print('Creating STL files:\nCreating slope STL')
	flag = 1
	fileName = 'slope.stl'
	file = open(fileName, 'w')
	file.write('solid slope\n')
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			vert0 = it.multi_index
			vert1 = tuple(map(add, it.multi_index, (1, 0)))
			vert2 = tuple(map(add, it.multi_index, (1, 1)))
			vert3 = tuple(map(add, it.multi_index, (0, 1)))
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				am.altitude[vert1] != am.NODATA_value and\
				am.altitude[vert2] != am.NODATA_value and\
				am.altitude[vert3] != am.NODATA_value:# and\
				#it.multi_index[1] - it.multi_index[0] * am.ny / am.nx - 0.3 * am.ny < 0 and\
				#it.multi_index[1] - it.multi_index[0] * am.ny / am.nx + 0.4 * am.ny > 0 and\
				#it.multi_index[1] + it.multi_index[0] * am.ny / am.nx - 1.5 * am.ny < 0: #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! last 3 lines only for 22 slope
					if flag == 1 and vert0[0] > am.nx / 2 and vert0[1] > am.ny / 2:
						print('Point inside slope: (%lf %lf %lf)' %\
							((vert0[0] + 0.5) * am.dx, (vert0[1] + 0.5) * am.dx, it[0] + height_area / 2 - am.alt_min))
						flag = 0
					writeFacet(file, [vert0[0] * am.dx, vert0[1] * am.dx, it[0] - am.alt_min],\
						[vert3[0] * am.dx, vert3[1] * am.dx, am.altitude[vert3] - am.alt_min],\
						[vert2[0] * am.dx, vert2[1] * am.dx, am.altitude[vert2] - am.alt_min])
					writeFacet(file, [vert0[0] * am.dx, vert0[1] * am.dx, it[0] - am.alt_min],\
						[vert2[0] * am.dx, vert2[1] * am.dx, am.altitude[vert2] - am.alt_min],\
						[vert1[0] * am.dx, vert1[1] * am.dx, am.altitude[vert1] - am.alt_min])
			it.iternext()
	file.write('endsolid slope\n')
	file.write('solid sides\n')
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			vert0 = it.multi_index
			vert1 = tuple(map(add, it.multi_index, (1, 0)))
			vert2 = tuple(map(add, it.multi_index, (1, 1)))
			vert3 = tuple(map(add, it.multi_index, (0, 1)))
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				am.altitude[vert1] != am.NODATA_value and\
				am.altitude[vert2] != am.NODATA_value and\
				am.altitude[vert3] != am.NODATA_value:# and\
				#it.multi_index[1] - it.multi_index[0] * am.ny / am.nx - 0.3 * am.ny < 0 and\
				#it.multi_index[1] - it.multi_index[0] * am.ny / am.nx + 0.4 * am.ny > 0 and\
				#it.multi_index[1] + it.multi_index[0] * am.ny / am.nx - 1.5 * am.ny < 0: #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! last 3 lines only for 22 slope
					neighbour_ind1 = tuple(map(add, it.multi_index, (-1, 0)))
					neighbour_ind2 = tuple(map(add, it.multi_index, (-1, 1)))
					if neighbour_ind1[0] < 0 or am.altitude[neighbour_ind1] == am.NODATA_value or am.altitude[neighbour_ind2] == am.NODATA_value:
						writeFacet(file, [vert0[0] * am.dx, vert0[1] * am.dx, it[0] - am.alt_min],\
							[vert0[0] * am.dx, vert0[1] * am.dx, it[0] + height_area - am.alt_min],\
							[vert3[0] * am.dx, vert3[1] * am.dx, am.altitude[vert3] + height_area - am.alt_min])
						writeFacet(file, [vert0[0] * am.dx, vert0[1] * am.dx, it[0] - am.alt_min],\
							[vert3[0] * am.dx, vert3[1] * am.dx, am.altitude[vert3] + height_area - am.alt_min],\
							[vert3[0] * am.dx, vert3[1] * am.dx, am.altitude[vert3] - am.alt_min])
					neighbour_ind1 = tuple(map(add, it.multi_index, (2, 0)))
					neighbour_ind2 = tuple(map(add, it.multi_index, (2, 1)))
					if neighbour_ind1[0] >= am.nx or am.altitude[neighbour_ind1] == am.NODATA_value or am.altitude[neighbour_ind2] == am.NODATA_value:
						writeFacet(file, [vert1[0] * am.dx, vert1[1] * am.dx, am.altitude[vert1] - am.alt_min],\
							[vert2[0] * am.dx, vert2[1] * am.dx, am.altitude[vert2] - am.alt_min],\
							[vert2[0] * am.dx, vert2[1] * am.dx, am.altitude[vert2] + height_area - am.alt_min])
						writeFacet(file, [vert1[0] * am.dx, vert1[1] * am.dx, am.altitude[vert1] - am.alt_min],\
							[vert2[0] * am.dx, vert2[1] * am.dx, am.altitude[vert2] + height_area - am.alt_min],\
							[vert1[0] * am.dx, vert1[1] * am.dx, am.altitude[vert1] + height_area - am.alt_min])
					neighbour_ind1 = tuple(map(add, it.multi_index, (0, -1)))
					neighbour_ind2 = tuple(map(add, it.multi_index, (1, -1)))
					if neighbour_ind1[1] < 0 or am.altitude[neighbour_ind1] == am.NODATA_value or am.altitude[neighbour_ind2] == am.NODATA_value:
						writeFacet(file, [vert0[0] * am.dx, vert0[1] * am.dx, it[0] - am.alt_min],\
							[vert1[0] * am.dx, vert1[1] * am.dx, am.altitude[vert1] - am.alt_min],\
							[vert1[0] * am.dx, vert1[1] * am.dx, am.altitude[vert1] + height_area - am.alt_min])
						writeFacet(file, [vert0[0] * am.dx, vert0[1] * am.dx, it[0] - am.alt_min],\
							[vert1[0] * am.dx, vert1[1] * am.dx, am.altitude[vert1] + height_area - am.alt_min],\
							[vert0[0] * am.dx, vert0[1] * am.dx, it[0] + height_area - am.alt_min])
					neighbour_ind1 = tuple(map(add, it.multi_index, (0, 2)))
					neighbour_ind2 = tuple(map(add, it.multi_index, (1, 2)))
					if neighbour_ind1[1] >= am.ny or am.altitude[neighbour_ind1] == am.NODATA_value or am.altitude[neighbour_ind2] == am.NODATA_value:
						writeFacet(file, [vert2[0] * am.dx, vert2[1] * am.dx, am.altitude[vert2] - am.alt_min],\
							[vert3[0] * am.dx, vert3[1] * am.dx, am.altitude[vert3] - am.alt_min],\
							[vert3[0] * am.dx, vert3[1] * am.dx, am.altitude[vert3] + height_area - am.alt_min])
						writeFacet(file, [vert2[0] * am.dx, vert2[1] * am.dx, am.altitude[vert2] - am.alt_min],\
							[vert3[0] * am.dx, vert3[1] * am.dx, am.altitude[vert3] + height_area - am.alt_min],\
							[vert2[0] * am.dx, vert2[1] * am.dx, am.altitude[vert2] + height_area - am.alt_min])
			it.iternext()
	file.write('endsolid sides\n')
	file.write('solid atmosphere\n')
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			vert0 = it.multi_index
			vert1 = tuple(map(add, it.multi_index, (1, 0)))
			vert2 = tuple(map(add, it.multi_index, (1, 1)))
			vert3 = tuple(map(add, it.multi_index, (0, 1)))
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				am.altitude[vert1] != am.NODATA_value and\
				am.altitude[vert2] != am.NODATA_value and\
				am.altitude[vert3] != am.NODATA_value:# and\
				#it.multi_index[1] - it.multi_index[0] * am.ny / am.nx - 0.3 * am.ny < 0 and\
				#it.multi_index[1] - it.multi_index[0] * am.ny / am.nx + 0.4 * am.ny > 0 and\
				#it.multi_index[1] + it.multi_index[0] * am.ny / am.nx - 1.5 * am.ny < 0: #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! last 3 lines only for 22 slope
					writeFacet(file, [vert0[0] * am.dx, vert0[1] * am.dx, it[0] + height_area - am.alt_min],\
						[vert2[0] * am.dx, vert2[1] * am.dx, am.altitude[vert2] + height_area - am.alt_min],\
						[vert3[0] * am.dx, vert3[1] * am.dx, am.altitude[vert3] + height_area - am.alt_min])
					writeFacet(file, [vert0[0] * am.dx, vert0[1] * am.dx, it[0] + height_area - am.alt_min],\
						[vert1[0] * am.dx, vert1[1] * am.dx, am.altitude[vert1] + height_area - am.alt_min],\
						[vert2[0] * am.dx, vert2[1] * am.dx, am.altitude[vert2] + height_area - am.alt_min])
			it.iternext()
	file.write('endsolid atmosphere\n')
	file.close()
	print('Slope STL file is ready\nCreating refine area STL')
	flag = 1
	fileName = 'refineSlope.stl'
	file = open(fileName, 'w')
	file.write('solid slope_refine\n')
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			vert0 = it.multi_index
			vert1 = tuple(map(add, it.multi_index, (1, 0)))
			vert2 = tuple(map(add, it.multi_index, (1, 1)))
			vert3 = tuple(map(add, it.multi_index, (0, 1)))
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				am.altitude[vert1] != am.NODATA_value and\
				am.altitude[vert2] != am.NODATA_value and\
				am.altitude[vert3] != am.NODATA_value:# and\
				#it.multi_index[1] - it.multi_index[0] * am.ny / am.nx - 0.3 * am.ny < 0 and\
				#it.multi_index[1] - it.multi_index[0] * am.ny / am.nx + 0.4 * am.ny > 0 and\
				#it.multi_index[1] + it.multi_index[0] * am.ny / am.nx - 1.5 * am.ny < 0: #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! last 3 lines only for 22 slope
					if flag == 1:
						print('Point inside refine area of slope: (%lf %lf %lf)' %\
							((vert0[0] + 0.5) * am.dx, (vert0[1] + 0.5) * am.dx, it[0] + height_refinement / 2 - am.alt_min))
						flag = 0
					writeFacet(file, [vert0[0] * am.dx, vert0[1] * am.dx, it[0] - am.alt_min],\
						[vert3[0] * am.dx, vert3[1] * am.dx, am.altitude[vert3] - am.alt_min],\
						[vert2[0] * am.dx, vert2[1] * am.dx, am.altitude[vert2] - am.alt_min])
					writeFacet(file, [vert0[0] * am.dx, vert0[1] * am.dx, it[0] - am.alt_min],\
						[vert2[0] * am.dx, vert2[1] * am.dx, am.altitude[vert2] - am.alt_min],\
						[vert1[0] * am.dx, vert1[1] * am.dx, am.altitude[vert1] - am.alt_min])
			it.iternext()
	file.write('endsolid slope_refine\n')
	file.write('solid sides_refine\n')
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			vert0 = it.multi_index
			vert1 = tuple(map(add, it.multi_index, (1, 0)))
			vert2 = tuple(map(add, it.multi_index, (1, 1)))
			vert3 = tuple(map(add, it.multi_index, (0, 1)))
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				am.altitude[vert1] != am.NODATA_value and\
				am.altitude[vert2] != am.NODATA_value and\
				am.altitude[vert3] != am.NODATA_value:# and\
				#it.multi_index[1] - it.multi_index[0] * am.ny / am.nx - 0.3 * am.ny < 0 and\
				#it.multi_index[1] - it.multi_index[0] * am.ny / am.nx + 0.4 * am.ny > 0 and\
				#it.multi_index[1] + it.multi_index[0] * am.ny / am.nx - 1.5 * am.ny < 0: #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! last 3 lines only for 22 slope
					neighbour_ind1 = tuple(map(add, it.multi_index, (-1, 0)))
					neighbour_ind2 = tuple(map(add, it.multi_index, (-1, 1)))
					if neighbour_ind1[0] < 0 or am.altitude[neighbour_ind1] == am.NODATA_value or am.altitude[neighbour_ind2] == am.NODATA_value:
						writeFacet(file, [vert0[0] * am.dx, vert0[1] * am.dx, it[0] - am.alt_min],\
							[vert0[0] * am.dx, vert0[1] * am.dx, it[0] + height_refinement - am.alt_min],\
							[vert3[0] * am.dx, vert3[1] * am.dx, am.altitude[vert3] + height_refinement - am.alt_min])
						writeFacet(file, [vert0[0] * am.dx, vert0[1] * am.dx, it[0] - am.alt_min],\
							[vert3[0] * am.dx, vert3[1] * am.dx, am.altitude[vert3] + height_refinement - am.alt_min],\
							[vert3[0] * am.dx, vert3[1] * am.dx, am.altitude[vert3] - am.alt_min])
					neighbour_ind1 = tuple(map(add, it.multi_index, (2, 0)))
					neighbour_ind2 = tuple(map(add, it.multi_index, (2, 1)))
					if neighbour_ind1[0] >= am.nx or am.altitude[neighbour_ind1] == am.NODATA_value or am.altitude[neighbour_ind2] == am.NODATA_value:
						writeFacet(file, [vert1[0] * am.dx, vert1[1] * am.dx, am.altitude[vert1] - am.alt_min],\
							[vert2[0] * am.dx, vert2[1] * am.dx, am.altitude[vert2] - am.alt_min],\
							[vert2[0] * am.dx, vert2[1] * am.dx, am.altitude[vert2] + height_refinement - am.alt_min])
						writeFacet(file, [vert1[0] * am.dx, vert1[1] * am.dx, am.altitude[vert1] - am.alt_min],\
							[vert2[0] * am.dx, vert2[1] * am.dx, am.altitude[vert2] + height_refinement - am.alt_min],\
							[vert1[0] * am.dx, vert1[1] * am.dx, am.altitude[vert1] + height_refinement - am.alt_min])
					neighbour_ind1 = tuple(map(add, it.multi_index, (0, -1)))
					neighbour_ind2 = tuple(map(add, it.multi_index, (1, -1)))
					if neighbour_ind1[1] < 0 or am.altitude[neighbour_ind1] == am.NODATA_value or am.altitude[neighbour_ind2] == am.NODATA_value:
						writeFacet(file, [vert0[0] * am.dx, vert0[1] * am.dx, it[0] - am.alt_min],\
							[vert1[0] * am.dx, vert1[1] * am.dx, am.altitude[vert1] - am.alt_min],\
							[vert1[0] * am.dx, vert1[1] * am.dx, am.altitude[vert1] + height_refinement - am.alt_min])
						writeFacet(file, [vert0[0] * am.dx, vert0[1] * am.dx, it[0] - am.alt_min],\
							[vert1[0] * am.dx, vert1[1] * am.dx, am.altitude[vert1] + height_refinement - am.alt_min],\
							[vert0[0] * am.dx, vert0[1] * am.dx, it[0] + height_refinement - am.alt_min])
					neighbour_ind1 = tuple(map(add, it.multi_index, (0, 2)))
					neighbour_ind2 = tuple(map(add, it.multi_index, (1, 2)))
					if neighbour_ind1[1] >= am.ny or am.altitude[neighbour_ind1] == am.NODATA_value or am.altitude[neighbour_ind2] == am.NODATA_value:
						writeFacet(file, [vert2[0] * am.dx, vert2[1] * am.dx, am.altitude[vert2] - am.alt_min],\
							[vert3[0] * am.dx, vert3[1] * am.dx, am.altitude[vert3] - am.alt_min],\
							[vert3[0] * am.dx, vert3[1] * am.dx, am.altitude[vert3] + height_refinement - am.alt_min])
						writeFacet(file, [vert2[0] * am.dx, vert2[1] * am.dx, am.altitude[vert2] - am.alt_min],\
							[vert3[0] * am.dx, vert3[1] * am.dx, am.altitude[vert3] + height_refinement - am.alt_min],\
							[vert2[0] * am.dx, vert2[1] * am.dx, am.altitude[vert2] + height_refinement - am.alt_min])
			it.iternext()
	file.write('endsolid sides_refine\n')
	file.write('solid atmosphere_refine\n')
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			vert0 = it.multi_index
			vert1 = tuple(map(add, it.multi_index, (1, 0)))
			vert2 = tuple(map(add, it.multi_index, (1, 1)))
			vert3 = tuple(map(add, it.multi_index, (0, 1)))
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				am.altitude[vert1] != am.NODATA_value and\
				am.altitude[vert2] != am.NODATA_value and\
				am.altitude[vert3] != am.NODATA_value:# and\
				#it.multi_index[1] - it.multi_index[0] * am.ny / am.nx - 0.3 * am.ny < 0 and\
				#it.multi_index[1] - it.multi_index[0] * am.ny / am.nx + 0.4 * am.ny > 0 and\
				#it.multi_index[1] + it.multi_index[0] * am.ny / am.nx - 1.5 * am.ny < 0: #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! last 3 lines only for 22 slope
					writeFacet(file, [vert0[0] * am.dx, vert0[1] * am.dx, it[0] + height_refinement - am.alt_min],\
						[vert2[0] * am.dx, vert2[1] * am.dx, am.altitude[vert2] + height_refinement - am.alt_min],\
						[vert3[0] * am.dx, vert3[1] * am.dx, am.altitude[vert3] + height_refinement - am.alt_min])
					writeFacet(file, [vert0[0] * am.dx, vert0[1] * am.dx, it[0] + height_refinement - am.alt_min],\
						[vert1[0] * am.dx, vert1[1] * am.dx, am.altitude[vert1] + height_refinement - am.alt_min],\
						[vert2[0] * am.dx, vert2[1] * am.dx, am.altitude[vert2] + height_refinement - am.alt_min])
			it.iternext()
	file.write('endsolid atmosphere_refine\n')
	file.close()
	print('Refine area STL is ready')

def createBMD_cube(am, height = 20, indent = 10.):
	print("Creating blockMeshDict file")
	size_x = am.nx * am.dx
	size_y = am.ny * am.dx
	size_z = am.alt_max - am.alt_min + height
	blockMeshDictFileName = "blockMeshDict"
	file_blockMeshDict = open(blockMeshDictFileName, "w")
	file_blockMeshDict.write("FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tobject\tblockMeshDict;\n}\n\nconvertToMeters 1.0;\n\n")
	file_blockMeshDict.write("vertices\n(\n")
	file_blockMeshDict.write("\t(%lf\t%lf\t%lf)\n" % (-indent, -indent, -indent))
	file_blockMeshDict.write("\t(%f\t%lf\t%lf)\n" % (size_x + indent, -indent, -indent))
	file_blockMeshDict.write("\t(%f\t%f\t%lf)\n" % (size_x + indent, size_y + indent, -indent))
	file_blockMeshDict.write("\t(%lf\t%f\t%lf)\n" % (-indent, size_y + indent, -indent))
	file_blockMeshDict.write("\t(%lf\t%lf\t%f)\n" % (-indent, -indent, size_z + indent))
	file_blockMeshDict.write("\t(%f\t%lf\t%f)\n" % (size_x + indent, -indent, size_z + indent))
	file_blockMeshDict.write("\t(%f\t%f\t%f)\n" % (size_x + indent, size_y + indent, size_z + indent))
	file_blockMeshDict.write("\t(%lf\t%f\t%f)\n" % (-indent, size_y + indent, size_z + indent))
	file_blockMeshDict.write(");\n\nblocks\n(\n")
	file_blockMeshDict.write("\thex (0\t1\t2\t3\t4\t5\t6\t7)\t(%d %d %d) simpleGrading (1 1 1)\n" % \
		(math.ceil((size_x + 2 * indent) / am.dx), math.ceil((size_y + 2 * indent) / am.dx), math.ceil((am.alt_max - am.alt_min + 2 * indent) / am.dx)))
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
	file.write('FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tlocation\t"system";\n\tobject\tsetFieldsDict;\n}')
	file.write('defaultFieldValues\n(\n\tvolScalarFieldValue alpha.water 0\n);\nregions\n(\n')
	with np.nditer(rg.region, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] == 0 and\
				am.altitude[it.multi_index] != am.NODATA_value:
				file.write('\tboxToCell\n\t{\n\t\tbox (%lf %lf %lf) (%lf %lf %lf);\n\t\tfieldValues\n\t\t(\n\t\t\tvolScalarFieldValue alpha.water 1\n\t\t);\n\t}' % (\
					it.multi_index[0] * am.dx, it.multi_index[1] * am.dx ,am.altitude[it.multi_index] - 1 - am.alt_min,\
					(it.multi_index[0] + 1) * am.dx, (it.multi_index[1] + 1) * am.dx, am.altitude[it.multi_index] - am.alt_min + height))
			it.iternext()
	file.write(');')
	file.close()
	print("setFieldsDict file is ready")

def writeReleaseArea(file, vert0, dx, i = 0, height = 0.5):
	vert1 = tuple(map(add, vert0, (1, 0)))
	vert2 = tuple(map(add, vert0, (1, 1)))
	vert3 = tuple(map(add, vert0, (0, 1)))
	file.write('\t\t\treleaseArea%d\n\t\t\t{\n\t\t\t\ttype polygon;\n\t\t\t\toffset (0 0 0);\n\t\t\t\tvertices\n\t\t\t\t(\n' % (i))
	file.write('\t\t\t\t\t( %lf %lf 0 )\n' % (vert0[0] * dx, vert0[1] * dx))
	file.write('\t\t\t\t\t( %lf %lf 0 )\n' % (vert1[0] * dx, vert1[1] * dx))
	file.write('\t\t\t\t\t( %lf %lf 0 )\n' % (vert2[0] * dx, vert2[1] * dx))
	file.write('\t\t\t\t\t( %lf %lf 0 )\n' % (vert3[0] * dx, vert3[1] * dx))
	file.write('\t\t\t\t);\n\t\t\t\tvalue %lf;\n\t\t\t}\n' % (height))

def createReleaseArea(am, rg, height = 0.5):
	print('Creating releaseArea file')
	file = open('releaseArea', 'w')
	file.write('FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tlocation\t\"system\";\n\tobject\treleaseArea;\n}\n')
	file.write('fields\n(\n\th\n\t{\n\t\tdefault 0;\n\t\tregions\n\t\t(\n')
	i = 0
	with np.nditer(rg.region, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] == 0 and am.altitude[it.multi_index] != am.NODATA_value:
				writeReleaseArea(file, it.multi_index, dx = am.dx, i = i, height = height)
				i += 1
			it.iternext()
	file.write('\t\t);\n\t}\n);')
	file.close()
	print('releaseArea file is ready')

def main(argv):
	map_name, region_map_name, cellsize = ra.readFileNames(argv)
	slope = ra.asc(map_name, region_map_name)
	#slope.am, slope.rg = ra.interpolateMap(slope.am, slope.rg, cellsize)
	createASCII_STL(slope.am, height_area = 20, height_refinement = 1)
	createBMD_cube(slope.am, height = 20, indent = 10)
	createSetFields(slope.am, slope.rg, height = 2)
	createReleaseArea(slope.am, slope.rg, height = 0.5)

if __name__== "__main__":
	main(sys.argv)