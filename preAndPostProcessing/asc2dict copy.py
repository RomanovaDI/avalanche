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

if not xllcorner <= region_xllcorner <= xllcorner + ncols * cellsize:
	print("Error pair of map and region map")
	exit()
if not yllcorner <= region_yllcorner <= yllcorner + nrows * cellsize:
	print("Error pair of map and region map")
	exit()

print("Creating blockMeshDict file")

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
del altitude_interpolation_mask

import math
f = lambda a: math.floor(a / dx) * dx if a != 0 else NODATA_value
fv = np.vectorize(f)
altitude_interpolation = fv(altitude_interpolation)

alt_max = np.amax(altitude_interpolation)
alt_min = np.amin(altitude_interpolation[altitude_interpolation != NODATA_value])
hight = 4.0
hight = math.floor(hight / dx) * dx
nz = int((alt_max - alt_min + hight) / dx)
vertices = np.full((nx + 1, ny + 1, nz + 1), -1, dtype=np.int32)
blocks = np.zeros((nx, ny, nz), dtype=np.float32)
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
blocks_ind = np.copy(blocks)
ind = 0;
for it in np.nditer(blocks_ind, op_flags=['readwrite']):
	if it != 0:
		it[...] = ind
		ind += 1
n_blocks = ind

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
n_vertices = 0
with np.nditer(vertices, flags=['multi_index'], op_flags=["readonly"]) as it:
	while not it.finished:
		if it[0] != -1:
			file_blockMeshDict.write("\t(%f\t%f\t%f)\n" % (it.multi_index[0] * dx, it.multi_index[1] * dx, it.multi_index[2] * dx + alt_min))
			n_vertices += 1
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

n_slope_faces = 0
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
			n_slope_faces += 1
			neighbour_ind = tuple(map(add, it.multi_index, (-1, 0, 0)))
			if neighbour_ind[0] < 0 or blocks[neighbour_ind] == 0:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vertices[vert0], vertices[vert4], vertices[vert7], vertices[vert3]))
				n_slope_faces += 1
			neighbour_ind = tuple(map(add, it.multi_index, (1, 0, 0)))
			if neighbour_ind[0] >= nx or blocks[neighbour_ind] == 0:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vertices[vert1], vertices[vert2], vertices[vert6], vertices[vert5]))
				n_slope_faces += 1
			neighbour_ind = tuple(map(add, it.multi_index, (0, -1, 0)))
			if neighbour_ind[1] < 0 or blocks[neighbour_ind] == 0:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vertices[vert0], vertices[vert1], vertices[vert5], vertices[vert4]))
				n_slope_faces += 1
			neighbour_ind = tuple(map(add, it.multi_index, (0, 1, 0)))
			if neighbour_ind[1] >= ny or blocks[neighbour_ind] == 0:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vertices[vert2], vertices[vert3], vertices[vert7], vertices[vert6]))
				n_slope_faces += 1
			neighbour_ind = tuple(map(add, it.multi_index, (0, 0, 1)))
			if neighbour_ind[2] >= nz or blocks[neighbour_ind] == 0:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vertices[vert4], vertices[vert5], vertices[vert6], vertices[vert7]))
				n_slope_faces += 1
		it.iternext()
file_blockMeshDict.write("\t\t);\n")
file_blockMeshDict.write("\t}\n")
file_blockMeshDict.write("\tatmosphere\n")
file_blockMeshDict.write("\t{\n")
file_blockMeshDict.write("\t\ttype patch;\n")
file_blockMeshDict.write("\t\tfaces\n")
file_blockMeshDict.write("\t\t(\n")

n_atmosphere_faces = 0
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
				n_atmosphere_faces += 1
			neighbour_ind = tuple(map(add, it.multi_index, (1, 0, 0)))
			if neighbour_ind[0] >= nx or blocks[neighbour_ind] == 0:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vertices[vert1], vertices[vert2], vertices[vert6], vertices[vert5]))
				n_atmosphere_faces += 1
			neighbour_ind = tuple(map(add, it.multi_index, (0, -1, 0)))
			if neighbour_ind[1] < 0 or blocks[neighbour_ind] == 0:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vertices[vert0], vertices[vert1], vertices[vert5], vertices[vert4]))
				n_atmosphere_faces += 1
			neighbour_ind = tuple(map(add, it.multi_index, (0, 1, 0)))
			if neighbour_ind[1] >= ny or blocks[neighbour_ind] == 0:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vertices[vert2], vertices[vert3], vertices[vert7], vertices[vert6]))
				n_atmosphere_faces += 1
			neighbour_ind = tuple(map(add, it.multi_index, (0, 0, 1)))
			if neighbour_ind[2] >= nz or blocks[neighbour_ind] == 0:
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (vertices[vert4], vertices[vert5], vertices[vert6], vertices[vert7]))
				n_atmosphere_faces += 1
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

boundaryFileName = "boundary"
file_boundary = open(boundaryFileName, "w")
facesFileName = "faces"
file_faces = open(facesFileName, "w")
facesIntFileName = "faces_int"
file_faces_int = open(facesIntFileName, "w")
facesSlFileName = "faces_slope"
file_faces_sl = open(facesSlFileName, "w")
facesAtmFileName = "faces_atmosphere"
file_faces_atm = open(facesAtmFileName, "w")
neighbourFileName = "neighbour"
file_neighbour = open(neighbourFileName, "w")
ownerFileName = "owner"
file_owner = open(ownerFileName, "w")
pointsFileName = "points"
file_points = open(pointsFileName, "w")
cellToRegionFileName = "cellToRegion"
file_cellToRegion = open(cellToRegionFileName, "w")

file_cellToRegion.write("FoamFile\n")
file_cellToRegion.write("{\n")
file_cellToRegion.write("    version     2.0;\n")
file_cellToRegion.write("    format      ascii;\n")
file_cellToRegion.write("    class       labelList;\n")
file_cellToRegion.write("    location    \"0\";\n")
file_cellToRegion.write("    object      cellToRegion;\n")
file_cellToRegion.write("}\n")
file_cellToRegion.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n")
file_cellToRegion.write("\n")

file_faces.write("FoamFile\n")
file_faces.write("{\n")
file_faces.write("    version     2.0;\n")
file_faces.write("    format      ascii;\n")
file_faces.write("    class       faceList;\n")
file_faces.write("    location    \"constant/polyMesh\";\n")
file_faces.write("    object      faces;\n")
file_faces.write("}\n")
file_faces.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n")
file_faces.write("\n")

file_points.write("FoamFile\n")
file_points.write("{\n")
file_points.write("    version     2.0;\n")
file_points.write("    format      ascii;\n")
file_points.write("    class       vectorField;\n")
file_points.write("    location    \"constant/polyMesh\";\n")
file_points.write("    object      points;\n")
file_points.write("}\n")
file_points.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n")
file_points.write("\n")
file_points.write("%d"%n_vertices)

file_points.write("(\n")
with np.nditer(vertices, flags=['multi_index'], op_flags=["readonly"]) as it:
	while not it.finished:
		if it[0] != -1:
			file_points.write("(%.0f\t%.0f\t%.0f)\n" % (it.multi_index[0] * dx, it.multi_index[1] * dx, it.multi_index[2] * dx + alt_min))
		it.iternext()
file_points.write(")\n")

n_int = 0
n_atm = 0
n_slp = 0
owner_int = []
owner_slp = []
owner_atm = []
neighbour = []
with np.nditer(blocks, flags=['multi_index'], op_flags=["readonly"]) as it:
	while not it.finished:
		if it[0] != 0:
			vert0 = it.multi_index
			vert1 = tuple(map(add, it.multi_index, (1, 0, 0)))
			vert2 = tuple(map(add, it.multi_index, (1, 1, 0)))
			vert3 = tuple(map(add, it.multi_index, (0, 1, 0)))
			vert4 = tuple(map(add, it.multi_index, (0, 0, 1)))
			vert5 = tuple(map(add, it.multi_index, (1, 0, 1)))
			vert6 = tuple(map(add, it.multi_index, (1, 1, 1)))
			vert7 = tuple(map(add, it.multi_index, (0, 1, 1)))
			neighbour_ind = tuple(map(add, it.multi_index, (0, 0, -1)))
			if neighbour_ind[2] < 0 or blocks[neighbour_ind] == 0:
				if it[0] == 1:
					file_faces_atm.write("4(%d %d %d %d)\n" % (vertices[vert3], vertices[vert2], vertices[vert1], vertices[vert0]))
					n_atm += 1
					owner_atm.append(blocks_ind[it.multi_index])
				if it[0] == 2:
					file_faces_sl.write("4(%d %d %d %d)\n" % (vertices[vert3], vertices[vert2], vertices[vert1], vertices[vert0]))
					n_slp += 1
					owner_slp.append(blocks_ind[it.multi_index])
			elif blocks_ind[it.multi_index] < blocks_ind[neighbour_ind]:
				file_faces_int.write("4(%d %d %d %d)\n" % (vertices[vert3], vertices[vert2], vertices[vert1], vertices[vert0]))
				n_int += 1
				owner_int.append(blocks_ind[it.multi_index])
				neighbour.append(blocks_ind[neighbour_ind])
			neighbour_ind = tuple(map(add, it.multi_index, (-1, 0, 0)))
			if neighbour_ind[0] < 0 or blocks[neighbour_ind] == 0:
				if it[0] == 1:
					file_faces_atm.write("4(%d %d %d %d)\n" % (vertices[vert0], vertices[vert4], vertices[vert7], vertices[vert3]))
					n_atm += 1
					owner_atm.append(blocks_ind[it.multi_index])
				if it[0] == 2:
					file_faces_sl.write("4(%d %d %d %d)\n" % (vertices[vert0], vertices[vert4], vertices[vert7], vertices[vert3]))
					n_slp += 1
					owner_slp.append(blocks_ind[it.multi_index])
			elif blocks_ind[it.multi_index] < blocks_ind[neighbour_ind]:
				file_faces_int.write("4(%d %d %d %d)\n" % (vertices[vert0], vertices[vert4], vertices[vert7], vertices[vert3]))
				n_int += 1
				owner_int.append(blocks_ind[it.multi_index])
				neighbour.append(blocks_ind[neighbour_ind])
			neighbour_ind = tuple(map(add, it.multi_index, (0, -1, 0)))
			if neighbour_ind[1] < 0 or blocks[neighbour_ind] == 0:
				if it[0] == 1:
					file_faces_atm.write("4(%d %d %d %d)\n" % (vertices[vert0], vertices[vert1], vertices[vert5], vertices[vert4]))
					n_atm += 1
					owner_atm.append(blocks_ind[it.multi_index])
				if it[0] == 2:
					file_faces_sl.write("4(%d %d %d %d)\n" % (vertices[vert0], vertices[vert1], vertices[vert5], vertices[vert4]))
					n_slp += 1
					owner_slp.append(blocks_ind[it.multi_index])
			elif blocks_ind[it.multi_index] < blocks_ind[neighbour_ind]:
				file_faces_int.write("4(%d %d %d %d)\n" % (vertices[vert0], vertices[vert1], vertices[vert5], vertices[vert4]))
				n_int += 1
				owner_int.append(blocks_ind[it.multi_index])
				neighbour.append(blocks_ind[neighbour_ind])
			neighbour_ind = tuple(map(add, it.multi_index, (0, 1, 0)))
			if neighbour_ind[1] >= ny or blocks[neighbour_ind] == 0:
				if it[0] == 1:
					file_faces_atm.write("4(%d %d %d %d)\n" % (vertices[vert2], vertices[vert3], vertices[vert7], vertices[vert6]))
					n_atm += 1
					owner_atm.append(blocks_ind[it.multi_index])
				if it[0] == 2:
					file_faces_sl.write("4(%d %d %d %d)\n" % (vertices[vert2], vertices[vert3], vertices[vert7], vertices[vert6]))
					n_slp += 1
					owner_slp.append(blocks_ind[it.multi_index])
			elif blocks_ind[it.multi_index] < blocks_ind[neighbour_ind]:
				file_faces_int.write("4(%d %d %d %d)\n" % (vertices[vert2], vertices[vert3], vertices[vert7], vertices[vert6]))
				n_int += 1
				owner_int.append(blocks_ind[it.multi_index])
				neighbour.append(blocks_ind[neighbour_ind])
			neighbour_ind = tuple(map(add, it.multi_index, (1, 0, 0)))
			if neighbour_ind[0] >= nx or blocks[neighbour_ind] == 0:
				if it[0] == 1:
					file_faces_atm.write("4(%d %d %d %d)\n" % (vertices[vert1], vertices[vert2], vertices[vert6], vertices[vert5]))
					n_atm += 1
					owner_atm.append(blocks_ind[it.multi_index])
				if it[0] == 2:
					file_faces_sl.write("4(%d %d %d %d)\n" % (vertices[vert1], vertices[vert2], vertices[vert6], vertices[vert5]))
					n_slp += 1
					owner_slp.append(blocks_ind[it.multi_index])
			elif blocks_ind[it.multi_index] < blocks_ind[neighbour_ind]:
				file_faces_int.write("4(%d %d %d %d)\n" % (vertices[vert1], vertices[vert2], vertices[vert6], vertices[vert5]))
				n_int += 1
				owner_int.append(blocks_ind[it.multi_index])
				neighbour.append(blocks_ind[neighbour_ind])
			neighbour_ind = tuple(map(add, it.multi_index, (0, 0, 1)))
			if neighbour_ind[2] >= nz or blocks[neighbour_ind] == 0:
				if it[0] == 1:
					file_faces_atm.write("4(%d %d %d %d)\n" % (vertices[vert4], vertices[vert5], vertices[vert6], vertices[vert7]))
					n_atm += 1
					owner_atm.append(blocks_ind[it.multi_index])
				if it[0] == 2:
					file_faces_sl.write("4(%d %d %d %d)\n" % (vertices[vert4], vertices[vert5], vertices[vert6], vertices[vert7]))
					n_slp += 1
					owner_slp.append(blocks_ind[it.multi_index])
			elif blocks_ind[it.multi_index] < blocks_ind[neighbour_ind]:
				file_faces_int.write("4(%d %d %d %d)\n" % (vertices[vert4], vertices[vert5], vertices[vert6], vertices[vert7]))
				n_int += 1
				owner_int.append(blocks_ind[it.multi_index])
				neighbour.append(blocks_ind[neighbour_ind])
		it.iternext()

if n_atm != n_atmosphere_faces:
	print("n_atm != n_atmosphere_faces\n")
if n_slp != n_slope_faces:
	print("n_slp != n_slope_faces\n")
n_faces = n_int + n_slp + n_atm
file_faces.write("%d\n" % n_faces)
file_faces.write("(\n")

file_faces_int.close()
file_faces_sl.close()
file_faces_atm.close()
#file_faces_int = open(facesIntFileName, "r")
#file_faces_sl = open(facesSlFileName, "r")
#file_faces_atm = open(facesAtmFileName, "r")
filenames = [facesIntFileName, facesSlFileName, facesAtmFileName]
for fname in filenames:
    with open(fname) as infile:
        for line in infile:
            file_faces.write(line)
file_faces.write(")\n")

file_neighbour.write("FoamFile\n")
file_neighbour.write("{\n")
file_neighbour.write("    version     2.0;\n")
file_neighbour.write("    format      ascii;\n")
file_neighbour.write("    class       labelList;\n")
file_neighbour.write("    note        \"nPoints: %d nCells: %d nFaces: %d nInternalFaces: %d\";\n" % (n_vertices, n_blocks, n_faces, n_int))
file_neighbour.write("    location    \"constant/polyMesh\";\n")
file_neighbour.write("    object      neighbour;\n")
file_neighbour.write("}\n")
file_neighbour.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n")
file_neighbour.write("\n")

file_owner.write("FoamFile\n")
file_owner.write("{\n")
file_owner.write("    version     2.0;\n")
file_owner.write("    format      ascii;\n")
file_owner.write("    class       labelList;\n")
file_owner.write("    note        \"nPoints: %d nCells: %d nFaces: %d nInternalFaces: %d\";\n" % (n_vertices, n_blocks, n_faces, n_int))
file_owner.write("    location    \"constant/polyMesh\";\n")
file_owner.write("    object      owner;\n")
file_owner.write("}\n")
file_owner.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n")
file_owner.write("\n")

owner = owner_int + owner_slp + owner_atm
owner = list(map(int, owner))
file_owner.write("%d\n" % n_faces)
file_owner.write("(\n")
file_owner.write('\n'.join(map(str, owner)))
file_owner.write(")\n")

neighbour = list(map(int, neighbour))
file_neighbour.write("%d\n" % n_int)
file_neighbour.write("(\n")
file_neighbour.write('\n'.join(map(str, neighbour)))
file_neighbour.write(")\n")

file_boundary.write("FoamFile\n")
file_boundary.write("{\n")
file_boundary.write("    version     2.0;\n")
file_boundary.write("    format      ascii;\n")
file_boundary.write("    class       polyBoundaryMesh;\n")
file_boundary.write("    location    \"constant/polyMesh\";\n")
file_boundary.write("    object      boundary;\n")
file_boundary.write("}\n")
file_boundary.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n")
file_boundary.write("\n")
file_boundary.write("2\n")
file_boundary.write("(\n")
file_boundary.write("    slope\n")
file_boundary.write("    {\n")
file_boundary.write("        type            wall;\n")
file_boundary.write("        inGroups        List<word> 1(wall);\n")
file_boundary.write("        nFaces          %d;\n" % n_slp)
file_boundary.write("        startFace       %d;\n" % n_int)
file_boundary.write("    }\n")
file_boundary.write("    atmosphere\n")
file_boundary.write("    {\n")
file_boundary.write("        type            patch;\n")
file_boundary.write("        nFaces          %d;\n" % n_atm)
file_boundary.write("        startFace       %d;\n" % (n_int + n_slp))
file_boundary.write("    }\n")
file_boundary.write(")\n")
file_boundary.write("\n")
file_boundary.write("// ************************************************************************* //\n")

file_boundary.close()
file_faces.close()
#file_faces_int.close()
#file_faces_sl.close()
#file_faces_atm.close()
file_neighbour.close()
file_owner.close()
file_points.close()
file_cellToRegion.close()

del vertices

print("Creating setFieldsDict file")
hight_of_snow = 2.0
jump = 1.0
hight_of_snow += jump
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
blocks[blocks == 0] = NODATA_value
blocks[blocks != NODATA_value] = 0
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
						if (z- z_slope + 1) * dx <= jump:
							blocks[it.multi_index[0], it.multi_index[1], z] = 0.0
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
		if it[0] != 0 and it[0] != NODATA_value:
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

print("Creating alpha.water file")
num_blocks = len(blocks[blocks != NODATA_value])
alphawaterFileName = "alpha.water"
file_alphawater = open(alphawaterFileName, "w")
file_alphawater.write("FoamFile\n")
file_alphawater.write("{\n")
file_alphawater.write("    version     2.0;\n")
file_alphawater.write("    format      ascii;\n")
file_alphawater.write("    class       volScalarField;\n")
file_alphawater.write("    location    \"0\";\n")
file_alphawater.write("    object      alpha.water;\n")
file_alphawater.write("}\n\n")
file_alphawater.write("dimensions [0 0 0 0 0 0 0];\n")
file_alphawater.write("internalField nonuniform List<scalar>\n")
file_alphawater.write("%d\n" % num_blocks)
file_alphawater.write("(\n")
for it in np.nditer(blocks):
	if it != NODATA_value:
		if it >= 0:
			file_alphawater.write("%f\n" % it)
		else:
			file_alphawater.write("%f\n" % 0.0)
file_alphawater.write(")\n;\n")
file_alphawater.write("boundaryField\n")
file_alphawater.write("{\n")
file_alphawater.write("\tslope\n")
file_alphawater.write("\t{\n")
file_alphawater.write("\t\ttype\t\tzeroGradient;\n")
file_alphawater.write("\t}\n")
file_alphawater.write("\tatmosphere\n")
file_alphawater.write("\t{\n")
file_alphawater.write("\t\ttype\t\tinletOutlet;\n")
file_alphawater.write("\t\tinletValue\tuniform 0;\n")
file_alphawater.write("\t\tvalue\t\tuniform 0;\n")
file_alphawater.write("\t}\n")
file_alphawater.write("\tdefaultFaces\n")
file_alphawater.write("\t{\n")
file_alphawater.write("\t\ttype\t\tempty;\n")
file_alphawater.write("\t}\n")
file_alphawater.write("}\n")

file_alphawater.close()

print("alpha.water file is ready")

print("Creating deposit_area file")

depositAreaFileName = "deposit_area"
file_depositArea = open(depositAreaFileName, "w")
file_depositArea.write("FoamFile\n")
file_depositArea.write("{\n")
file_depositArea.write("    version     2.0;\n")
file_depositArea.write("    format      ascii;\n")
file_depositArea.write("    class       volScalarField;\n")
file_depositArea.write("    location    \"0\";\n")
file_depositArea.write("    object      deposit_area;\n")
file_depositArea.write("}\n\n")
file_depositArea.write("dimensions [0 0 0 0 0 0 0];\n")
file_depositArea.write("internalField nonuniform List<scalar>\n")
file_depositArea.write("%d\n" % num_blocks)
file_depositArea.write("(\n")
for it in np.nditer(blocks):
	if it != NODATA_value:
		if it <= 0:
			file_depositArea.write("%f\n" % it)
		else:
			file_depositArea.write("%f\n" % 0.0)
file_depositArea.write(")\n;\n")
file_depositArea.write("boundaryField\n")
file_depositArea.write("{\n")
file_depositArea.write("\tslope\n")
file_depositArea.write("\t{\n")
file_depositArea.write("\t\ttype\t\tzeroGradient;\n")
file_depositArea.write("\t}\n")
file_depositArea.write("\tatmosphere\n")
file_depositArea.write("\t{\n")
file_depositArea.write("\t\ttype\t\tinletOutlet;\n")
file_depositArea.write("\t\tinletValue\tuniform 0;\n")
file_depositArea.write("\t\tvalue\t\tuniform 0;\n")
file_depositArea.write("\t}\n")
file_depositArea.write("\tdefaultFaces\n")
file_depositArea.write("\t{\n")
file_depositArea.write("\t\ttype\t\tempty;\n")
file_depositArea.write("\t}\n")
file_depositArea.write("}\n")

file_depositArea.close()

print("deposit_area file is ready")

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

