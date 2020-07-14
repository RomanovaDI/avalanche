import numpy

print("Enter cellsize:")
cellsize = float(input())
print("Enter length:")
length = float(input())
scale = length / 70.
nx = int(70. * scale / cellsize)
ny = int(21. * scale / cellsize)
x = numpy.linspace(0., 70. * scale, nx)
xy = numpy.tile(x,(ny,1))

def alt(x, scale=1):
	if x <= 30. * scale:
		z = - (x - 40. * scale) / numpy.sqrt(3.)
	elif x >= 50. * scale:
		z = 0
	else:
		z = (x - 50. * scale)**2 / (40. * scale * numpy.sqrt(3.))
	return z + 10

def reg(x, y, scale=1):
	if 1. * scale <= y <= 15. * scale and 5. * scale <= x <= 10. * scale:
		f = 0
	else:
		f = -9999
	return f

valt = numpy.vectorize(alt)
altitude = valt(xy, scale)

region = numpy.copy(xy)
with numpy.nditer(region, flags=['multi_index'], op_flags=["writeonly"]) as it:
	while not it.finished:
		it[0] = reg(it.multi_index[0] * cellsize, it.multi_index[1] * cellsize, scale)
		it.iternext()

f = open("slope.asc", "w")
f.write("ncols         %d\n" % ny)
f.write("nrows         %d\n" % nx)
f.write("xllcorner     530200,48752344\n")
f.write("yllcorner     7503732,4955134\n")
f.write("cellsize      %lf\n" % cellsize)
f.write("NODATA_value  -9999\n")
numpy.savetxt(f, altitude.T, fmt='%f')
f.close()

f = open("slope_region.asc", "w")
f.write("ncols         %d\n" % ny)
f.write("nrows         %d\n" % nx)
f.write("xllcorner     530200,48752344\n")
f.write("yllcorner     7503732,4955134\n")
f.write("cellsize      %lf\n" % cellsize)
f.write("NODATA_value  -9999\n")
numpy.savetxt(f, region.T, fmt='%d')
f.close()

