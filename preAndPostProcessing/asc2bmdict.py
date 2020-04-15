import numpy as np
from scipy import interpolate
from operator import add
import math
import readAsc as ra

class BMDarr:
	def __init__(self, vertices, blocks, nx, ny, nz, dx):
		self.vertices = vertices
		self.blocks = blocks
		self.nx = nx
		self.ny = ny
		self.nz = nz
		self.dx = dx

def prepareSlopeData(am, height):
	f = lambda a: math.floor(a / am.dx) * am.dx if a != am.NODATA_value else am.NODATA_value
	fv = np.vectorize(f)
	altitude = np.copy(am.altitude)
	altitude = fv(altitude)
	height = math.floor(height / am.dx) * am.dx
	nz = int((am.alt_max - am.alt_min + height) / am.dx)
	vertices = np.full((am.nx + 1, am.ny + 1, nz + 1), -1, dtype=np.int32)
	blocks = np.zeros((am.nx, am.ny, nz), dtype=np.float32)
	with np.nditer(altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if it[0] != am.NODATA_value:
				for z in range(int((it[0] - am.alt_min) / am.dx), int((it[0] - am.alt_min + height) / am.dx) + 1):
					vertices[it.multi_index[0], it.multi_index[1], z] = 1
					vertices[it.multi_index[0] + 1, it.multi_index[1], z] = 1
					vertices[it.multi_index[0], it.multi_index[1] + 1, z] = 1
					vertices[it.multi_index[0] + 1, it.multi_index[1] + 1, z] = 1
				for z in range(int((it[0] - am.alt_min) / am.dx), int((it[0] - am.alt_min + height) / am.dx)):
					blocks[it.multi_index[0], it.multi_index[1], z] = 1
				blocks[it.multi_index[0], it.multi_index[1], int((it[0] - am.alt_min) / am.dx)] = 2
			it.iternext()
	ind = 0
	for it in np.nditer(vertices, op_flags=['readwrite']):
		if it == 1:
			it[...] = ind
			ind += 1
	#self.blocks_ind = np.copy(self.blocks)
	#ind = 0;
	#for it in np.nditer(self.blocks_ind, op_flags=['readwrite']):
	#	if it != 0:
	#		it[...] = ind
	#		ind += 1
	#self.n_blocks = ind
	#self.n_vertices = (self.vertices != -1).sum()
	return BMDarr(vertices, blocks, am.nx, am.ny, nz, am.dx)

def createBlockMeshDict(am, height = 16):
	ba = prepareSlopeData(am, height) # blockMeshDict array
	print("Creating blockMeshDict file")
	blockMeshDictFileName = "blockMeshDict"
	file_blockMeshDict = open(blockMeshDictFileName, "w")
	file_blockMeshDict.write("FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tobject\tblockMeshDict;\n}\n\nconvertToMeters 1.0;\n\n")
	file_blockMeshDict.write("vertices\n(\n")
	with np.nditer(ba.vertices, flags=['multi_index'], op_flags=["readonly"]) as it:
		while not it.finished:
			if it[0] != -1:
				file_blockMeshDict.write("\t(%f\t%f\t%f)\n" % (it.multi_index[0] * ba.dx, it.multi_index[1] * ba.dx, it.multi_index[2] * ba.dx))
			it.iternext()
	file_blockMeshDict.write(");\n\nblocks\n(\n")
	with np.nditer(ba.blocks, flags=['multi_index'], op_flags=["readonly"]) as it:
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
					(ba.vertices[vert0], ba.vertices[vert1], ba.vertices[vert2], ba.vertices[vert3], ba.vertices[vert4],\
					ba.vertices[vert5], ba.vertices[vert6], ba.vertices[vert7]))
			it.iternext()
	file_blockMeshDict.write(");\n\nedges\n(\n);\n\nboundary\n(\n\tslope\n\t{\n\t\ttype wall;\n\t\tfaces\n\t\t(\n")
	with np.nditer(ba.blocks, flags=['multi_index'], op_flags=["readonly"]) as it:
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
				file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (ba.vertices[vert3], ba.vertices[vert2], ba.vertices[vert1], ba.vertices[vert0]))
				neighbour_ind = tuple(map(add, it.multi_index, (-1, 0, 0)))
				if neighbour_ind[0] < 0 or ba.blocks[neighbour_ind] == 0:
					file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (ba.vertices[vert0], ba.vertices[vert4], ba.vertices[vert7], ba.vertices[vert3]))
				neighbour_ind = tuple(map(add, it.multi_index, (1, 0, 0)))
				if neighbour_ind[0] >= ba.nx or ba.blocks[neighbour_ind] == 0:
					file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (ba.vertices[vert1], ba.vertices[vert2], ba.vertices[vert6], ba.vertices[vert5]))
				neighbour_ind = tuple(map(add, it.multi_index, (0, -1, 0)))
				if neighbour_ind[1] < 0 or ba.blocks[neighbour_ind] == 0:
					file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (ba.vertices[vert0], ba.vertices[vert1], ba.vertices[vert5], ba.vertices[vert4]))
				neighbour_ind = tuple(map(add, it.multi_index, (0, 1, 0)))
				if neighbour_ind[1] >= ba.ny or ba.blocks[neighbour_ind] == 0:
					file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (ba.vertices[vert2], ba.vertices[vert3], ba.vertices[vert7], ba.vertices[vert6]))
				neighbour_ind = tuple(map(add, it.multi_index, (0, 0, 1)))
				if neighbour_ind[2] >= ba.nz or ba.blocks[neighbour_ind] == 0:
					file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (ba.vertices[vert4], ba.vertices[vert5], ba.vertices[vert6], ba.vertices[vert7]))
			it.iternext()
	file_blockMeshDict.write("\t\t);\n\t}\n\tatmosphere\n\t{\n\t\ttype patch;\n\t\tfaces\n\t\t(\n")
	with np.nditer(ba.blocks, flags=['multi_index'], op_flags=["readonly"]) as it:
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
				if neighbour_ind[0] < 0 or ba.blocks[neighbour_ind] == 0:
					file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (ba.vertices[vert0], ba.vertices[vert4], ba.vertices[vert7], ba.vertices[vert3]))
				neighbour_ind = tuple(map(add, it.multi_index, (1, 0, 0)))
				if neighbour_ind[0] >= ba.nx or ba.blocks[neighbour_ind] == 0:
					file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (ba.vertices[vert1], ba.vertices[vert2], ba.vertices[vert6], ba.vertices[vert5]))
				neighbour_ind = tuple(map(add, it.multi_index, (0, -1, 0)))
				if neighbour_ind[1] < 0 or ba.blocks[neighbour_ind] == 0:
					file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (ba.vertices[vert0], ba.vertices[vert1], ba.vertices[vert5], ba.vertices[vert4]))
				neighbour_ind = tuple(map(add, it.multi_index, (0, 1, 0)))
				if neighbour_ind[1] >= ba.ny or ba.blocks[neighbour_ind] == 0:
					file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (ba.vertices[vert2], ba.vertices[vert3], ba.vertices[vert7], ba.vertices[vert6]))
				neighbour_ind = tuple(map(add, it.multi_index, (0, 0, 1)))
				if neighbour_ind[2] >= ba.nz or ba.blocks[neighbour_ind] == 0:
					file_blockMeshDict.write("\t\t\t(%d %d %d %d)\n" % (ba.vertices[vert4], ba.vertices[vert5], ba.vertices[vert6], ba.vertices[vert7]))
			it.iternext()
	file_blockMeshDict.write("\t\t);\n\t}\n);\n\nmergePatchPairs\n(\n);\n")
	file_blockMeshDict.close()
	print("blockMeshDict file is ready")

def main():
	map_name, region_map_name = ra.readFileNames()
	slope = ra.asc(map_name, region_map_name)
	createBlockMeshDict(slope.am, 20)

if __name__== "__main__":
	main()