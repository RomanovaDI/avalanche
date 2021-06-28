import numpy as np
from scipy import interpolate
from operator import add
import math
import sys, getopt
#import sys

def readFileNames(argv):
	mapfile = 'relief_22.asc'
	regionfile = 'region_22.asc'
	cellsize = 0
	snowdepth = 5
	areaheight = 20
	try:
		opts, args = getopt.getopt(argv[1:],'hm:r:c:s:z:',['help', 'mapfile=','regionfile=', 'cellsize=', 'snowdepth=', 'areaheight='])
	except getopt.GetoptError:
		print(argv[0] + '-m <map file> -r <region file> -c <cellsize> -s <snowdepth> -z <areaheight>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(argv[0] + '-m <map file> -r <region file> -c <cellsize> -s <snowdepth> -z <areaheight>')
			sys.exit()
		elif opt in ("-m", "--mapfile"):
			mapfile = arg
		elif opt in ("-r", "--regionfile"):
			regionfile = arg
		elif opt in ("-c", "--cellsize"):
			cellsize = float(arg)
		elif opt in ("-s", "--snowdepth"):
			snowdepth = float(arg)
		elif opt in ("-z", "--areaheight"):
			areaheight = float(arg)
	print('Map file is \"' + mapfile + '\"')
	print('Region file is \"' + regionfile + '\"')
	print('Cellsize is ' + str(cellsize) + ' meters')
	print('Depth of snow cover is ' + str(snowdepth) + ' meters')
	print('Depth of calculation area is ' + str(areaheight) + ' meters')
	return mapfile, regionfile, cellsize, snowdepth, areaheight

#def readFileNames():
#	print("Write a file of ASCII map or type enter and file name will be \"relief_22.asc\"")
#	map_name = input()
#	if map_name == "":
#		map_name = "relief_22.asc"
#	print("Write a file of ASCII region map or type enter and file name will be \"region_22.asc\"")
#	region_map_name = input()
#	if region_map_name == "":
#		region_map_name = "region_22.asc"
#	return map_name, region_map_name

class altMap:
	def __init__(self, altitude, nx, ny, dx, NODATA_value):
		self.nx = nx
		self.ny = ny
		self.dx = dx
		self.altitude = altitude
		self.NODATA_value = NODATA_value
		self.alt_max = np.amax(self.altitude[self.altitude != self.NODATA_value])
		self.alt_min = np.amin(self.altitude[self.altitude != self.NODATA_value])

class regMap:
	def __init__(self, region, nx, ny, dx, NODATA_value):
		self.nx = nx
		self.ny = ny
		self.dx = dx
		self.region = region
		self.NODATA_value = NODATA_value

def interpolateMap(mapIn, regIn, dx = -1):
	mapOut = altMap(mapIn.altitude, mapIn.nx, mapIn.ny, mapIn.dx, mapIn.NODATA_value)
	regOut = regMap(regIn.region, regIn.nx, regIn.ny, regIn.dx, regIn.NODATA_value)
	if dx == -1:
		print("Write new cell size:")
		mapOut.dx = input()
		if mapOut.dx == "":
			return;
		else:
			mapOut.dx = regOut.dx = float(mapOut.dx)
	elif dx == 0:
		return mapIn, regIn
	else:
		mapOut.dx = regOut.dx = dx

	altitude_mask = np.copy(mapIn.altitude)
	f = lambda a: 0 if a == mapIn.NODATA_value else 1
	fv = np.vectorize(f)
	altitude_mask = fv(altitude_mask)

	x = np.arange(0, mapIn.dx * mapIn.ny, mapIn.dx)
	y = np.arange(0, mapIn.dx * mapIn.nx, mapIn.dx)
	xnew = np.arange(0, mapIn.dx * mapIn.ny, mapOut.dx)
	ynew = np.arange(0, mapIn.dx * mapIn.nx, mapOut.dx)
	f = interpolate.interp2d(x, y, mapIn.altitude, kind='linear')
	altitude_interpolation = f(xnew, ynew)
	f = interpolate.interp2d(x, y, altitude_mask, kind='linear')
	altitude_interpolation_mask = f(xnew, ynew)
	f = lambda a: 0 if a < 0.9999 else 1
	fv = np.vectorize(f)
	altitude_interpolation_mask = fv(altitude_interpolation_mask)
	altitude_interpolation = altitude_interpolation * altitude_interpolation_mask
	f = lambda a: mapIn.NODATA_value if a == 0 else a
	fv = np.vectorize(f)
	altitude_interpolation = fv(altitude_interpolation)
	mapOut.ny = xnew.shape[0]
	mapOut.nx = ynew.shape[0]
	mapOut.altitude = altitude_interpolation

	region_mask = np.copy(regIn.region)
	f = lambda a: 0 if a == regIn.NODATA_value else 1
	fv = np.vectorize(f)
	region_mask = fv(region_mask)
	f = lambda a: -1 if a == 0 else a
	fv = np.vectorize(f)
	regIn.region = fv(regIn.region)

	x = np.arange(0, regIn.dx * regIn.ny, regIn.dx)
	y = np.arange(0, regIn.dx * regIn.nx, regIn.dx)
	xnew = np.arange(0, regIn.dx * regIn.ny, regOut.dx)
	ynew = np.arange(0, regIn.dx * regIn.nx, regOut.dx)
	f = interpolate.interp2d(x, y, regIn.region, kind='linear')
	region_interpolation = f(xnew, ynew)
	f = interpolate.interp2d(x, y, region_mask, kind='linear')
	region_interpolation_mask = f(xnew, ynew)
	f = lambda a: 0 if a < 0.9999 else 1
	fv = np.vectorize(f)
	region_interpolation_mask = fv(region_interpolation_mask)
	region_interpolation = region_interpolation * region_interpolation_mask
#	f = lambda a: 1 if a > 0 else 0 if a < 0 else regIn.NODATA_value
	f = lambda a: regIn.NODATA_value if a == 0 else a
	fv = np.vectorize(f)
	region_interpolation = fv(region_interpolation)
	regOut.ny = xnew.shape[0]
	regOut.nx = ynew.shape[0]
	regOut.region = region_interpolation

	return mapOut, regOut

class asc:
	def __init__(self, map_name='', region_map_name=''):
		self.map_name = map_name
		self.region_map_name = region_map_name
		self.readMapFile()
		self.readRegionFile()
		self.checkPair()

	def readMapFile(self):
		print("Opening file: \"" + self.map_name + "\"")
		file_map = open(self.map_name, "r")

		line = file_map.readline()
		line_list = line.split()
		if line_list[0] != 'ncols':
			raise ValueError('No tag \"ncols\" in first line')
		self.ncols = int(line_list[1])

		line = file_map.readline()
		line_list = line.split()
		if line_list[0] != 'nrows':
			raise ValueError('No tag \"nrows\" in second line')
		self.nrows = int(line_list[1])

		line = file_map.readline()
		line_list = line.split()
		if line_list[0] != 'xllcorner':
			raise ValueError('No tag \"xllcorner\" in third line')
		self.xllcorner = float(line_list[1].replace(",", "."))

		line = file_map.readline()
		line_list = line.split()
		if line_list[0] != 'yllcorner':
			raise ValueError('No tag \"yllcorner\" in fourth line')
		self.yllcorner = float(line_list[1].replace(",", "."))

		line = file_map.readline()
		line_list = line.split()
		if line_list[0] != 'cellsize':
			raise ValueError('No tag \"cellsize\" in fifth line')
		self.cellsize = float(line_list[1].replace(",", "."))

		line = file_map.readline()
		line_list = line.split()
		if line_list[0] != 'NODATA_value':
			raise ValueError('No tag \"NODATA_value\" in sixth line')
		self.NODATA_value = float(line_list[1].replace(",", "."))

		altitude = np.loadtxt(file_map, dtype=np.str)
		file_map.close()
		altitude = np.char.replace(altitude, ',', '.').astype(np.float32)
		self.am = altMap(altitude, self.nrows, self.ncols, self.cellsize, self.NODATA_value)

	def readRegionFile(self):
		print("Opening file: \"" + self.region_map_name + "\"")
		region_file_map = open(self.region_map_name, "r")

		line = region_file_map.readline()
		line_list = line.split()
		if line_list[0] != 'ncols':
			raise ValueError('No tag \"ncols\" in first line')
		self.region_ncols = int(line_list[1])

		line = region_file_map.readline()
		line_list = line.split()
		if line_list[0] != 'nrows':
			raise ValueError('No tag \"nrows\" in second line')
		self.region_nrows = int(line_list[1])

		line = region_file_map.readline()
		line_list = line.split()
		if line_list[0] != 'xllcorner':
			raise ValueError('No tag \"xllcorner\" in third line')
		self.region_xllcorner = float(line_list[1].replace(",", "."))

		line = region_file_map.readline()
		line_list = line.split()
		if line_list[0] != 'yllcorner':
			raise ValueError('No tag \"yllcorner\" in fourth line')
		self.region_yllcorner = float(line_list[1].replace(",", "."))

		line = region_file_map.readline()
		line_list = line.split()
		if line_list[0] != 'cellsize':
			raise ValueError('No tag \"cellsize\" in fifth line')
		self.region_cellsize = float(line_list[1].replace(",", "."))

		line = region_file_map.readline()
		line_list = line.split()
		if line_list[0] != 'NODATA_value':
			raise ValueError('No tag \"NODATA_value\" in sixth line')
		self.region_NODATA_value = float(line_list[1].replace(",", "."))

		region_pre = np.loadtxt(region_file_map, dtype=np.str)
		region_file_map.close()
		region_pre = np.char.replace(region_pre, ',', '.').astype(np.float32)
		x_margin = self.nrows - self.region_nrows - int((self.region_yllcorner - self.yllcorner) / self.cellsize)
		y_margin = int((self.region_xllcorner - self.xllcorner) / self.cellsize)
		region = np.full(self.am.altitude.shape, self.am.NODATA_value)
		with np.nditer(region, flags=['multi_index'], op_flags=['writeonly']) as it:
			while not it.finished:
				if	it.multi_index[0] >= x_margin and\
					it.multi_index[1] >= y_margin and\
					it.multi_index[0] - x_margin < self.region_nrows and\
					it.multi_index[1] - y_margin < self.region_ncols and\
					region_pre[it.multi_index[0]-x_margin, it.multi_index[1]-y_margin] != self.region_NODATA_value:
						it[0] = region_pre[it.multi_index[0]-x_margin, it.multi_index[1]-y_margin]
				it.iternext()
		self.rg = regMap(region, self.nrows, self.ncols, self.cellsize, self.NODATA_value)

	def checkPair(self):
		if not self.xllcorner <= self.region_xllcorner <= self.xllcorner + self.ncols * self.cellsize:
			raise ValueError('Error pair of map and region map')
		if not self.yllcorner <= self.region_yllcorner <= self.yllcorner + self.nrows * self.cellsize:
			raise ValueError('Error pair of map and region map')
