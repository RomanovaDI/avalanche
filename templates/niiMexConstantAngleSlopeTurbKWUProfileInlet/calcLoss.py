import subprocess as sp
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import math
from functools import partial

def readHV(fileName):
	df = pd.read_csv(fileName, sep='\t', header=None)
	HV = df.to_numpy()
	HV = normalizeHV(HV)
	return HV

def readHVPostProc(fileName):
	df = pd.read_csv(fileName, sep='\t', header=None)
	HV = df.iloc[:, [0,1]].to_numpy()
	HV = normalizeHV(HV)
	return HV

def normalizeHV(HV):
	Hstart = HV[0,0]
	Hfinish = HV[-1,0]
	Hstep = 0.0001
	H = np.arange(Hstart, Hfinish + Hstep, Hstep, dtype=float)
	V = np.interp(H, HV[:,0], HV[:,1], left=0, right=0)
	HV = np.column_stack((H, V))
	return HV

def calcOneRMSE(HVRef, HVTmp):
	URef = waterVelocityExtract(HVRef[:,1])
	UTmp = waterVelocityExtract(HVTmp[:,1])
	size = min(URef.size, UTmp.size)
	URef = URef[:size]
	UTmp = UTmp[:size]
	RMSE = (URef - UTmp)**2
	RMSE =  math.sqrt(RMSE.sum() / size)
	return RMSE

def waterVelocityExtract(U):
	it = np.nditer(U, flags=['f_index'], op_flags=['readwrite'])
	for u in it:
		if (it.index > 0 and u < U[it.index-1]):
			u = 0
	return U

def main():
	bounds = [[0.5, 1.0], [0.5, 2.5], [0.2, 0.8], [0.7, 1.0], [0.0, 0.15], [0.0, 0.15], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.5, 1.5], [5.0, 15.0]]
	coeffs = [0.85, 1.0, 0.5, 0.856, 0.075, 0.0828, 0.09, 0.5555556, 0.44, 0.31, 1.0, 10.0]
#	coeffs = [0.09]
	refFile = ("data/180321OutletSmoothProfile.csv")
	turbFile = ("postProcessing/singleGraph/0.5/line_U.xy")
	dfHVRef = readHV(refFile)
	dfHVPostProc = readHVPostProc(turbFile)
	RMSE = calcOneRMSE(dfHVRef, dfHVPostProc)
	open("data/loss", "w").write(str(RMSE))

if __name__ == "__main__":
	main()
