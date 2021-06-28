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

def createSetFieldsFourPhases(am, rg, height = 2): #rg - region map, height - height of snow cover
	print("Creating setFieldsDict file.")
	file = open("setFieldsDict", "w")
	file.write('FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tlocation\t"system";\n\tobject\tsetFieldsDict;\n}\n')
	file.write('defaultFieldValues\n(\n\tvolScalarFieldValue alpha.air 1\n\tvolScalarFieldValue alpha.water 0\n\tvolScalarFieldValue alpha.oil 0\n\tvolScalarFieldValue alpha.mercury 0\n\tvolVectorFieldValue U (0 0 0)\n);\nregions\n(\n')
	with np.nditer(rg.region, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] == 0 and\
				am.altitude[it.multi_index] != am.NODATA_value:
				file.write('\tboxToCell\n\t{\n\t\tbox (%lf %lf %lf) (%lf %lf %lf);\n\t\tfieldValues\n\t\t(\n\t\t\tvolScalarFieldValue alpha.water 1\n\t\t\tvolScalarFieldValue alpha.oil 0\n\t\t\tvolScalarFieldValue alpha.mercury 0\n\t\t\tvolScalarFieldValue alpha.air 0\n\t\t);\n\t}\n' % (\
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
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				rg.region[vert1] != am.NODATA_value and\
				rg.region[vert2] != am.NODATA_value and\
				rg.region[vert3] != am.NODATA_value:
					file.write('\trotatedBoxToCell\n\t{\n\t\torigin (%f %f %f);\n\t\ti (%f %f %f);\n\t\tj (%f %f %f);\n\t\tk (%f %f %f);\n\t\tfieldValues\n\t\t(\n\t\t\tvolScalarFieldValue alpha.water 1\n\t\t);\n\t}\n' % (\
						it.multi_index[0] * am.dx, it.multi_index[1] * am.dx, am.altitude[vert0] - am.alt_min + indent,\
						am.dx, 0, am.altitude[vert1] - am.altitude[vert0],\
						0, am.dx, am.altitude[vert3] - am.altitude[vert0],\
						0, 0, height))
			it.iternext()
	file.write(');')
	file.close()
	print("setFieldsDict file is ready")

def createSetFieldsRotatedHeight(am, rg): #rg - region map, height - height of snow cover
	print("Creating setFieldsDict file.")
	file = open("setFieldsDict", "w")
	file.write('FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tlocation\t"system";\n\tobject\tsetFieldsDict;\n}\n')
	file.write('defaultFieldValues\n(\n\tvolScalarFieldValue alpha.water 0\n);\nregions\n(\n')
	indent = 0
	height = 0
	with np.nditer(rg.region, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			vert0 = it.multi_index
			vert1 = tuple(map(add, it.multi_index, (1, 0)))
			vert2 = tuple(map(add, it.multi_index, (1, 1)))
			vert3 = tuple(map(add, it.multi_index, (0, 1)))
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				rg.region[vert1] != am.NODATA_value and\
				rg.region[vert2] != am.NODATA_value and\
				rg.region[vert3] != am.NODATA_value:
					if height == 0:
						height = it[0]
					file.write('\trotatedBoxToCell\n\t{\n\t\torigin (%f %f %f);\n\t\ti (%f %f %f);\n\t\tj (%f %f %f);\n\t\tk (%f %f %f);\n\t\tfieldValues\n\t\t(\n\t\t\tvolScalarFieldValue alpha.water 1\n\t\t);\n\t}\n' % (\
						it.multi_index[0] * am.dx, it.multi_index[1] * am.dx, am.altitude[vert0] - am.alt_min + indent,\
						am.dx, 0, am.altitude[vert1] - am.altitude[vert0],\
						0, am.dx, am.altitude[vert3] - am.altitude[vert0],\
						0, 0, height))
			it.iternext()
	file.write(');')
	file.close()
	print("setFieldsDict file is ready")

def createSetFieldsFourPhasesRotated(am, rg, height = 2): #rg - region map, height - height of snow cover
	print("Creating setFieldsDict file.")
	file = open("setFieldsDict", "w")
	file.write('FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tlocation\t"system";\n\tobject\tsetFieldsDict;\n}\n')
	file.write('defaultFieldValues\n(\n\tvolScalarFieldValue alpha.air 1\n\tvolScalarFieldValue alpha.water 0\n\tvolScalarFieldValue alpha.oil 0\n\tvolScalarFieldValue alpha.mercury 0\n\tvolVectorFieldValue U (0 0 0)\n);\nregions\n(\n')
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
					file.write('\trotatedBoxToCell\n\t{\n\t\torigin (%f %f %f);\n\t\ti (%f %f %f);\n\t\tj (%f %f %f);\n\t\tk (%f %f %f);\n\t\tfieldValues\n\t\t(\n\t\t\tvolScalarFieldValue alpha.water 1\n\t\t\tvolScalarFieldValue alpha.oil 0\n\t\t\tvolScalarFieldValue alpha.mercury 0\n\t\t\tvolScalarFieldValue alpha.air 0\n\t\t);\n\t}\n' % (\
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


def createInitialFields(am, rg, height = 0.5): #rg - region map, height - height of snow cover
	print("Creating initial fields files.")
	#np.savetxt('tmp.out', rg.region)
	number = 0
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]] != am.NODATA_value and\
				am.altitude[it.multi_index[0],it.multi_index[1]+1] != am.NODATA_value and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]+1] != am.NODATA_value:
					number += 1
			it.iternext()
	file = open("h", "w")
	file.write('FoamFile\n{\n\tversion\t2.0;\n\t format\tascii;\n\tclass\tareaScalarField;\n\tlocation\t"0";\n\tobject\th;\n}\n')
	file.write('dimensions\t[0 1 0 0 0 0 0];\ninternalField\tnonuniform List<scalar>\n')
	file.write('%d\n(\n' % (number))
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]] != am.NODATA_value and\
				am.altitude[it.multi_index[0],it.multi_index[1]+1] != am.NODATA_value and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]+1] != am.NODATA_value:
				value = height if rg.region[it.multi_index] == 0 else 0
				file.write('%lf\n' % (value))
			it.iternext()
	file.write(')\n;\n')
	file.write('boundaryField\n{\n\tsides\n\t{\n\t\ttype\t\tinletOutlet;\n\t\tphi\t\tphis;\n\t\tinletValue\t\tuniform 0;\n\t\tvalue\t\tuniform 0;\n\t}\n}\n')
	file.close()
	file = open("H", "w")
	file.write('FoamFile\n{\n\tversion\t2.0;\n\t format\tascii;\n\tclass\tareaScalarField;\n\tlocation\t"0";\n\tobject\th;\n}\n')
	file.write('dimensions\t[0 1 0 0 0 0 0];\ninternalField\tuniform 0;\n')
	file.write('boundaryField\n{\n\tsides\n\t{\n\t\ttype\t\tcalculated;\n\t\tvalue\t\tuniform 0;\n\t}\n')
	file.write('\tslope\n\t{\n\t\ttype\t\tcalculated;\n\t\tvalue\t\tnonuniform List<scalar>\n')
	file.write('%d\n(\n' % (number))
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]] != am.NODATA_value and\
				am.altitude[it.multi_index[0],it.multi_index[1]+1] != am.NODATA_value and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]+1] != am.NODATA_value:
				value = height if rg.region[it.multi_index] == 0 else 0
				file.write('%lf\n' % (value))
			it.iternext()
	file.write(')\n;\n\t}\n')
	file.write('\tatmosphere\n\t{\n\t\ttype\t\tcalculated;\n\t\tvalue\t\tuniform 0;\n\t}\n}\n')
	file.close()
	file = open("Us", "w")
	file.write('FoamFile\n{\n\tversion\t2.0;\n\t format\tascii;\n\tclass\tareaVectorField;\n\tlocation\t"0";\n\tobject\tUs;\n}\n')
	file.write('dimensions\t[0 1 -1 0 0 0 0];\ninternalField\tuniform (0 0 0);\n')
	file.write('boundaryField\n{\n\tsides\n\t{\n\t\ttype\t\tinletOutlet;\n\t\tphi\t\tphis;\n\t\tinletValue\t\tuniform (0 0 0);\n\t\tvalue\t\tuniform (0 0 0);\n\t}\n}\n')
	file.close()
	print("Initial fields files are ready")

def createInitialFields2012(am, rg, height = 0.5): #rg - region map, height - height of snow cover
	print("Creating initial fields files.")
	#np.savetxt('tmp.out', rg.region)
	number = 0
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]] != am.NODATA_value and\
				am.altitude[it.multi_index[0],it.multi_index[1]+1] != am.NODATA_value and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]+1] != am.NODATA_value:
					number += 1
			it.iternext()
	file = open("h", "w")
	file.write('FoamFile\n{\n\tversion\t2.0;\n\t format\tascii;\n\tclass\tareaScalarField;\n\tlocation\t"0";\n\tobject\th;\n}\n')
	file.write('dimensions\t[0 1 0 0 0 0 0];\ninternalField\tnonuniform List<scalar>\n')
	file.write('%d\n(\n' % (number))
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]] != am.NODATA_value and\
				am.altitude[it.multi_index[0],it.multi_index[1]+1] != am.NODATA_value and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]+1] != am.NODATA_value:
				value = height if rg.region[it.multi_index] == 0 else 0
				file.write('%lf\n' % (value))
			it.iternext()
	file.write(')\n;\n')
	file.write('boundaryField\n{\n\tsides\n\t{\n\t\ttype\t\tinletOutlet;\n\t\tphi\t\tphis;\n\t\tinletValue\t\tuniform 0;\n\t\tvalue\t\tuniform 0;\n\t}\n}\n')
	file.close()
	file = open("H", "w")
	file.write('FoamFile\n{\n\tversion\t2.0;\n\t format\tascii;\n\tclass\tvolScalarField;\n\tlocation\t"0";\n\tobject\tH;\n}\n')
	file.write('dimensions\t[0 1 0 0 0 0 0];\ninternalField\tuniform 0;\n')
	file.write('boundaryField\n{\n\tsides\n\t{\n\t\ttype\t\tcalculated;\n\t\tvalue\t\tuniform 0;\n\t}\n')
	file.write('\tslope\n\t{\n\t\ttype\t\tcalculated;\n\t\tvalue\t\tnonuniform List<scalar>\n')
	file.write('%d\n(\n' % (number))
	with np.nditer(am.altitude, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] != am.NODATA_value and\
				it.multi_index[0]+1 < am.nx and\
				it.multi_index[1]+1 < am.ny and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]] != am.NODATA_value and\
				am.altitude[it.multi_index[0],it.multi_index[1]+1] != am.NODATA_value and\
				am.altitude[it.multi_index[0]+1,it.multi_index[1]+1] != am.NODATA_value:
				value = height if rg.region[it.multi_index] == 0 else 0
				file.write('%lf\n' % (value))
			it.iternext()
	file.write(')\n;\n\t}\n')
	file.write('\tatmosphere\n\t{\n\t\ttype\t\tcalculated;\n\t\tvalue\t\tuniform 0;\n\t}\n}\n')
	file.close()
	print("Initial fields files are ready")

def createReleaseArea(am, rg, height = 2):#rg - region map, height - height of snow cover
	print("Creating releaseArea file")
	file = open("releaseArea", "w")
	file.write('FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tlocation\t"system";\n\tobject\treleaseArea;\n}')
	file.write('fields\n(\n\th\n\t{\n\t\tdefault 0;\n\t\tregions\n\t\t(')
	file.write('\t\t\treleaseArea1\n\t\t\t{\n\t\t\t\ttype polygon;\n\t\t\t\toffset (0 0 0);\n\t\t\t\tvertices\n\t\t\t\t(')
	for i in range(2, contour_num+2):
		with np.nditer(contour, flags=['multi_index'], op_flags=['readwrite']) as it:
			while not it.finished:
				if	it[0] == i:
					file.write('\t\t\t\t\t(%lf\t%lf\t0)' % (it.multi_index[0] * rg.dx, it.multi_index[1] * rg.dx))
					break
			it.iternext()
	file.write('\t\t\t\tvalue %d0.5;\n\t\t\t}' % (height))
	file.write('\t\t);\n\t}\n);')
	file.close()
	print("releaseArea file is ready")

def createTopoSetRotatedStartFinish(am, rg, height = 20): #rg - region map, height - height of calculation domain
	print("Creating topoSetDict file.")
	file = open("topoSetDict", "w")
	file.write('FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tlocation\t"system";\n\tobject\ttopoSetDict;\n}\n')
	file.write('actions\n(\n')
	indent = 0
	startAreaFirstEntryFlag = 1
	finishAreaFirstEntryFlag = 1
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
					if startAreaFirstEntryFlag == 1:
						file.write('\t{\n\t\tname\t\tstartArea;\n\t\ttype\t\tcellSet;\n\t\taction\t\tnew;\n')
						startAreaFirstEntryFlag = 0
					else:
						file.write('\t{\n\t\tname\t\tstartArea;\n\t\ttype\t\tcellSet;\n\t\taction\t\tadd;\n')
					file.write('\t\tsource\t\trotatedBoxToCell;\n\t\torigin (%f %f %f);\n\t\ti (%f %f %f);\n\t\tj (%f %f %f);\n\t\tk (%f %f %f);\n\t}\n' % (\
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
					if finishAreaFirstEntryFlag == 1:
						file.write('\t{\n\t\tname\t\tfinishArea;\n\t\ttype\t\tcellSet;\n\t\taction\t\tnew;\n')
						finishAreaFirstEntryFlag = 0
					else:
						file.write('\t{\n\t\tname\t\tfinishArea;\n\t\ttype\t\tcellSet;\n\t\taction\t\tadd;\n')
					file.write('\t\tsource\t\trotatedBoxToCell;\n\t\torigin (%f %f %f);\n\t\ti (%f %f %f);\n\t\tj (%f %f %f);\n\t\tk (%f %f %f);\n\t}\n' % (\
						it.multi_index[0] * am.dx, it.multi_index[1] * am.dx, am.altitude[vert0] - am.alt_min + indent,\
						am.dx, 0, am.altitude[vert1] - am.altitude[vert0],\
						0, am.dx, am.altitude[vert3] - am.altitude[vert0],\
						0, 0, height))
			it.iternext()
	file.write(');')
	file.close()
	print("topoSetDict file is ready")
