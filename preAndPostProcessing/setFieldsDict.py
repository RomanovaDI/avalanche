import numpy as np
from scipy import interpolate
from operator import add
import math
import readAsc as ra
import sys

def createSetFields(am, rg, height = 2): #rg - region map, height - height of snow cover
	print("Creating setFieldsDict file.")
	file = open("setFieldsDict", "w")
	file.write('FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tlocation\t"system";\n\tobject\tsetFieldsDict;\n}\n')
	file.write('defaultFieldValues\n(\n\tvolScalarFieldValue alpha.water 0\n);\nregions\n(\n')
	with np.nditer(rg.region, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] == 0 and\
				am.altitude[it.multi_index] != am.NODATA_value:
				file.write('\tboxToCell\n\t{\n\t\tbox (%lf %lf %lf) (%lf %lf %lf);\n\t\tfieldValues\n\t\t(\n\t\t\tvolScalarFieldValue alpha.water 1\n\t\t);\n\t}\n' % (\
					it.multi_index[0] * am.dx, it.multi_index[1] * am.dx ,am.altitude[it.multi_index] - 1 - am.alt_min,\
					(it.multi_index[0] + 1) * am.dx, (it.multi_index[1] + 1) * am.dx, am.altitude[it.multi_index] - am.alt_min + height))
			it.iternext()
	file.write(');')
	file.close()
	print("setFieldsDict file is ready")

def createSetFieldsRotated(am, rg, height = 2): #rg - region map, height - height of snow cover
	print("Creating setFieldsDict file.")
	file = open("setFieldsDict", "w")
	file.write('FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tlocation\t"system";\n\tobject\tsetFieldsDict;\n}\n')
	file.write('defaultFieldValues\n(\n\tvolScalarFieldValue alpha.water 0\n);\nregions\n(\n')
	indent = 0
	with np.nditer(rg.region, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			vert0 = it.multi_index
			vert1 = tuple(map(add, it.multi_index, (1, 0)))
			vert2 = tuple(map(add, it.multi_index, (1, 1)))
			vert3 = tuple(map(add, it.multi_index, (0, 1)))
			if	it[0] == 0 and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				rg.region[vert1] == 0 and\
				rg.region[vert2] == 0 and\
				rg.region[vert3] == 0:
					file.write('\trotatedBoxToCell\n\t{\n\t\torigin (%f %f %f);\n\t\ti (%f %f %f);\n\t\tj (%f %f %f);\n\t\tk (%f %f %f);\n\t\tfieldValues\n\t\t(\n\t\t\tvolScalarFieldValue alpha.water 1\n\t\t);\n\t}\n' % (\
						it.multi_index[0] * am.dx, it.multi_index[1] * am.dx, am.altitude[vert0] - am.alt_min + indent,\
						am.dx, 0, am.altitude[vert1] - am.altitude[vert0],\
						0, am.dx, am.altitude[vert3] - am.altitude[vert0],\
						0, 0, height))
			it.iternext()
	file.write(');')
	file.close()
	print("setFieldsDict file is ready")

def createSetFieldsRotatedStartFinish(am, rg, height = 2): #rg - region map, height - height of snow cover
	print("Creating setFieldsDict file.")
	file = open("setFieldsDict", "w")
	file.write('FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tlocation\t"system";\n\tobject\tsetFieldsDict;\n}\n')
	file.write('defaultFieldValues\n(\n\tvolScalarFieldValue alpha.water 0\n\tvolScalarFieldValue region 0\n);\nregions\n(\n')
	indent = 0
	with np.nditer(rg.region, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			vert0 = it.multi_index
			vert1 = tuple(map(add, it.multi_index, (1, 0)))
			vert2 = tuple(map(add, it.multi_index, (1, 1)))
			vert3 = tuple(map(add, it.multi_index, (0, 1)))
			if	it[0] == 0 and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				rg.region[vert1] == 0 and\
				rg.region[vert2] == 0 and\
				rg.region[vert3] == 0:
					file.write('\trotatedBoxToCell\n\t{\n\t\torigin (%f %f %f);\n\t\ti (%f %f %f);\n\t\tj (%f %f %f);\n\t\tk (%f %f %f);\n\t\tfieldValues\n\t\t(\n\t\t\tvolScalarFieldValue alpha.water 1\n\t\t);\n\t}\n' % (\
						it.multi_index[0] * am.dx, it.multi_index[1] * am.dx, am.altitude[vert0] - am.alt_min + indent,\
						am.dx, 0, am.altitude[vert1] - am.altitude[vert0],\
						0, am.dx, am.altitude[vert3] - am.altitude[vert0],\
						0, 0, height))
			if	it[0] == 1 and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				rg.region[vert1] == 1 and\
				rg.region[vert2] == 1 and\
				rg.region[vert3] == 1:
					file.write('\trotatedBoxToCell\n\t{\n\t\torigin (%f %f %f);\n\t\ti (%f %f %f);\n\t\tj (%f %f %f);\n\t\tk (%f %f %f);\n\t\tfieldValues\n\t\t(\n\t\t\tvolScalarFieldValue region 1\n\t\t);\n\t}\n' % (\
						it.multi_index[0] * am.dx, it.multi_index[1] * am.dx, am.altitude[vert0] - am.alt_min + indent,\
						am.dx, 0, am.altitude[vert1] - am.altitude[vert0],\
						0, am.dx, am.altitude[vert3] - am.altitude[vert0],\
						0, 0, height))
			it.iternext()
	file.write(');')
	file.close()
	print("setFieldsDict file is ready")