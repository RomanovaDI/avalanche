import numpy as np
from scipy import interpolate
from operator import add
import math
import readAsc as ra

def createSetFields(am, rg, height = 2): #rg - region map, height - height of snow cover
	print("Creating setFieldsDict file.")
	file = open("setFieldsDict", "w")
	file.write('FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tlocation\t"system";\n\tobject\tsetFieldsDict;\n}')
	file.write('defaultFieldValues\n(\n\tvolScalarFieldValue alpha.water 0\n);\nregions\n(\n')
	with np.nditer(rg.region, flags=['multi_index'], op_flags=['readonly']) as it:
		while not it.finished:
			if	it[0] == 0 and\
				am.altitude[it.multi_index] != am.NODATA_value:
				file.write('\tboxToCell\n\t{\n\t\tbox (%lf %lf %lf) (%lf %lf %lf);\n\t\tfieldValues\n\t\t(\n\t\t\tvolScalarFieldValue alpha.water 1\n\t\t);\n\t}' % (\
					it.multi_index[0] * am.dx, it.multi_index[1] * am.dx ,am.altitude[it.multi_index],\
					(it.multi_index[0] + 1) * am.dx, (it.multi_index[1] + 1) * am.dx, am.altitude[it.multi_index] + height))
			it.iternext()
	file.write(');')
	file.close()
	print("setFieldsDict file is ready")

def main():
	map_name, region_map_name = ra.readFileNames()
	slope = ra.asc(map_name, region_map_name)
	createSetFields(slope.am, slope.rg, 2)

if __name__== "__main__":
	main()