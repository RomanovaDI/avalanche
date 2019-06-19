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

print(ncols)
print(nrows)
print(xllcorner)
print(yllcorner)
print(cellsize)
print(NODATA_value)

print("Write new cell size if necessary:")
new_cellsize = input()
if new_cellsize == "":
	new_cellsize = cellsize
else:
	new_cellsize = float(new_cellsize)

import numpy as np
altitude = np.loadtxt(file_map, dtype=np.str)
altitude = np.char.replace(altitude, ',', '.').astype(np.float64)
with np.nditer(altitude, op_flags=['readwrite']) as it:
	for x in it:
		if x == NODATA_value:
			x[...] = 0
print(altitude)

altitude_mask = np.copy(altitude)
with np.nditer(altitude_mask, op_flags=['readwrite']) as it:
	for x in it:
		if x > 0:
			x[...] = 1

from scipy import interpolate
x = np.arange(0, cellsize * ncols, cellsize)
y = np.arange(0, cellsize * nrows, cellsize)
xnew = np.arange(0, cellsize * ncols, new_cellsize)
ynew = np.arange(0, cellsize * nrows, new_cellsize)
f = interpolate.interp2d(x, y, altitude, kind='cubic')
altitude_interpolation = f(xnew, ynew)
f = interpolate.interp2d(x, y, altitude_mask, kind='linear')
altitude_interpolation_mask = f(xnew, ynew)
with np.nditer(altitude_interpolation_mask, op_flags=['readwrite']) as it:
	for x in it:
		if x < 1:
			x[...] = 0
		else:
			x[...] = 1
altitude_interpolation = altitude_interpolation * altitude_interpolation_mask
print(xnew.shape)
print(ynew.shape)
xnew, ynew = np.meshgrid(xnew, ynew)
print(xnew.shape)
print(ynew.shape)
print(altitude_interpolation.shape)
print(altitude_interpolation_mask.shape)

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.gca(projection='3d')
#dots = ax.scatter(xnew, ynew, altitude_interpolation_mask)
surf = ax.plot_surface(xnew, ynew, altitude_interpolation)
plt.show()

file_map.close()
