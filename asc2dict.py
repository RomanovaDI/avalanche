print("Write a file of ASCII map or type enter and file name will be \"relief_22.asc\"")
map_name = input()
if map_name == "":
	map_name = "relief_22.asc"
print("Opening file: \"" + map_name + "\"")
file_map = open(map_name, "r")

line = file_map.readline()
line_list = line.split()
if line_list[0] != 'ncols':
	print("No tag \"ncols\" in first line")
	exit()
ncols = int(line_list[1])

line = file_map.readline()
line_list = line.split()
if line_list[0] != 'nrows':
	print("No tag \"ncrows\" in second line")
	exit()
nrows = int(line_list[1])

line = file_map.readline()
line_list = line.split()
if line_list[0] != 'xllcorner':
	print("No tag \"xllcorner\" in third line")
	exit()
xllcorner = float(line_list[1].replace(",", "."))

line = file_map.readline()
line_list = line.split()
if line_list[0] != 'yllcorner':
	print("No tag \"yllcorner\" in fourth line")
	exit()
yllcorner = float(line_list[1].replace(",", "."))

line = file_map.readline()
line_list = line.split()
if line_list[0] != 'cellsize':
	print("No tag \"cellsize\" in fifth line")
	exit()
cellsize = float(line_list[1].replace(",", "."))

line = file_map.readline()
line_list = line.split()
if line_list[0] != 'NODATA_value':
	print("No tag \"NODATA_value\" in sixth line")
	exit()
NODATA_value = float(line_list[1].replace(",", "."))

print("Write new cell size if necessary:")
new_cellsize = input()
if new_cellsize == "":
	new_cellsize = cellsize
else:
	new_cellsize = float(new_cellsize)

import numpy as np
altitude = np.loadtxt(file_map, dtype=np.str)
file_map.close()
altitude = np.char.replace(altitude, ',', '.').astype(np.float64)
print(altitude)
print(altitude[100, 100])

altitude_mask = np.copy(altitude)
f = lambda a: 0 if a == NODATA_value else 1
fv = np.vectorize(f)
altitude_mask = fv(altitude_mask)
print(altitude_mask)
print(altitude_mask[100, 100])

from scipy import interpolate
x = np.arange(0, cellsize * ncols, cellsize)
y = np.arange(0, cellsize * nrows, cellsize)
xnew = np.arange(0, cellsize * ncols, new_cellsize)
ynew = np.arange(0, cellsize * nrows, new_cellsize)
f = interpolate.interp2d(x, y, altitude, kind='linear')
altitude_interpolation = f(xnew, ynew)
f = interpolate.interp2d(x, y, altitude_mask, kind='linear')
altitude_interpolation_mask = f(xnew, ynew)
f = lambda a: 0 if a < 1 else 1
fv = np.vectorize(f)
altitude_interpolation_mask = fv(altitude_interpolation_mask)
altitude_interpolation = altitude_interpolation * altitude_interpolation_mask
ny = xnew.shape[0]
nx = ynew.shape[0]
dx = new_cellsize
print(altitude_interpolation)
print(altitude_interpolation[500, 500])

import math
f = lambda a: math.floor(a / dx) * dx if a != 0 else NODATA_value
fv = np.vectorize(f)
altitude_interpolation = fv(altitude_interpolation)
print(altitude_interpolation)
print(altitude_interpolation[500, 500])

#maximum = np.amax(altitude_interpolation)
#with np.nditer(altitude_interpolation, op_flags=['readwrite']) as it:
#	for x in it:
#		if x == NODATA_value:
#			x[...] = maximum + 1000
#minimum = np.amin(altitude_interpolation)
#with np.nditer(altitude_interpolation, op_flags=['readwrite']) as it:
#	for x in it:
#		if x == maximum + 1000:
#			x[...] = NODATA_value
#nz = (maximum - minimum + 50) / dx
#blocks = np.zeros((nx, ny, nz))
#it = np.nditer(blocks, flags=['multi_index'], op_flags=['writeonly'])
#with it:
#	while not it.finished:
#		cell_alt = it.multi_index[2] * dx
#		curr_alt = altitude_interpolation[it.multi_index[0], it.multi_index[1]]
#		if cell_alt >= surr_alt and cell_alt < curr_alt + 50
#			it[0] = 1
#		it.iternext()
#vertices = np.zeros((nx + 1, ny + 1, nz + 1))
#it = np.nditer(vertices, flags=['multi_index'], op_flags=['writeonly'])
#with it:
#	while not it.finished:
#		ind = it.multi_index
#		if 0 <= ind[0] < nx and 0 <= ind[1] < ny and 0 <= ind[2] < nz:
#			if blocks[ind] == 1
#				it[0] = 1
#		ind = it.multi_index - (1, 0, 0)
#		if 0 <= ind[0] < nx and 0 <= ind[1] < ny and 0 <= ind[2] < nz:
#			if blocks[ind] == 1
#				it[0] = 1
#		ind = it.multi_index - (0, 1, 0)
#		if 0 <= ind[0] < nx and 0 <= ind[1] < ny and 0 <= ind[2] < nz:
#			if blocks[ind] == 1
#				it[0] = 1
#		ind = it.multi_index - (0, 0, 1)
#		if 0 <= ind[0] < nx and 0 <= ind[1] < ny and 0 <= ind[2] < nz:
#			if blocks[ind] == 1
#				it[0] = 1
#		ind = it.multi_index - (1, 1, 0)
#		if 0 <= ind[0] < nx and 0 <= ind[1] < ny and 0 <= ind[2] < nz:
#			if blocks[ind] == 1
#				it[0] = 1
#		ind = it.multi_index - (1, 0, 1)
#		if 0 <= ind[0] < nx and 0 <= ind[1] < ny and 0 <= ind[2] < nz:
#			if blocks[ind] == 1
#				it[0] = 1
#		ind = it.multi_index - (0, 1, 1)
#		if 0 <= ind[0] < nx and 0 <= ind[1] < ny and 0 <= ind[2] < nz:
#			if blocks[ind] == 1
#				it[0] = 1
#		ind = it.multi_index - (1, 1, 1)
#		if 0 <= ind[0] < nx and 0 <= ind[1] < ny and 0 <= ind[2] < nz:
#			if blocks[ind] == 1
#				it[0] = 1
#		it.iternext()

blockMeshDictFileName = "blockMeshDict"
file_blockMeshDict = open(blockMeshDictFileName, "w")
file_blockMeshDict.write("FoamFile\n")
file_blockMeshDict.write("{\n")
file_blockMeshDict.write("    version     2.0;\n")
file_blockMeshDict.write("    format      ascii;\n")
file_blockMeshDict.write("    class       dictionary;\n")
file_blockMeshDict.write("    object      blockMeshDict;\n")
file_blockMeshDict.write("}\n")
file_blockMeshDict.write("convertToMeters ")
file_blockMeshDict.write(str(dx))
file_blockMeshDict.write(";\n")
file_blockMeshDict.write("vertices\n")
file_blockMeshDict.write("(\n")
hight = 50
hight = math.floor(hight / dx) * dx
it = np.nditer(altitude_interpolation, flags=['multi_index'], op_flags=["readonly"])
while not it.finished:
	if it[0] != NODATA_value:
		file_blockMeshDict.write("\t(%f\t%f\t%f)\n" % (it.multi_index[0] * dx, it.multi_index[1] * dx, it[0]))
		file_blockMeshDict.write("\t(%f\t%f\t%f)\n" % (it.multi_index[0] * dx + dx, it.multi_index[1] * dx, it[0]))
		file_blockMeshDict.write("\t(%f\t%f\t%f)\n" % (it.multi_index[0] * dx + dx, it.multi_index[1] * dx + dx, it[0]))
		file_blockMeshDict.write("\t(%f\t%f\t%f)\n" % (it.multi_index[0] * dx, it.multi_index[1] * dx + dx, it[0]))
		file_blockMeshDict.write("\t(%f\t%f\t%f)\n" % (it.multi_index[0] * dx, it.multi_index[1] * dx, it[0] + hight))
		file_blockMeshDict.write("\t(%f\t%f\t%f)\n" % (it.multi_index[0] * dx + dx, it.multi_index[1] * dx, it[0] + hight))
		file_blockMeshDict.write("\t(%f\t%f\t%f)\n" % (it.multi_index[0] * dx + dx, it.multi_index[1] * dx + dx, it[0] + hight))
		file_blockMeshDict.write("\t(%f\t%f\t%f)\n" % (it.multi_index[0] * dx, it.multi_index[1] * dx + dx, it[0] + hight))
	it.iternext()
file_blockMeshDict.write(");\n")
file_blockMeshDict.write("blocks\n")
file_blockMeshDict.write("(\n")
altitude_interpolation_ind = np.copy(altitude_interpolation)
ind = 0
it = np.nditer(altitude_interpolation, flags=['multi_index'], op_flags=["readonly"])
while not it.finished:
	if it[0] != NODATA_value:
		file_blockMeshDict.write("\thex (%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d)\t(1 1 %d) simpleGrading (1 1 1)\n" % (8*ind, 8*ind+1, 8*ind+2, 8*ind+3, 8*ind+4, 8*ind+5, 8*ind+6, 8*ind+7, int(hight / dx)))
		altitude_interpolation_ind[it.multi_index] = ind
		ind += 1
	it.iternext()
file_blockMeshDict.write(");\n")
file_blockMeshDict.write("edges\n")
file_blockMeshDict.write("(\n")
file_blockMeshDict.write(");\n")
file_blockMeshDict.write("boundary\n")
file_blockMeshDict.write("(\n")
file_blockMeshDict.write("\tslope\n")
file_blockMeshDict.write("\t{\n")
file_blockMeshDict.write("\t\ttype wall;\n")
file_blockMeshDict.write("\t\tfaces\n")
file_blockMeshDict.write("\t\t(\n")
it = np.nditer(altitude_interpolation, flags=['multi_index'], op_flags=["readonly"])
from operator import add
while not it.finished:
	if it[0] != NODATA_value:
		if it.multi_index[0] - 1 >= 0:
			neighbour_ind = tuple(map(add, it.multi_index, (-1, 0)))
			if altitude_interpolation[neighbour_ind] != NODATA_value:
				if altitude_interpolation[neighbour_ind] > it[0]:
					file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (altitude_interpolation_ind[it.multi_index]+3, altitude_interpolation_ind[it.multi_index]+0, altitude_interpolation_ind[neighbour_ind]+1, altitude_interpolation_ind[neighbour_ind]+2))
				elif altitude_interpolation[neighbour_ind] < it[0]:
					file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (altitude_interpolation_ind[it.multi_index]+3, altitude_interpolation_ind[it.multi_index]+0, altitude_interpolation_ind[neighbour_ind]+1, altitude_interpolation_ind[neighbour_ind]+2))
		if it.multi_index[1] - 1 >= 0:
			neighbour_ind = tuple(map(add, it.multi_index, (0, -1)))
			if altitude_interpolation[neighbour_ind] != NODATA_value:
				if altitude_interpolation[neighbour_ind] > it[0]:
					file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (altitude_interpolation_ind[it.multi_index]+0, altitude_interpolation_ind[it.multi_index]+1, altitude_interpolation_ind[neighbour_ind]+2, altitude_interpolation_ind[neighbour_ind]+3))
				elif altitude_interpolation[neighbour_ind] < it[0]:
					file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (altitude_interpolation_ind[it.multi_index]+0, altitude_interpolation_ind[it.multi_index]+1, altitude_interpolation_ind[neighbour_ind]+2, altitude_interpolation_ind[neighbour_ind]+3))
	it.iternext()
file_blockMeshDict.write("\t\t);\n")
file_blockMeshDict.write("\t}\n")
file_blockMeshDict.write(");\n")
file_blockMeshDict.write("\tatmosphere\n")
file_blockMeshDict.write("\t{\n")
file_blockMeshDict.write("\t\ttype patch;\n")
file_blockMeshDict.write("\t\tfaces\n")
file_blockMeshDict.write("\t\t(\n")
it = np.nditer(altitude_interpolation, flags=['multi_index'], op_flags=["readonly"])
while not it.finished:
	if it[0] != NODATA_value:
		if it.multi_index[0] - 1 >= 0:
			neighbour_ind = tuple(map(add, it.multi_index, (-1, 0)))
			if altitude_interpolation[neighbour_ind] != NODATA_value:
				if altitude_interpolation[neighbour_ind] > it[0]:
					file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (altitude_interpolation_ind[it.multi_index]+4, altitude_interpolation_ind[it.multi_index]+7, altitude_interpolation_ind[neighbour_ind]+6, altitude_interpolation_ind[neighbour_ind]+5))
				elif altitude_interpolation[neighbour_ind] < it[0]:
					file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (altitude_interpolation_ind[it.multi_index]+4, altitude_interpolation_ind[it.multi_index]+7, altitude_interpolation_ind[neighbour_ind]+6, altitude_interpolation_ind[neighbour_ind]+5))
			else:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (altitude_interpolation_ind[it.multi_index]+0, altitude_interpolation_ind[it.multi_index]+4, altitude_interpolation_ind[it.multi_index]+7, altitude_interpolation_ind[it.multi_index]+3))
		if it.multi_index[0] + 1 < nx:
			neighbour_ind = tuple(map(add, it.multi_index, (1, 0)))
			if altitude_interpolation[neighbour_ind] == NODATA_value:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (altitude_interpolation_ind[it.multi_index]+1, altitude_interpolation_ind[it.multi_index]+2, altitude_interpolation_ind[it.multi_index]+6, altitude_interpolation_ind[it.multi_index]+5))
		if it.multi_index[1] - 1 >= 0:
			neighbour_ind = tuple(map(add, it.multi_index, (0, -1)))
			if altitude_interpolation[neighbour_ind] != NODATA_value:
				if altitude_interpolation[neighbour_ind] > it[0]:
					file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (altitude_interpolation_ind[it.multi_index]+5, altitude_interpolation_ind[it.multi_index]+4, altitude_interpolation_ind[neighbour_ind]+7, altitude_interpolation_ind[neighbour_ind]+6))
				elif altitude_interpolation[neighbour_ind] < it[0]:
					file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (altitude_interpolation_ind[it.multi_index]+5, altitude_interpolation_ind[it.multi_index]+4, altitude_interpolation_ind[neighbour_ind]+7, altitude_interpolation_ind[neighbour_ind]+6))
		if it.multi_index[1] + 1 < ny:
			neighbour_ind = tuple(map(add, it.multi_index, (0, 1)))
			if altitude_interpolation[neighbour_ind] == NODATA_value:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (altitude_interpolation_ind[it.multi_index]+2, altitude_interpolation_ind[it.multi_index]+3, altitude_interpolation_ind[it.multi_index]+7, altitude_interpolation_ind[it.multi_index]+6))
	it.iternext()
file_blockMeshDict.write("\t\t);\n")
file_blockMeshDict.write("\t}\n")
file_blockMeshDict.write("")
file_blockMeshDict.write("")
file_blockMeshDict.write("")
file_blockMeshDict.write("")
file_blockMeshDict.write("")
file_blockMeshDict.write("")
file_blockMeshDict.close()


#from mpl_toolkits.mplot3d import Axes3D
#import matplotlib.pyplot as plt
#fig = plt.figure()
#ax = fig.gca(projection='3d')
#xnew, ynew = np.meshgrid(xnew, ynew)
#dots = ax.scatter(xnew, ynew, altitude_interpolation)
##surf = ax.plot_surface(xnew, ynew, altitude_interpolation)
#plt.show()

