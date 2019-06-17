print("Write a file of ASCII map or type enter and file name will be \"relief_22.asc\"")
map_name = input()
if map_name == "":
	map_name = "relief_22.asc"
print("Opening file: \"" + map_name + "\"")
file_map = open(map_name, "r")

line = file_map.readline()
ncols = line.split()
if ncols[0] != 'ncols':
	print("No tag \"ncols\" in first line")
	exit()
ncols[1] = int(ncols[1])

line = file_map.readline()
nrows = line.split()
if nrows[0] != 'nrows':
	print("No tag \"ncrows\" in second line")
	exit()
nrows[1] = int(nrows[1])

line = file_map.readline()
xllcorner = line.split()
if xllcorner[0] != 'xllcorner':
	print("No tag \"xllcorner\" in third line")
	exit()
xllcorner[1] = float(xllcorner[1].replace(",", "."))

line = file_map.readline()
yllcorner = line.split()
if yllcorner[0] != 'yllcorner':
	print("No tag \"yllcorner\" in fourth line")
	exit()
yllcorner[1] = float(yllcorner[1].replace(",", "."))

line = file_map.readline()
cellsize = line.split()
if cellsize[0] != 'cellsize':
	print("No tag \"cellsize\" in fifth line")
	exit()
cellsize[1] = float(cellsize[1].replace(",", "."))

line = file_map.readline()
NODATA_value = line.split()
if NODATA_value[0] != 'NODATA_value':
	print("No tag \"NODATA_value\" in sixth line")
	exit()
NODATA_value[1] = float(NODATA_value[1].replace(",", "."))

print(ncols)
print(nrows)
print(xllcorner)
print(yllcorner)
print(cellsize)
print(NODATA_value)

import numpy as np
altitude = np.loadtxt(file_map, dtype = np.str)
altitude = np.char.replace(altitude, ',', '.').astype(np.float64)
print(altitude)

file_map.close()
