import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dfInlet = pd.read_csv('data/180321InletSmoothProfile.csv', delimiter="\t", header=None)
HAlphaWater = 0
with open('data/180321H.dat') as file:
	HAlphaWater = float(file.read())
#dfOutlet = pd.read_csv('180321_outlet.csv', delimiter="\t", header=None)
#X = dfInlet[0].to_numpy()
#A = X.reshape((1, np.size(X)))
#A = np.repeat(A, np.size(X), axis=0)
#A = np.power(np.transpose(A), np.arange(np.size(X)))
#B = dfInlet[1].to_numpy()
#W = np.linalg.solve(A, B)
#Xtest = np.linspace(0.0, 10.0, num=100)
#Htest = Xtest.reshape((1,np.size(Xtest)))
#Htest = np.repeat(Htest, np.size(X), axis=0)
#Htest = np.power(np.transpose(Htest), np.arange(np.size(X)))
#Htest = Htest.dot(W)
#plt.plot(X, B, label="experiment")
#plt.plot(Xtest, Htest, label="approximation")
#plt.show()
Z = dfInlet[0].to_numpy()
V = dfInlet[1].to_numpy()
#plt.plot(Vtmp, Ztmp, label="real")
#plt.plot(V, Z, label="interp")
#plt.show()
fU = open("constant/boundaryData/leftInletWall/0/U", "w")
fAlphaWater = open("constant/boundaryData/leftInletWall/0/alpha.water.orig", "w")
fPoints = open("constant/boundaryData/leftInletWall/points", "w")
Ystart = 0.0
Yfinish = 0.005
Ystep = 0.0005
Y = np.arange(Ystart, Yfinish + Ystep, Ystep)
nPoints = Y.shape[0] * Z.shape[0] + 1
fU.write("%d\n(\n\t(0.0\t0.0\t0.0)\n" % (nPoints))
fPoints.write("%d\n(\n\t(0.0\t%f\t0.0)\n" % (nPoints, Y[1]))
fAlphaWater.write("%d\n(\n\t1.0\n" % (nPoints))
for y in Y:
	if y == Y[0]:
		fU.write(("\t(0.0\t0.0\t0.0)\n") * Z.shape[0])
	elif y == Y[-1]:
		fU.write(("\t(0.0\t0.0\t0.0)\n") * Z.shape[0])
	else:
		for v in V:
			fU.write("\t(%f\t0.0\t0.0)\n" % (v))
	for z in Z:
		fPoints.write("\t(0.0\t%f\t%f)\n" % (y, z*0.001))
		if z <= HAlphaWater:
			fAlphaWater.write("\t%f\n" % (1.0))
		else:
			fAlphaWater.write("\t%f\n" % (0.0))
fPoints.write(")")
fU.write(")")
fAlphaWater.write(")")
fPoints.close()
fU.close()
fAlphaWater.close()
