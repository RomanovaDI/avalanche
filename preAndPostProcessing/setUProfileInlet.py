import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dfInlet = pd.read_csv('inlet.txt', delimiter="\t", header=None)
dfOutlet = pd.read_csv('outlet.txt', delimiter="\t", header=None)
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
Ztmp = dfInlet[0].to_numpy()
Zstart = 0.0
Zfinish = 10.0
Zstep = 0.25
Z = np.arange(Zstart, Zfinish + Zstep, Zstep, dtype=float)
Vtmp = dfInlet[1].to_numpy()
V = np.interp(Z, Ztmp, Vtmp, left=0, right=0)
#plt.plot(Vtmp, Ztmp, label="real")
#plt.plot(V, Z, label="interp")
#plt.show()
fU = open("constant/boundary/leftInletWall/0/U", "w")
fPoints = open("constant/boundary/leftInletWall/points", "w")
Ystart = 0.0
Yfinish = 0.005
Ystep = 0.0005
Y = np.arange(Ystart, Yfinish + Ystep, Ystep)
nPoints = Y.shape * Z.shape + 1
fU.write("%d\n(\n\t(0.0\t0.0\t0.0)\n" % (nPoints))
fPoints.write("%d\n(\n\t(0.0\t%f\t0.0)\n" % (nPoints, Y[1]))
for y in Y:
	if y = Y[0]:
		fU.write(("\t(0.0\t0.0\t0.0)\n") * Z.shape)
	else if y = Y[-1]:
		fU.write(("\t(0.0\t0.0\t0.0)\n") * Z.shape)
	else:
		for v in V:
			fU.write("\t(%f\t0.0\t0.0)\n" % (v))
	for z in Z:
		fPoints.write("\t(0.0\t%f\t%f)\n" % (y, z))
fPoints.write(")")
fU.write(")")
fPoints.close()
fU.close()
