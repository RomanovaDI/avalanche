# Two unadapted parameters in code: Hstep variable and the last time step

import subprocess as sp
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import math
from multiprocessing import Pool
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

def calcMSE(dfRef, dfTmp):
	listMSE = list(map(calcOneMSE, dfRef, dfTmp))
	MSE = sum(listMSE)
	return MSE

def calcOneMSE(HVRef, HVTmp):
	URef = waterVelocityExtract(HVRef[:,1])
	UTmp = waterVelocityExtract(HVTmp[:,1])
	size = min(URef.size, UTmp.size)
	URef = URef[:size]
	UTmp = UTmp[:size]
	MSE = (URef - UTmp)**2
	return math.sqrt(MSE.sum())

def waterVelocityExtract(U):
	it = np.nditer(U, flags=['f_index'], op_flags=['readwrite'])
	for u in it:
		if (it.index > 0 and u < U[it.index-1]):
			u = 0
	return U

def runOF(caseDir, coeffs):
	sp.call("cd "+caseDir+";\
			sed \"s/alphaK1_pattern/	alphaK1			"+str(coeffs[0])+";/\" constant/turbulencePropertiesPattern > tmp;\
			mv tmp constant/turbulenceProperties;\
			sed \"s/alphaK2_pattern/	alphaK2			"+str(coeffs[1])+";/\" constant/turbulenceProperties > tmp;\
			mv tmp constant/turbulenceProperties;\
			sed \"s/alphaOmega1_pattern/	alphaOmega1			"+str(coeffs[2])+";/\" constant/turbulenceProperties > tmp;\
			mv tmp constant/turbulenceProperties;\
			sed \"s/alphaOmega2_pattern/	alphaOmega2			"+str(coeffs[3])+";/\" constant/turbulenceProperties > tmp;\
			mv tmp constant/turbulenceProperties;\
			sed \"s/beta1_pattern/	beta1		"+str(coeffs[4])+";/\" constant/turbulenceProperties > tmp;\
			mv tmp constant/turbulenceProperties;\
			sed \"s/beta2_pattern/	beta2	"+str(coeffs[5])+";/\" constant/turbulenceProperties > tmp;\
			mv tmp constant/turbulenceProperties;\
			sed \"s/betaStar_pattern/	betaStar	"+str(coeffs[6])+";/\" constant/turbulenceProperties > tmp;\
			mv tmp constant/turbulenceProperties;\
			sed \"s/gamma1_pattern/	gamma1	"+str(coeffs[7])+";/\" constant/turbulenceProperties > tmp;\
			mv tmp constant/turbulenceProperties;\
			sed \"s/gamma2_pattern/	gamma2	"+str(coeffs[8])+";/\" constant/turbulenceProperties > tmp;\
			mv tmp constant/turbulenceProperties;\
			sed \"s/a1_pattern/	a1	"+str(coeffs[9])+";/\" constant/turbulenceProperties > tmp;\
			mv tmp constant/turbulenceProperties;\
			sed \"s/b1_pattern/	b1	"+str(coeffs[10])+";/\" constant/turbulenceProperties > tmp;\
			mv tmp constant/turbulenceProperties;\
			sed \"s/c1_pattern/	c1	"+str(coeffs[11])+";/\" constant/turbulenceProperties > tmp;\
			mv tmp constant/turbulenceProperties;\
			./Allclean;\
			sbatch -n8 -W -o log.sbatch Allrun;\
			cd ../", shell=True)

def calcLoss(coeffs, dfRefHV, caseDirs):
	with Pool() as pool:
		pool.map(partial(runOF, coeffs=coeffs), caseDirs)
	dfTmpHV = list(map(readHVPostProc, list(map(lambda e : e + "postProcessing/singleGraph/0.5/line_U.xy", caseDirs))))
	MSE = calcMSE(dfRefHV, dfTmpHV)
	open("log.MLTransportCoeffsCorrection", "a").write("coeffs: "+str(coeffs)+"\n")
	open("log.MLTransportCoeffsCorrection", "a").write("MSE = "+str(MSE)+"\n")
	return MSE

def minimizeSciPy(initCoeffs, bounds, referenceValue, caseDir):
	res = minimize(calcLoss, initCoeffs, args=(referenceValue, caseDir), method='Nelder-Mead', tol=1e-6)#, bounds=bounds)
	print(res.x)

def main():
	bounds = [[0.5, 1.0], [0.5, 2.5], [0.2, 0.8], [0.7, 1.0], [0.0, 0.15], [0.0, 0.15], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.5, 1.5], [5.0, 15.0]]
	coeffs = [0.85, 1.0, 0.5, 0.856, 0.075, 0.0828, 0.09, 0.5555556, 0.44, 0.31, 1.0, 10.0]
#	coeffs = [0.09]
	RefFiles = ("constantAngleSlopeTurbKWUProfileInlet180321/data/180321OutletSmoothProfile.csv",
				"constantAngleSlopeTurbKWUProfileInlet230421/data/230421OutletSmoothProfile.csv",
				"constantAngleSlopeTurbKWUProfileInlet100621/data/100621OutletSmoothProfile.csv")
	TurbKWCaseDirs = ("constantAngleSlopeTurbKWUProfileInlet180321/",
				"constantAngleSlopeTurbKWUProfileInlet230421/",
				"constantAngleSlopeTurbKWUProfileInlet100621/")
	dfHVRef = list(map(readHV, RefFiles))
	minimizeSciPy(coeffs, bounds, dfHVRef, TurbKWCaseDirs)

if __name__ == "__main__":
	main()
