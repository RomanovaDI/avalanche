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
	print("No tag \"nrows\" in second line")
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

print("Write a file of ASCII region map or type enter and file name will be \"region_22.asc\"")
region_map_name = input()
if region_map_name == "":
	region_map_name = "region_22.asc"
print("Opening file: \"" + region_map_name + "\"")
region_file_map = open(region_map_name, "r")

line = region_file_map.readline()
line_list = line.split()
if line_list[0] != 'ncols':
	print("No tag \"ncols\" in first line")
	exit()
region_ncols = int(line_list[1])

line = region_file_map.readline()
line_list = line.split()
if line_list[0] != 'nrows':
	print("No tag \"nrows\" in second line")
	exit()
region_nrows = int(line_list[1])

line = region_file_map.readline()
line_list = line.split()
if line_list[0] != 'xllcorner':
	print("No tag \"xllcorner\" in third line")
	exit()
region_xllcorner = float(line_list[1].replace(",", "."))

line = region_file_map.readline()
line_list = line.split()
if line_list[0] != 'yllcorner':
	print("No tag \"yllcorner\" in fourth line")
	exit()
region_yllcorner = float(line_list[1].replace(",", "."))

line = region_file_map.readline()
line_list = line.split()
if line_list[0] != 'cellsize':
	print("No tag \"cellsize\" in fifth line")
	exit()
region_cellsize = float(line_list[1].replace(",", "."))

line = region_file_map.readline()
line_list = line.split()
if line_list[0] != 'NODATA_value':
	print("No tag \"NODATA_value\" in sixth line")
	exit()
region_NODATA_value = float(line_list[1].replace(",", "."))

import numpy as np
altitude = np.loadtxt(file_map, dtype=np.str)
file_map.close()
altitude = np.char.replace(altitude, ',', '.').astype(np.float32)

region = np.loadtxt(region_file_map, dtype=np.str)
region_file_map.close()
region = np.char.replace(region, ',', '.').astype(np.float32)

if not xllcorner < region_xllcorner < xllcorner + ncols * cellsize:
	print("Error pair of map and region map")
	exit()
if not yllcorner < region_yllcorner < yllcorner + nrows * cellsize:
	print("Error pair of map and region map")
	exit()

print("Creating blockMaeshDict file")

altitude_mask = np.copy(altitude)
f = lambda a: 0 if a == NODATA_value else 1
fv = np.vectorize(f)
altitude_mask = fv(altitude_mask)

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
del altitude
del altitude_mask

import math
f = lambda a: math.floor(a / dx) * dx if a != 0 else NODATA_value
fv = np.vectorize(f)
altitude_interpolation = fv(altitude_interpolation)
del altitude_interpolation_mask

alt_max = np.amax(altitude_interpolation)
alt_min = np.amin(altitude_interpolation[altitude_interpolation != NODATA_value])
hight = 10.0
hight = math.floor(hight / dx) * dx
nz = int((alt_max - alt_min + hight) / dx)
vertices = np.full((nx + 1, ny + 1, nz + 1), -1, dtype=np.int32)
blocks = np.zeros((nx, ny, nz), dtype=np.int32)
with np.nditer(altitude_interpolation, flags=['multi_index'], op_flags=['readonly']) as it:
	while not it.finished:
		if it[0] != NODATA_value:
			for z in range(int((it[0] - alt_min) / dx), int((it[0] - alt_min + hight) / dx) + 1):
				vertices[it.multi_index[0], it.multi_index[1], z] = 1
				vertices[it.multi_index[0] + 1, it.multi_index[1], z] = 1
				vertices[it.multi_index[0], it.multi_index[1] + 1, z] = 1
				vertices[it.multi_index[0] + 1, it.multi_index[1] + 1, z] = 1
			for z in range(int((it[0] - alt_min) / dx), int((it[0] - alt_min + hight) / dx)):
				blocks[it.multi_index[0], it.multi_index[1], z] = 1
			blocks[it.multi_index[0], it.multi_index[1], int((it[0] - alt_min) / dx)] = 2
		it.iternext()
ind = 0;
for it in np.nditer(vertices, op_flags=['readwrite']):
	if it == 1:
		it[...] = ind
		ind += 1

blockMeshDictFileName = "blockMeshDict"
file_blockMeshDict = open(blockMeshDictFileName, "w")
file_blockMeshDict.write("FoamFile\n")
file_blockMeshDict.write("{\n")
file_blockMeshDict.write("    version     2.0;\n")
file_blockMeshDict.write("    format      ascii;\n")
file_blockMeshDict.write("    class       dictionary;\n")
file_blockMeshDict.write("    object      blockMeshDict;\n")
file_blockMeshDict.write("}\n\n")
file_blockMeshDict.write("convertToMeters 1.0;\n\n")
file_blockMeshDict.write("vertices\n")
file_blockMeshDict.write("(\n")
with np.nditer(vertices, flags=['multi_index'], op_flags=["readonly"]) as it:
	while not it.finished:
		if it[0] != -1:
			file_blockMeshDict.write("\t(%f\t%f\t%f)\n" % (it.multi_index[0] * dx, it.multi_index[1] * dx, it.multi_index[2] * dx + alt_min))
		it.iternext()
file_blockMeshDict.write(");\n\n")
file_blockMeshDict.write("blocks\n")
file_blockMeshDict.write("(\n")
from operator import add
with np.nditer(blocks, flags=['multi_index'], op_flags=["readonly"]) as it:
	while not it.finished:
		if it[0]:
			vert0 = it.multi_index
			vert1 = tuple(map(add, it.multi_index, (1, 0, 0)))
			vert2 = tuple(map(add, it.multi_index, (1, 1, 0)))
			vert3 = tuple(map(add, it.multi_index, (0, 1, 0)))
			vert4 = tuple(map(add, it.multi_index, (0, 0, 1)))
			vert5 = tuple(map(add, it.multi_index, (1, 0, 1)))
			vert6 = tuple(map(add, it.multi_index, (1, 1, 1)))
			vert7 = tuple(map(add, it.multi_index, (0, 1, 1)))
			file_blockMeshDict.write("\thex (%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d)\t(1 1 1) simpleGrading (1 1 1)\n" % \
				(vertices[vert0], vertices[vert1], vertices[vert2], vertices[vert3], vertices[vert4], vertices[vert5], vertices[vert6], vertices[vert7]))
		it.iternext()
file_blockMeshDict.write(");\n\n")
file_blockMeshDict.write("edges\n")
file_blockMeshDict.write("(\n")
file_blockMeshDict.write(");\n\n")
file_blockMeshDict.write("boundary\n")
file_blockMeshDict.write("(\n")
file_blockMeshDict.write("\tslope\n")
file_blockMeshDict.write("\t{\n")
file_blockMeshDict.write("\t\ttype wall;\n")
file_blockMeshDict.write("\t\tfaces\n")
file_blockMeshDict.write("\t\t(\n")

with np.nditer(blocks, flags=['multi_index'], op_flags=["readonly"]) as it:
	while not it.finished:
		if it[0] == 2:
			vert0 = it.multi_index
			vert1 = tuple(map(add, it.multi_index, (1, 0, 0)))
			vert2 = tuple(map(add, it.multi_index, (1, 1, 0)))
			vert3 = tuple(map(add, it.multi_index, (0, 1, 0)))
			vert4 = tuple(map(add, it.multi_index, (0, 0, 1)))
			vert5 = tuple(map(add, it.multi_index, (1, 0, 1)))
			vert6 = tuple(map(add, it.multi_index, (1, 1, 1)))
			vert7 = tuple(map(add, it.multi_index, (0, 1, 1)))
			file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vertices[vert3], vertices[vert2], vertices[vert1], vertices[vert0]))
			neighbour_ind = tuple(map(add, it.multi_index, (-1, 0, 0)))
			if neighbour_ind[0] < 0 or blocks[neighbour_ind] == 0:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vertices[vert0], vertices[vert4], vertices[vert7], vertices[vert3]))
			neighbour_ind = tuple(map(add, it.multi_index, (1, 0, 0)))
			if neighbour_ind[0] >= nx or blocks[neighbour_ind] == 0:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vertices[vert1], vertices[vert2], vertices[vert6], vertices[vert5]))
			neighbour_ind = tuple(map(add, it.multi_index, (0, -1, 0)))
			if neighbour_ind[1] < 0 or blocks[neighbour_ind] == 0:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vertices[vert0], vertices[vert1], vertices[vert5], vertices[vert4]))
			neighbour_ind = tuple(map(add, it.multi_index, (0, 1, 0)))
			if neighbour_ind[1] >= ny or blocks[neighbour_ind] == 0:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vertices[vert2], vertices[vert3], vertices[vert7], vertices[vert6]))
			neighbour_ind = tuple(map(add, it.multi_index, (0, 0, 1)))
			if neighbour_ind[2] >= nz or blocks[neighbour_ind] == 0:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vertices[vert4], vertices[vert5], vertices[vert6], vertices[vert7]))
		it.iternext()
file_blockMeshDict.write("\t\t);\n")
file_blockMeshDict.write("\t}\n")
file_blockMeshDict.write("\tatmosphere\n")
file_blockMeshDict.write("\t{\n")
file_blockMeshDict.write("\t\ttype patch;\n")
file_blockMeshDict.write("\t\tfaces\n")
file_blockMeshDict.write("\t\t(\n")
with np.nditer(blocks, flags=['multi_index'], op_flags=["readonly"]) as it:
	while not it.finished:
		if it[0] == 1:
			vert0 = it.multi_index
			vert1 = tuple(map(add, it.multi_index, (1, 0, 0)))
			vert2 = tuple(map(add, it.multi_index, (1, 1, 0)))
			vert3 = tuple(map(add, it.multi_index, (0, 1, 0)))
			vert4 = tuple(map(add, it.multi_index, (0, 0, 1)))
			vert5 = tuple(map(add, it.multi_index, (1, 0, 1)))
			vert6 = tuple(map(add, it.multi_index, (1, 1, 1)))
			vert7 = tuple(map(add, it.multi_index, (0, 1, 1)))
			neighbour_ind = tuple(map(add, it.multi_index, (-1, 0, 0)))
			if neighbour_ind[0] < 0 or blocks[neighbour_ind] == 0:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vertices[vert0], vertices[vert4], vertices[vert7], vertices[vert3]))
			neighbour_ind = tuple(map(add, it.multi_index, (1, 0, 0)))
			if neighbour_ind[0] >= nx or blocks[neighbour_ind] == 0:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vertices[vert1], vertices[vert2], vertices[vert6], vertices[vert5]))
			neighbour_ind = tuple(map(add, it.multi_index, (0, -1, 0)))
			if neighbour_ind[1] < 0 or blocks[neighbour_ind] == 0:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vertices[vert0], vertices[vert1], vertices[vert5], vertices[vert4]))
			neighbour_ind = tuple(map(add, it.multi_index, (0, 1, 0)))
			if neighbour_ind[1] >= ny or blocks[neighbour_ind] == 0:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vertices[vert2], vertices[vert3], vertices[vert7], vertices[vert6]))
			neighbour_ind = tuple(map(add, it.multi_index, (0, 0, 1)))
			if neighbour_ind[2] >= nz or blocks[neighbour_ind] == 0:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vertices[vert4], vertices[vert5], vertices[vert6], vertices[vert7]))
		it.iternext()
file_blockMeshDict.write("\t\t);\n")
file_blockMeshDict.write("\t}\n")
file_blockMeshDict.write(");\n\n")
file_blockMeshDict.write("mergePatchPairs\n")
file_blockMeshDict.write("(\n")
file_blockMeshDict.write(");\n")
file_blockMeshDict.write("")
file_blockMeshDict.write("")
file_blockMeshDict.write("")
file_blockMeshDict.write("")
file_blockMeshDict.write("")
file_blockMeshDict.close()
print("blockMeshDict file is ready")
del vertices
del blocks

print("Creating setFieldsDict file")
hight_of_snow = 8.0
x_offset = int((region_xllcorner - xllcorner) / dx)
y_offset = int((region_yllcorner - yllcorner) / dx)
f = lambda a: 0 if a == region_NODATA_value else (1 if a == 1 else -1)
fv = np.vectorize(f)
region = fv(region)
x = np.arange(0, region_cellsize * region_ncols, region_cellsize)
y = np.arange(0, region_cellsize * region_nrows, region_cellsize)
xnew = np.arange(0, region_cellsize * region_ncols, new_cellsize)
ynew = np.arange(0, region_cellsize * region_nrows, new_cellsize)
f = interpolate.interp2d(x, y, region, kind='linear')
region_interpolation = f(xnew, ynew)
del region
f = lambda a: 0 if (-1 < a < 1) else (1 if a >= 1 else -1)
fv = np.vectorize(f)
region_interpolation = fv(region_interpolation)
blocks = np.zeros((nx, ny, nz), dtype=np.float16)
with np.nditer(altitude_interpolation, flags=['multi_index'], op_flags=['readonly']) as it:
	while not it.finished:
		if it[0] != NODATA_value\
			and 0 <= it.multi_index[0] - x_offset < region_interpolation.shape[0]\
			and 0 <= it.multi_index[1] - y_offset < region_interpolation.shape[1]\
			and region_interpolation[it.multi_index[0] - x_offset, it.multi_index[1] - y_offset] != 0:
				if region_interpolation[it.multi_index[0] - x_offset, it.multi_index[1] - y_offset] == -1:
					z_slope = int((it[0] - alt_min) / dx)
					for z in range(int((it[0] - alt_min) / dx), int(math.ceil((it[0] - alt_min + hight_of_snow) / dx))):
						blocks[it.multi_index[0], it.multi_index[1], z] = 1.0 if (z - z_slope + 1) * dx <= hight_of_snow else ((z - z_slope + 1) * dx - hight_of_snow) / dx
				else:
					for z in range(int((it[0] - alt_min) / dx), int((it[0] - alt_min + hight) / dx)):
						blocks[it.multi_index[0], it.multi_index[1], z] = -1.0
		it.iternext()

setFieldsDictFileName = "setFieldsDict"
file_setFieldsDict = open(setFieldsDictFileName, "w")
file_setFieldsDict.write("FoamFile\n")
file_setFieldsDict.write("{\n")
file_setFieldsDict.write("    version     2.0;\n")
file_setFieldsDict.write("    format      ascii;\n")
file_setFieldsDict.write("    class       dictionary;\n")
file_setFieldsDict.write("    location    \"system\";\n")
file_setFieldsDict.write("    object      setFieldsDict;\n")
file_setFieldsDict.write("}\n\n")
file_setFieldsDict.write("defaultFieldValues\n")
file_setFieldsDict.write("(\n")
file_setFieldsDict.write("\tvolScalarFieldValue alpha.water 0\n")
file_setFieldsDict.write("\tvolScalarFieldValue deposit_area 0\n")
file_setFieldsDict.write(");\n\n")
file_setFieldsDict.write("regions\n")
file_setFieldsDict.write("(\n")
with np.nditer(blocks, flags=['multi_index'], op_flags=["readonly"]) as it:
	while not it.finished:
		if it[0] != 0:
			file_setFieldsDict.write("\tboxToCell\n")
			file_setFieldsDict.write("\t{\n")
			file_setFieldsDict.write("\t\tbox (%f\t%f\t%f) (%f\t%f\t%f);\n" %\
				(it.multi_index[0] * dx, it.multi_index[1] * dx, it.multi_index[2] * dx + alt_min,\
				it.multi_index[0] * dx + dx, it.multi_index[1] * dx + dx, it.multi_index[2] * dx + dx + alt_min))
			file_setFieldsDict.write("\t\tfieldValues\n")
			file_setFieldsDict.write("\t\t(\n")
			if it[0] > 0:
				file_setFieldsDict.write("\t\t\tvolScalarFieldValue alpha.water %f\n" % it[0])
			else:
				file_setFieldsDict.write("\t\t\tvolScalarFieldValue deposit_area 1\n")
			file_setFieldsDict.write("\t\t);\n")
			file_setFieldsDict.write("\t}\n")
		it.iternext()
file_setFieldsDict.write(");\n")

file_setFieldsDict.close()

print("setFieldsDict file is ready")

del region_interpolation
del altitude_interpolation
del blocks

#from mpl_toolkits.mplot3d import Axes3D
#import matplotlib.pyplot as plt
#fig = plt.figure()
#ax = fig.gca(projection='3d')
#xnew, ynew = np.meshgrid(xnew, ynew)
##dots = ax.scatter(xnew, ynew, altitude_interpolation, s=0.5)
#dots = ax.scatter(xnew, ynew, blocks[:, :, 50], s=0.5)
##surf = ax.plot_surface(xnew, ynew, altitude_interpolation)
#plt.show()

