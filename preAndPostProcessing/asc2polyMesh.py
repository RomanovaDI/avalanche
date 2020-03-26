import numpy as np
from scipy import interpolate
from operator import add
import math
#import sys

def readFileNames():
	print("Write a file of ASCII map or type enter and file name will be \"relief_22.asc\"")
	map_name = input()
	if map_name == "":
		map_name = "relief_22.asc"
	print("Write a file of ASCII region map or type enter and file name will be \"region_22.asc\"")
	region_map_name = input()
	if region_map_name == "":
		region_map_name = "region_22.asc"
	return map_name, region_map_name

class map:

	def __init__(self, altitude, nx, ny, cellsize, NODATA_value):
		self.nx = nx
		self ny = ny
		self.cellsize = cellsize
		self.altitude = altitude
		self.NODATA_value = NODATA_value

def interpolateMap(mapIn, cellsize = -1):
	map mapOut
	if cellsize == -1:
		print("Write new cell size:")
		mapOut.cellsize = input()
		if mapOut.cellsize == "":
			return;
		else:
			mapOut.cellsize = float(mapOut.cellsize)
	else:
		mapOut.cellsize = cellsize

	altitude_mask = np.copy(mapIn.altitude)
	f = lambda a: 0 if a == mapIn.NODATA_value else 1
	fv = np.vectorize(f)
	altitude_mask = fv(altitude_mask)

	x = np.arange(0, mapIn.cellsize * mapIn.ncols, mapIn.cellsize)
	y = np.arange(0, mapIn.cellsize * MapIn.nrows, mapIn.cellsize)
	xnew = np.arange(0, mapIn.cellsize * mapIn.ncols, mapOut.cellsize)
	ynew = np.arange(0, mapIn.cellsize * mapIn.nrows, mapOut.cellsize)
	f = interpolate.interp2d(x, y, mapIn.altitude, kind='linear')
	altitude_interpolation = f(xnew, ynew)
	f = interpolate.interp2d(x, y, altitude_mask, kind='linear')
	altitude_interpolation_mask = f(xnew, ynew)
	f = lambda a: 0 if a < 1 else 1
	fv = np.vectorize(f)
	altitude_interpolation_mask = fv(altitude_interpolation_mask)
	altitude_interpolation = altitude_interpolation * altitude_interpolation_mask
	f = lambda a: mapIn.NODATA_value if a == 0 else a
	fv = np.vectorize(f)
	altitude_interpolation = fv(altitude_interpolation)
	mapOut.ny = xnew.shape[0]
	mapOut.nx = ynew.shape[0]
	mapOut.altitude = altitude_interpolation
	return mapOut
class asc:

	def __init__(self, map_name='', region_map_name=''):
		self.map_name = map_name
		self.region_map_name = region_map_name
		self.readMapFile()
		self.readRegionFile()
		self.checkPair()
		self.loadMap()
		#self.altitude = self.interpolateMap()

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

		self.region = np.loadtxt(region_file_map, dtype=np.str)
		region_file_map.close()
		self.region = np.char.replace(self.region, ',', '.').astype(np.float32)

	def checkPair(self):
		if not self.xllcorner <= self.region_xllcorner <= self.xllcorner + self.ncols * self.cellsize:
			raise ValueError('Error pair of map and region map')
		if not self.yllcorner <= self.region_yllcorner <= self.yllcorner + self.nrows * self.cellsize:
			raise ValueError('Error pair of map and region map')

	def loadMap(self):
		altitude = np.loadtxt(file_map, dtype=np.str)
		file_map.close()
		altitude = np.char.replace(altitude, ',', '.').astype(np.float32)
		self.altMap = map(altitude, self.ncols, self.nrows, self.cellsize, self.NODATA_value)

class files:
	def __init__(self, slopeData, height=16.):
		self.sd = slopeData
		self.height = height
		self.prepareSlopeDataFlag = 0
		self.prepareSlopeDataGradFlag = 0

	def prepareSlopeData(self):
		if self.prepareSlopeDataFlag == 1:
			return
		self.prepareSlopeDataFlag = 1
		f = lambda a: math.floor(a / self.sd.altMap.cellsize) * self.sd.altMap.cellsize if a != 0 else self.sd.altMap.NODATA_value
		fv = np.vectorize(f)
		self.sd.altitude = fv(self.sd.altitude)
		self.alt_max = np.amax(self.sd.altitude)
		self.alt_min = np.amin(self.sd.altitude[self.sd.altitude != self.sd.NODATA_value])
		self.height = math.floor(self.height / self.sd.dx) * self.sd.dx
		self.sd.nz = int((self.alt_max - self.alt_min + self.height) / self.sd.dx)
		self.vertices = np.full((self.sd.nx + 1, self.sd.ny + 1, self.sd.nz + 1), -1, dtype=np.int32)
		self.blocks = np.zeros((self.sd.nx, self.sd.ny, self.sd.nz), dtype=np.float32)
		with np.nditer(self.sd.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
			while not it.finished:
				if it[0] != self.sd.NODATA_value:
					for z in range(int((it[0] - self.alt_min) / self.sd.dx), int((it[0] - self.alt_min + self.height) / self.sd.dx) + 1):
						self.vertices[it.multi_index[0], it.multi_index[1], z] = 1
						self.vertices[it.multi_index[0] + 1, it.multi_index[1], z] = 1
						self.vertices[it.multi_index[0], it.multi_index[1] + 1, z] = 1
						self.vertices[it.multi_index[0] + 1, it.multi_index[1] + 1, z] = 1
					for z in range(int((it[0] - self.alt_min) / self.sd.dx), int((it[0] - self.alt_min + self.height) / self.sd.dx)):
						self.blocks[it.multi_index[0], it.multi_index[1], z] = 1
					self.blocks[it.multi_index[0], it.multi_index[1], int((it[0] - self.alt_min) / self.sd.dx)] = 2
				it.iternext()
		ind = 0
		for it in np.nditer(self.vertices, op_flags=['readwrite']):
			if it == 1:
				it[...] = ind
				ind += 1
		self.blocks_ind = np.copy(self.blocks)
		ind = 0;
		for it in np.nditer(self.blocks_ind, op_flags=['readwrite']):
			if it != 0:
				it[...] = ind
				ind += 1
		self.n_blocks = ind
		self.n_vertices = (self.vertices != -1).sum()

	def createBlockMeshDict(self):
		self.prepareSlopeData()
		print("Creating blockMeshDict file")
		blockMeshDictFileName = "blockMeshDict"
		file_blockMeshDict = open(blockMeshDictFileName, "w")
		file_blockMeshDict.write("FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tobject\tblockMeshDict;\n}\n\nconvertToMeters 1.0;\n\n")
		file_blockMeshDict.write("vertices\n(\n")
		with np.nditer(self.vertices, flags=['multi_index'], op_flags=["readonly"]) as it:
			while not it.finished:
				if it[0] != -1:
					file_blockMeshDict.write("\t(%f\t%f\t%f)\n" % (it.multi_index[0] * self.sd.dx, it.multi_index[1] * self.sd.dx, it.multi_index[2] * self.sd.dx))
				it.iternext()
		file_blockMeshDict.write(");\n\nblocks\n(\n")
		with np.nditer(self.blocks, flags=['multi_index'], op_flags=["readonly"]) as it:
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
						(self.vertices[vert0], self.vertices[vert1], self.vertices[vert2], self.vertices[vert3], self.vertices[vert4],\
						self.vertices[vert5], self.vertices[vert6], self.vertices[vert7]))
				it.iternext()
		file_blockMeshDict.write(");\n\nedges\n(\n);\n\nboundary\n(\n\tslope\n\t{\n\t\ttype wall;\n\t\tfaces\n\t\t(\n")
		with np.nditer(self.blocks, flags=['multi_index'], op_flags=["readonly"]) as it:
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
					file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (self.vertices[vert3], self.vertices[vert2], self.vertices[vert1], self.vertices[vert0]))
					neighbour_ind = tuple(map(add, it.multi_index, (-1, 0, 0)))
					if neighbour_ind[0] < 0 or self.blocks[neighbour_ind] == 0:
						file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (self.vertices[vert0], self.vertices[vert4], self.vertices[vert7], self.vertices[vert3]))
					neighbour_ind = tuple(map(add, it.multi_index, (1, 0, 0)))
					if neighbour_ind[0] >= self.sd.nx or self.blocks[neighbour_ind] == 0:
						file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (self.vertices[vert1], self.vertices[vert2], self.vertices[vert6], self.vertices[vert5]))
					neighbour_ind = tuple(map(add, it.multi_index, (0, -1, 0)))
					if neighbour_ind[1] < 0 or self.blocks[neighbour_ind] == 0:
						file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (self.vertices[vert0], self.vertices[vert1], self.vertices[vert5], self.vertices[vert4]))
					neighbour_ind = tuple(map(add, it.multi_index, (0, 1, 0)))
					if neighbour_ind[1] >= self.sd.ny or self.blocks[neighbour_ind] == 0:
						file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (self.vertices[vert2], self.vertices[vert3], self.vertices[vert7], self.vertices[vert6]))
					neighbour_ind = tuple(map(add, it.multi_index, (0, 0, 1)))
					if neighbour_ind[2] >= self.sd.nz or self.blocks[neighbour_ind] == 0:
						file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (self.vertices[vert4], self.vertices[vert5], self.vertices[vert6], self.vertices[vert7]))
				it.iternext()
		file_blockMeshDict.write("\t\t);\n\t}\n\tatmosphere\n\t{\n\t\ttype patch;\n\t\tfaces\n\t\t(\n")
		with np.nditer(self.blocks, flags=['multi_index'], op_flags=["readonly"]) as it:
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
					if neighbour_ind[0] < 0 or self.blocks[neighbour_ind] == 0:
						file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (self.vertices[vert0], self.vertices[vert4], self.vertices[vert7], self.vertices[vert3]))
					neighbour_ind = tuple(map(add, it.multi_index, (1, 0, 0)))
					if neighbour_ind[0] >= self.sd.nx or self.blocks[neighbour_ind] == 0:
						file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (self.vertices[vert1], self.vertices[vert2], self.vertices[vert6], self.vertices[vert5]))
					neighbour_ind = tuple(map(add, it.multi_index, (0, -1, 0)))
					if neighbour_ind[1] < 0 or self.blocks[neighbour_ind] == 0:
						file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (self.vertices[vert0], self.vertices[vert1], self.vertices[vert5], self.vertices[vert4]))
					neighbour_ind = tuple(map(add, it.multi_index, (0, 1, 0)))
					if neighbour_ind[1] >= self.sd.ny or self.blocks[neighbour_ind] == 0:
						file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (self.vertices[vert2], self.vertices[vert3], self.vertices[vert7], self.vertices[vert6]))
					neighbour_ind = tuple(map(add, it.multi_index, (0, 0, 1)))
					if neighbour_ind[2] >= self.sd.nz or self.blocks[neighbour_ind] == 0:
						file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (self.vertices[vert4], self.vertices[vert5], self.vertices[vert6], self.vertices[vert7]))
				it.iternext()
		file_blockMeshDict.write("\t\t);\n\t}\n);\n\nmergePatchPairs\n(\n);\n")
		file_blockMeshDict.close()
		print("blockMeshDict file is ready")

	def createBlockMeshDictInclined(self):
		print("Creating blockMeshDict file")
		blockMeshDictFileName = "blockMeshDict"
		file_blockMeshDict = open(blockMeshDictFileName, "w")
		blocksFileName = "blocks"
		file_blocks = open(blocksFileName, "w")
		boundariesSlopeFileName = "boundarySlope"
		file_boundaries_slope = open(boundariesSlopeFileName, "w")
		boundariesAtmosphereFileName = "boundaryAtmosphere"
		file_boundaries_atmosphere = open(boundariesAtmosphereFileName, "w")
		file_blockMeshDict.write("FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tobject\tblockMeshDict;\n}\n\nscale 1.0;\n\n")
		file_blockMeshDict.write("vertices\n(\n")
		tmp = self.sd.dx
		while tmp < self.height:
			tmp *= 2
		self.height = tmp
		nz = int(math.log(self.height / self.sd.dx, 2)) + 1
		heights = np.full(nz, self.sd.dx)
		heights[0] = 0
		for i in range(1, nz):
			heights[i] *= pow(2,i-1)
		ind = np.copy(self.sd.altitude)
		tmp = 0
		with np.nditer(ind, flags=['multi_index'], op_flags=["readwrite"]) as it:
			while not it.finished:
				if it[0] != self.sd.NODATA_value:
					it[0] = tmp
					tmp += 1
				else:
					it[0] = -1
				it.iternext()
		with np.nditer(self.sd.altitude, flags=['multi_index'], op_flags=["readonly"]) as it:
			while not it.finished:
				if it[0] != self.sd.NODATA_value:
					for z in heights:
						file_blockMeshDict.write("\t(%f\t%f\t%f)\n" %\
							(it.multi_index[0] * self.sd.dx, it.multi_index[1] * self.sd.dx, it[0] + z))
				it.iternext()
		file_blocks.write(");\n\nblocks\n(\n")
		with np.nditer(ind, flags=['multi_index'], op_flags=["readonly"]) as it:
			while not it.finished:
				if it[0] != -1:
					vert0 = it.multi_index
					vert1 = tuple(map(add, it.multi_index, (1, 0)))
					vert2 = tuple(map(add, it.multi_index, (1, 1)))
					vert3 = tuple(map(add, it.multi_index, (0, 1)))
					if	vert1[0] < self.sd.nx and vert3[1] < self.sd.ny and\
						ind[vert1] != -1 and ind[vert2] != -1 and ind[vert3] != -1:
							for z in range(nz-1):
								file_blocks.write("\thex (%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d)\t(1 1 1) simpleGrading (1 1 1)\n" % \
									(nz*ind[vert0]+z, nz*ind[vert1]+z, nz*ind[vert2]+z, nz*ind[vert3]+z,\
									nz*ind[vert0]+z+1, nz*ind[vert1]+z+1, nz*ind[vert2]+z+1, nz*ind[vert3]+z+1))
					if	vert1[0] < self.sd.nx and vert3[1] < self.sd.ny and\
						ind[vert1] != -1 and ind[vert2] != -1 and ind[vert3] != -1:
							file_boundaries_slope.write("\t\t\t(%d %d %d %d)\n" % (nz*ind[vert3], nz*ind[vert2], nz*ind[vert1], nz*ind[vert0]))
					if	vert1[0] < self.sd.nx and vert3[1] < self.sd.ny and\
						ind[vert1] != -1 and ind[vert2] != -1 and ind[vert3] != -1:
							file_boundaries_atmosphere.write("\t\t\t(%d %d %d %d)\n" % (nz*ind[vert0]+nz-1, nz*ind[vert1]+nz-1, nz*ind[vert2]+nz-1, nz*ind[vert3]+nz-1))
							neighbour_ind1 = tuple(map(add, it.multi_index, (-1, 0)))
							neighbour_ind2 = tuple(map(add, it.multi_index, (-1, 1)))
							if neighbour_ind1[0] < 0 or ind[neighbour_ind1] == -1 or neighbour_ind2[0] < 0 or ind[neighbour_ind2] == -1:
								for z in range(nz-1):
									file_boundaries_atmosphere.write("\t\t\t(%d %d %d %d)\n" % (nz*ind[vert3]+z, nz*ind[vert0]+z, nz*ind[vert0]+z+1, nz*ind[vert3]+z+1))
							neighbour_ind1 = tuple(map(add, it.multi_index, (2, 0)))
							neighbour_ind2 = tuple(map(add, it.multi_index, (2, 1)))
							if neighbour_ind1[0] >= self.sd.nx or ind[neighbour_ind1] == -1 or neighbour_ind2[0] >= self.sd.nx or ind[neighbour_ind2] == -1:
								for z in range(nz-1):
									file_boundaries_atmosphere.write("\t\t\t(%d %d %d %d)\n" % (nz*ind[vert1]+z, nz*ind[vert2]+z, nz*ind[vert2]+z+1, nz*ind[vert1]+z+1))
							neighbour_ind1 = tuple(map(add, it.multi_index, (0, -1)))
							neighbour_ind2 = tuple(map(add, it.multi_index, (1, -1)))
							if neighbour_ind1[1] < 0 or ind[neighbour_ind1] == -1 or neighbour_ind2[1] < 0 or ind[neighbour_ind2] == -1:
								for z in range(nz-1):
									file_boundaries_atmosphere.write("\t\t\t(%d %d %d %d)\n" % (nz*ind[vert0]+z, nz*ind[vert1]+z, nz*ind[vert1]+z+1, nz*ind[vert0]+z+1))
							neighbour_ind1 = tuple(map(add, it.multi_index, (0, 2)))
							neighbour_ind2 = tuple(map(add, it.multi_index, (1, 2)))
							if neighbour_ind1[1] >= self.sd.ny or ind[neighbour_ind1] == -1 or neighbour_ind2[1] >= self.sd.ny or ind[neighbour_ind2] == -1:
								for z in range(nz-1):
									file_boundaries_atmosphere.write("\t\t\t(%d %d %d %d)\n" % (nz*ind[vert2]+z, nz*ind[vert3]+z, nz*ind[vert3]+z+1, nz*ind[vert2]+z+1))
				it.iternext()
		file_blocks.write(");\n\nedges\n(\n);\n\nboundary\n(\n\tslope\n\t{\n\t\ttype wall;\n\t\tfaces\n\t\t(\n")
		file_boundaries_slope.write("\t\t);\n\t}\n\tatmosphere\n\t{\n\t\ttype patch;\n\t\tfaces\n\t\t(\n")
		file_boundaries_atmosphere.write("\t\t);\n\t}\n);\n\nmergePatchPairs\n(\n);\n")
		file_blocks.close()
		file_boundaries_slope.close()
		file_boundaries_atmosphere.close()
		filenames = [blocksFileName, boundariesSlopeFileName, boundariesAtmosphereFileName]
		for fname in filenames:
			with open(fname) as infile:
				for line in infile:
					file_blockMeshDict.write(line)
		file_blockMeshDict.close()
		print("blockMeshDict file is ready")

	def polyMesh(self):
		self.prepareSlopeData()
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

		file_cellToRegion.write("FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tlabelList;\n\tlocation\t\"0\";\n\tobject\tcellToRegion;\n}\n\n")
		file_faces.write("FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tfaceList;\n\tlocation\t\"constant/polyMesh\";\n\tobject\tfaces;\n}\n\n")
		file_points.write("FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tvectorField;\n\tlocation\t\"constant/polyMesh\";\n\tobject\tpoints;\n}\n\n")
		file_points.write("%d(\n"%self.n_vertices)
		with np.nditer(self.vertices, flags=['multi_index'], op_flags=["readonly"]) as it:
			while not it.finished:
				if it[0] != -1:
					file_points.write("(%.0f\t%.0f\t%.0f)\n" % (it.multi_index[0] * self.sd.dx, it.multi_index[1] * self.sd.dx, it.multi_index[2] * self.sd.dx + self.alt_min))
				it.iternext()
		file_points.write(")\n")

		n_int = n_atm = n_slp = 0
		owner_int = []
		owner_slp = []
		owner_atm = []
		neighbour = []
		with np.nditer(self.blocks, flags=['multi_index'], op_flags=["readonly"]) as it:
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
					if neighbour_ind[2] < 0 or self.blocks[neighbour_ind] == 0:
						if it[0] == 1:
							file_faces_atm.write("4(%d %d %d %d)\n" % (self.vertices[vert3], self.vertices[vert2], self.vertices[vert1], self.vertices[vert0]))
							n_atm += 1
							owner_atm.append(self.blocks_ind[it.multi_index])
						if it[0] == 2:
							file_faces_sl.write("4(%d %d %d %d)\n" % (self.vertices[vert3], self.vertices[vert2], self.vertices[vert1], self.vertices[vert0]))
							n_slp += 1
							owner_slp.append(self.blocks_ind[it.multi_index])
					elif self.blocks_ind[it.multi_index] < self.blocks_ind[neighbour_ind]:
						file_faces_int.write("4(%d %d %d %d)\n" % (self.vertices[vert3], self.vertices[vert2], self.vertices[vert1], self.vertices[vert0]))
						n_int += 1
						owner_int.append(self.blocks_ind[it.multi_index])
						neighbour.append(self.blocks_ind[neighbour_ind])
					neighbour_ind = tuple(map(add, it.multi_index, (-1, 0, 0)))
					if neighbour_ind[0] < 0 or self.blocks[neighbour_ind] == 0:
						if it[0] == 1:
							file_faces_atm.write("4(%d %d %d %d)\n" % (self.vertices[vert0], self.vertices[vert4], self.vertices[vert7], self.vertices[vert3]))
							n_atm += 1
							owner_atm.append(self.blocks_ind[it.multi_index])
						if it[0] == 2:
							file_faces_sl.write("4(%d %d %d %d)\n" % (self.vertices[vert0], self.vertices[vert4], self.vertices[vert7], self.vertices[vert3]))
							n_slp += 1
							owner_slp.append(self.blocks_ind[it.multi_index])
					elif self.blocks_ind[it.multi_index] < self.blocks_ind[neighbour_ind]:
						file_faces_int.write("4(%d %d %d %d)\n" % (self.vertices[vert0], self.vertices[vert4], self.vertices[vert7], self.vertices[vert3]))
						n_int += 1
						owner_int.append(self.blocks_ind[it.multi_index])
						neighbour.append(self.blocks_ind[neighbour_ind])
					neighbour_ind = tuple(map(add, it.multi_index, (0, -1, 0)))
					if neighbour_ind[1] < 0 or self.blocks[neighbour_ind] == 0:
						if it[0] == 1:
							file_faces_atm.write("4(%d %d %d %d)\n" % (self.vertices[vert0], self.vertices[vert1], self.vertices[vert5], self.vertices[vert4]))
							n_atm += 1
							owner_atm.append(self.blocks_ind[it.multi_index])
						if it[0] == 2:
							file_faces_sl.write("4(%d %d %d %d)\n" % (self.vertices[vert0], self.vertices[vert1], self.vertices[vert5], self.vertices[vert4]))
							n_slp += 1
							owner_slp.append(self.blocks_ind[it.multi_index])
					elif self.blocks_ind[it.multi_index] < self.blocks_ind[neighbour_ind]:
						file_faces_int.write("4(%d %d %d %d)\n" % (self.vertices[vert0], self.vertices[vert1], self.vertices[vert5], self.vertices[vert4]))
						n_int += 1
						owner_int.append(self.blocks_ind[it.multi_index])
						neighbour.append(self.blocks_ind[neighbour_ind])
					neighbour_ind = tuple(map(add, it.multi_index, (0, 1, 0)))
					if neighbour_ind[1] >= self.sd.ny or self.blocks[neighbour_ind] == 0:
						if it[0] == 1:
							file_faces_atm.write("4(%d %d %d %d)\n" % (self.vertices[vert2], self.vertices[vert3], self.vertices[vert7], self.vertices[vert6]))
							n_atm += 1
							owner_atm.append(self.blocks_ind[it.multi_index])
						if it[0] == 2:
							file_faces_sl.write("4(%d %d %d %d)\n" % (self.vertices[vert2], self.vertices[vert3], self.vertices[vert7], self.vertices[vert6]))
							n_slp += 1
							owner_slp.append(self.blocks_ind[it.multi_index])
					elif self.blocks_ind[it.multi_index] < self.blocks_ind[neighbour_ind]:
						file_faces_int.write("4(%d %d %d %d)\n" % (self.vertices[vert2], self.vertices[vert3], self.vertices[vert7], self.vertices[vert6]))
						n_int += 1
						owner_int.append(self.blocks_ind[it.multi_index])
						neighbour.append(self.blocks_ind[neighbour_ind])
					neighbour_ind = tuple(map(add, it.multi_index, (1, 0, 0)))
					if neighbour_ind[0] >= self.sd.nx or self.blocks[neighbour_ind] == 0:
						if it[0] == 1:
							file_faces_atm.write("4(%d %d %d %d)\n" % (self.vertices[vert1], self.vertices[vert2], self.vertices[vert6], self.vertices[vert5]))
							n_atm += 1
							owner_atm.append(self.blocks_ind[it.multi_index])
						if it[0] == 2:
							file_faces_sl.write("4(%d %d %d %d)\n" % (self.vertices[vert1], self.vertices[vert2], self.vertices[vert6], self.vertices[vert5]))
							n_slp += 1
							owner_slp.append(self.blocks_ind[it.multi_index])
					elif self.blocks_ind[it.multi_index] < self.blocks_ind[neighbour_ind]:
						file_faces_int.write("4(%d %d %d %d)\n" % (self.vertices[vert1], self.vertices[vert2], self.vertices[vert6], self.vertices[vert5]))
						n_int += 1
						owner_int.append(self.blocks_ind[it.multi_index])
						neighbour.append(self.blocks_ind[neighbour_ind])
					neighbour_ind = tuple(map(add, it.multi_index, (0, 0, 1)))
					if neighbour_ind[2] >= self.sd.nz or self.blocks[neighbour_ind] == 0:
						if it[0] == 1:
							file_faces_atm.write("4(%d %d %d %d)\n" % (self.vertices[vert4], self.vertices[vert5], self.vertices[vert6], self.vertices[vert7]))
							n_atm += 1
							owner_atm.append(self.blocks_ind[it.multi_index])
						if it[0] == 2:
							file_faces_sl.write("4(%d %d %d %d)\n" % (self.vertices[vert4], self.vertices[vert5], self.vertices[vert6], self.vertices[vert7]))
							n_slp += 1
							owner_slp.append(self.blocks_ind[it.multi_index])
					elif self.blocks_ind[it.multi_index] < self.blocks_ind[neighbour_ind]:
						file_faces_int.write("4(%d %d %d %d)\n" % (self.vertices[vert4], self.vertices[vert5], self.vertices[vert6], self.vertices[vert7]))
						n_int += 1
						owner_int.append(self.blocks_ind[it.multi_index])
						neighbour.append(self.blocks_ind[neighbour_ind])
				it.iternext()

		n_faces = n_int + n_slp + n_atm
		file_faces.write("%d\n(\n" % n_faces)
		
		file_faces_int.close()
		file_faces_sl.close()
		file_faces_atm.close()
		filenames = [facesIntFileName, facesSlFileName, facesAtmFileName]
		for fname in filenames:
			with open(fname) as infile:
				for line in infile:
					file_faces.write(line)
		file_faces.write(")\n")

		file_neighbour.write("FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tlabelList;\n")
		file_neighbour.write("\tnote\t\"nPoints: %d nCells: %d nFaces: %d nInternalFaces: %d\";\n" % (self.n_vertices, self.n_blocks, n_faces, n_int))
		file_neighbour.write("\tlocation\t\"constant/polyMesh\";\n\tobject\tneighbour;\n}\n\n")

		file_owner.write("FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tlabelList;\n")
		file_owner.write("\tnote\t\"nPoints: %d nCells: %d nFaces: %d nInternalFaces: %d\";\n" % (self.n_vertices, self.n_blocks, n_faces, n_int))
		file_owner.write("\tlocation\t\"constant/polyMesh\";\n\tobject\towner;\n}\n\n")

		owner = owner_int + owner_slp + owner_atm
		owner = list(map(int, owner))
		file_owner.write("%d\n(\n" % n_faces)
		file_owner.write('\n'.join(map(str, owner)))
		file_owner.write(")\n")

		neighbour = list(map(int, neighbour))
		file_neighbour.write("%d\n(\n" % n_int)
		file_neighbour.write('\n'.join(map(str, neighbour)))
		file_neighbour.write(")\n")

		file_boundary.write("FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tpolyBoundaryMesh;\n\tlocation\t\"constant/polyMesh\";\n\tobject\tboundary;\n}\n\n")
		file_boundary.write("2\n(\n\tslope\n\t{\n\t\ttype\twall;\n\t\tinGroups\tList<word> 1(wall);\n\t\tnFaces\t%d;\n\t\tstartFace\t%d;\n\t}\n" % (n_slp, n_int))
		file_boundary.write("\tatmosphere\n\t{\n\t\ttype\tpatch;\n\t\tnFaces\t%d;\n\t\tstartFace\t%d;\n\t}\n)\n\n" % (n_atm, (n_int + n_slp)))

		file_boundary.close()
		file_faces.close()
		#file_faces_int.close()
		#file_faces_sl.close()
		#file_faces_atm.close()
		file_neighbour.close()
		file_owner.close()
		file_points.close()
		file_cellToRegion.close()

	def createSetFieldsDict(self, height_of_snow=2.0, jump=1.0):
		print("Creating setFieldsDict file")
		height_of_snow += jump
		x_offset = int((self.sd.region_xllcorner - self.sd.xllcorner) / self.sd.dx)
		y_offset = int((self.sd.region_yllcorner - self.sd.yllcorner) / self.sd.dx)
		f = lambda a: 0 if a == self.sd.region_NODATA_value else (1 if a == 1 else -1)
		fv = np.vectorize(f)
		region = fv(self.sd.region)
		x = np.arange(0, self.sd.region_cellsize * self.sd.region_ncols, self.sd.region_cellsize)
		y = np.arange(0, self.sd.region_cellsize * self.sd.region_nrows, self.sd.region_cellsize)
		xnew = np.arange(0, self.sd.region_cellsize * self.sd.region_ncols, self.sd.new_cellsize)
		ynew = np.arange(0, self.sd.region_cellsize * self.sd.region_nrows, self.sd.new_cellsize)
		f = interpolate.interp2d(x, y, region, kind='linear')
		region = f(xnew, ynew)
		f = lambda a: 0 if (-1 < a < 1) else (1 if a >= 1 else -1)
		fv = np.vectorize(f)
		region = fv(region)
		self.blocks[self.blocks == 0] = self.sd.NODATA_value
		self.blocks[self.blocks != self.sd.NODATA_value] = 0
		with np.nditer(self.sd.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
			while not it.finished:
				if it[0] != self.sd.NODATA_value\
					and 0 <= it.multi_index[0] - x_offset < region.shape[0]\
					and 0 <= it.multi_index[1] - y_offset < region.shape[1]\
					and region[it.multi_index[0] - x_offset, it.multi_index[1] - y_offset] != 0:
						if region[it.multi_index[0] - x_offset, it.multi_index[1] - y_offset] == -1:
							z_slope = int((it[0] - self.alt_min) / self.sd.dx)
							for z in range(int((it[0] - self.alt_min) / self.sd.dx), int(math.ceil((it[0] - self.alt_min + height_of_snow) / self.sd.dx))):
								self.blocks[it.multi_index[0], it.multi_index[1], z] = 1.0 if (z - z_slope + 1) * self.sd.dx <= height_of_snow else ((z - z_slope + 1) * self.sd.dx - height_of_snow) / self.sd.dx
								if (z- z_slope + 1) * self.sd.dx <= jump:
									self.blocks[it.multi_index[0], it.multi_index[1], z] = 0.0
						else:
							for z in range(int((it[0] - self.alt_min) / self.sd.dx), int((it[0] - self.alt_min + self.height) / self.sd.dx)):
								self.blocks[it.multi_index[0], it.multi_index[1], z] = -1.0
				it.iternext()
		setFieldsDictFileName = "setFieldsDict"
		file_setFieldsDict = open(setFieldsDictFileName, "w")
		file_setFieldsDict.write("FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tlocation\t\"system\";\n\tobject\tsetFieldsDict;\n}\n\n")
		file_setFieldsDict.write("defaultFieldValues\n(\n\tvolScalarFieldValue alpha.water 0\n\tvolScalarFieldValue deposit_area 0\n);\n\n")
		file_setFieldsDict.write("regions\n(\n")
		with np.nditer(self.blocks, flags=['multi_index'], op_flags=["readonly"]) as it:
			while not it.finished:
				if it[0] != 0 and it[0] != self.sd.NODATA_value:
					file_setFieldsDict.write("\tboxToCell\n\t{\n\t\tbox (%f\t%f\t%f) (%f\t%f\t%f);\n\t\tfieldValues\n\t\t(\n" %\
						(it.multi_index[0] * self.sd.dx, it.multi_index[1] * self.sd.dx, it.multi_index[2] * self.sd.dx + self.alt_min,\
						it.multi_index[0] * self.sd.dx + self.sd.dx, it.multi_index[1] * self.sd.dx + self.sd.dx, it.multi_index[2] * self.sd.dx + self.sd.dx + self.alt_min))
					if it[0] > 0:
						file_setFieldsDict.write("\t\t\tvolScalarFieldValue alpha.water %f\n" % it[0])
					else:
						file_setFieldsDict.write("\t\t\tvolScalarFieldValue deposit_area 1\n")
					file_setFieldsDict.write("\t\t);\n\t}\n")
				it.iternext()
		file_setFieldsDict.write(");\n")
		file_setFieldsDict.close()
		print("setFieldsDict file is ready")

	def createAlphaWater(self):
		print("Creating alpha.water file")
		num_blocks = len(self.blocks[self.blocks != self.sd.NODATA_value])
		alphawaterFileName = "alpha.water"
		file_alphawater = open(alphawaterFileName, "w")
		file_alphawater.write("FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tvolScalarField;\n\tlocation\t\"0\";\n\tobject\talpha.water;\n}\n\n\
			dimensions [0 0 0 0 0 0 0];\ninternalField nonuniform List<scalar>\n%d\n(\n" % num_blocks)
		for it in np.nditer(self.blocks):
			if it != self.sd.NODATA_value:
				if it >= 0:
					file_alphawater.write("%f\n" % it)
				else:
					file_alphawater.write("%f\n" % 0.0)
		file_alphawater.write(")\n;\nboundaryField\n{\n\tslope\n\t{\n\t\ttype\t\tzeroGradient;\n\t}\n\tatmosphere\n\t{\n\t\ttype\t\tinletOutlet;\
			\n\t\tinletValue\tuniform 0;\n\t\tvalue\t\tuniform 0;\n\t}\n\tdefaultFaces\n\t{\n\t\ttype\t\tempty;\n\t}\n}\n")
		file_alphawater.close()
		print("alpha.water file is ready")

		print("Creating deposit_area file")
		depositAreaFileName = "deposit_area"
		file_depositArea = open(depositAreaFileName, "w")
		file_depositArea.write("FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tvolScalarField;\n\tlocation\t\"0\";\n\tobject\tdeposit_area;\n}\n\n\
			dimensions [0 0 0 0 0 0 0];\ninternalField nonuniform List<scalar>\n%d\n(\n" % num_blocks)
		for it in np.nditer(self.blocks):
			if it != self.sd.NODATA_value:
				if it <= 0:
					file_depositArea.write("%f\n" % it)
				else:
					file_depositArea.write("%f\n" % 0.0)
		file_depositArea.write(")\n;\nboundaryField\n{\n\tslope\n\t{\n\t\ttype\t\tzeroGradient;\n\t}\n\tatmosphere\n\t{\n\
			\t\ttype\t\tinletOutlet;\n\t\tinletValue\tuniform 0;\n\t\tvalue\t\tuniform 0;\n\t}\n\tdefaultFaces\n\t{\n\t\ttype\t\tempty;\n\t}\n}\n")
		file_depositArea.close()
		print("deposit_area file is ready")

	def createOBJ(self):
		print("Creating OBJ file.")
		file_obj = open("slope.obj", "w")
		file_obj.write('g slope\n')
		alt_ind = np.zeros_like(self.sd.altitude)
		with np.nditer(self.sd.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
			while not it.finished:
				if	it[0] != self.sd.NODATA_value and\
					it.multi_index[0]+1 < self.sd.nx and\
					it.multi_index[1]+1 < self.sd.ny and\
					self.sd.altitude[it.multi_index[0]+1,it.multi_index[1]] != self.sd.NODATA_value and\
					self.sd.altitude[it.multi_index[0],it.multi_index[1]+1] != self.sd.NODATA_value and\
					self.sd.altitude[it.multi_index[0]+1,it.multi_index[1]+1] != self.sd.NODATA_value:
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
				if it[0] > -1:
					file_obj.write('v\t%f\t%f\t%f\nv\t%f\t%f\t%f\n' % (self.sd.dx * it.multi_index[0], self.sd.dx * it.multi_index[1],\
						self.sd.altitude[it.multi_index] - self.alt_min + 1, self.sd.dx * it.multi_index[0], self.sd.dx * it.multi_index[1],\
						self.sd.altitude[it.multi_index] - self.alt_min + self.height - 1))
				it.iternext()
		#with np.nditer(alt_ind, flags=['multi_index'], op_flags=['readonly']) as it:
		#	while not it.finished:
		#		if	it[0] > -1 and\
		#			it.multi_index[0]+1 < self.sd.nx and\
		#			it.multi_index[1]+1 < self.sd.ny and\
		#			alt_ind[it.multi_index[0]+1,it.multi_index[1]] != -1 and\
		#			alt_ind[it.multi_index[0],it.multi_index[1]+1] != -1 and\
		#			alt_ind[it.multi_index[0]+1,it.multi_index[1]+1] != -1:
		#				file_obj.write('f\t%d\t%d\t%d\t%d\n' % (it[0]*2+1, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*2+1,\
		#					alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*2+1, alt_ind[it.multi_index[0],it.multi_index[1]+1]*2+1))
		#				file_obj.write('f\t%d\t%d\t%d\t%d\n' % (it[0]*2+2, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*2+2,\
		#					alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*2+2, alt_ind[it.multi_index[0],it.multi_index[1]+1]*2+2))
		#				if	it.multi_index[1]-1 < 0 or\
		#					alt_ind[it.multi_index[0],it.multi_index[1]-1] == -1 or\
		#					alt_ind[it.multi_index[0]+1,it.multi_index[1]-1] == -1:
		#						file_obj.write('f\t%d\t%d\t%d\t%d\n' % (it[0]*2+1, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*2+1,\
		#							alt_ind[it.multi_index[0]+1,it.multi_index[1]]*2+2, it[0]*2+2))
		#				if	it.multi_index[0]-1 < 0 or\
		#					alt_ind[it.multi_index[0]-1,it.multi_index[1]] == -1 or\
		#					alt_ind[it.multi_index[0]-1,it.multi_index[1]+1] == -1:
		#						file_obj.write('f\t%d\t%d\t%d\t%d\n' % (it[0]*2+1, alt_ind[it.multi_index[0],it.multi_index[1]+1]*2+1,\
		#							alt_ind[it.multi_index[0],it.multi_index[1]+1]*2+2, it[0]*2+2))
		#				if	it.multi_index[1]+2 >= self.sd.ny or\
		#					alt_ind[it.multi_index[0],it.multi_index[1]+2] == -1 or\
		#					alt_ind[it.multi_index[0]+1,it.multi_index[1]+2] == -1:
		#						file_obj.write('f\t%d\t%d\t%d\t%d\n' % (alt_ind[it.multi_index[0],it.multi_index[1]+1]*2+1,\
		#							alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*2+1, alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*2+2,\
		#							alt_ind[it.multi_index[0],it.multi_index[1]+1]*2+2))
		#				if	it.multi_index[0]+2 >= self.sd.nx or\
		#					alt_ind[it.multi_index[0]+2,it.multi_index[1]] == -1 or\
		#					alt_ind[it.multi_index[0]+2,it.multi_index[1]+1] == -1:
		#						file_obj.write('f\t%d\t%d\t%d\t%d\n' % (alt_ind[it.multi_index[0]+1,it.multi_index[1]]*2+1,\
		#							alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*2+1, alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*2+2,\
		#							alt_ind[it.multi_index[0]+1,it.multi_index[1]]*2+2))
		#		it.iternext()
		with np.nditer(alt_ind, flags=['multi_index'], op_flags=['readonly']) as it:
			while not it.finished:
				if	it[0] > -1 and\
					it.multi_index[0]+1 < self.sd.nx and\
					it.multi_index[1]+1 < self.sd.ny and\
					alt_ind[it.multi_index[0]+1,it.multi_index[1]] != -1 and\
					alt_ind[it.multi_index[0],it.multi_index[1]+1] != -1 and\
					alt_ind[it.multi_index[0]+1,it.multi_index[1]+1] != -1:
						file_obj.write('f\t%d\t%d\t%d\nf\t%d\t%d\t%d\n' % (it[0]*2+1, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*2+1,\
							alt_ind[it.multi_index[0],it.multi_index[1]+1]*2+1, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*2+1,\
							alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*2+1, alt_ind[it.multi_index[0],it.multi_index[1]+1]*2+1))
						file_obj.write('f\t%d\t%d\t%d\nf\t%d\t%d\t%d\n' % (it[0]*2+2, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*2+2,\
							alt_ind[it.multi_index[0],it.multi_index[1]+1]*2+2, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*2+2,\
							alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*2+2, alt_ind[it.multi_index[0],it.multi_index[1]+1]*2+2))
						if	it.multi_index[1]-1 < 0 or\
							alt_ind[it.multi_index[0],it.multi_index[1]-1] == -1 or\
							alt_ind[it.multi_index[0]+1,it.multi_index[1]-1] == -1:
								file_obj.write('f\t%d\t%d\t%d\nf\t%d\t%d\t%d\n' % (it[0]*2+1, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*2+1, it[0]*2+2,\
									alt_ind[it.multi_index[0]+1,it.multi_index[1]]*2+1, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*2+2, it[0]*2+2))
						if	it.multi_index[0]-1 < 0 or\
							alt_ind[it.multi_index[0]-1,it.multi_index[1]] == -1 or\
							alt_ind[it.multi_index[0]-1,it.multi_index[1]+1] == -1:
								file_obj.write('f\t%d\t%d\t%d\nf\t%d\t%d\t%d\n' % (it[0]*2+1, alt_ind[it.multi_index[0],it.multi_index[1]+1]*2+1, it[0]*2+2,\
									alt_ind[it.multi_index[0],it.multi_index[1]+1]*2+1, alt_ind[it.multi_index[0],it.multi_index[1]+1]*2+2, it[0]*2+2))
						if	it.multi_index[1]+2 >= self.sd.ny or\
							alt_ind[it.multi_index[0],it.multi_index[1]+2] == -1 or\
							alt_ind[it.multi_index[0]+1,it.multi_index[1]+2] == -1:
								file_obj.write('f\t%d\t%d\t%d\nf\t%d\t%d\t%d\n' % (alt_ind[it.multi_index[0],it.multi_index[1]+1]*2+1,\
									alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*2+1, alt_ind[it.multi_index[0],it.multi_index[1]+1]*2+2,\
									alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*2+1, alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*2+2,\
									alt_ind[it.multi_index[0],it.multi_index[1]+1]*2+2))
						if	it.multi_index[0]+2 >= self.sd.nx or\
							alt_ind[it.multi_index[0]+2,it.multi_index[1]] == -1 or\
							alt_ind[it.multi_index[0]+2,it.multi_index[1]+1] == -1:
								file_obj.write('f\t%d\t%d\t%d\nf\t%d\t%d\t%d\n' % (alt_ind[it.multi_index[0]+1,it.multi_index[1]]*2+1,\
									alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*2+1, alt_ind[it.multi_index[0]+1,it.multi_index[1]]*2+2,\
									alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*2+1, alt_ind[it.multi_index[0]+1,it.multi_index[1]+1]*2+2,\
									alt_ind[it.multi_index[0]+1,it.multi_index[1]]*2+2))
				it.iternext()
		file_obj.close()
		print("OBJ file is ready")

def main():
	map_name, region_map_name = readFileNames()
	slope = asc(map_name, region_map_name)
	f = files(slope,15)
	#f.createBlockMeshDict()
	f.createBlockMeshDictInclined()
	#f.polyMesh()
	#f.createSetFieldsDict()
	#f.createAlphaWater()
	#f.createOBJ()

if __name__== "__main__":
	main()