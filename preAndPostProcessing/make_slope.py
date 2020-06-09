import numpy

print("Enter cellsize:")
cellsize = float(input())
nx = int(70. / cellsize)
ny = int(21. / cellsize)
x = numpy.linspace(0., 70., nx)
xy = numpy.tile(x,(ny,1))

def alt(x):
	if x <= 30.:
		z = - (x - 40.) / numpy.sqrt(3.)
	elif x >= 50.:
		z = 0
	else:
		z = (x - 50.)**2 / (40. * numpy.sqrt(3.))
	return z + 10

def reg(x, y):
	if 1. <= y <= 15. and 7. < x < 13.:
		f = 0
	else:
		f = -9999
	return f

valt = numpy.vectorize(alt)
altitude = valt(xy)

region = numpy.copy(xy)
with numpy.nditer(region, flags=['multi_index'], op_flags=["writeonly"]) as it:
	while not it.finished:
		it[0] = reg(it.multi_index[0] * cellsize, it.multi_index[1] * cellsize)
		it.iternext()

f = open("slope.asc", "w")
f.write("ncols         %d\n" % ny)
f.write("nrows         %d\n" % nx)
f.write("xllcorner     530200,48752344\n")
f.write("yllcorner     7503732,4955134\n")
f.write("cellsize      1\n")
f.write("NODATA_value  -9999\n")
numpy.savetxt(f, altitude.T, fmt='%f')
f.close()

f = open("slope_region.asc", "w")
f.write("ncols         %d\n" % ny)
f.write("nrows         %d\n" % nx)
f.write("xllcorner     530200,48752344\n")
f.write("yllcorner     7503732,4955134\n")
f.write("cellsize      1\n")
f.write("NODATA_value  -9999\n")
numpy.savetxt(f, region.T, fmt='%d')
f.close()

