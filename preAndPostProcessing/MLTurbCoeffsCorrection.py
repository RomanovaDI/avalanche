#import os
#os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'

#import tensorflow as tf
#import tensorflow_probability as tfp
import subprocess as sp
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import math
from multiprocessing import Pool

def readHV(fileName):
	df = pd.read_csv(fileName)
	HV = df[['Points:2', 'U:0']].to_numpy()
	HV = normalizeHV(HV)
	dfProfile = pd.DataFrame(HV)
	return dfProfile

def normalizeHV(HV):
	Hstart = HV[0,0]
	Hfinish = HV[-1,0]
	Hstep = 0.05
	H = np.arange(Hstart, Hfinish + Hstep, Hstep, dtype=float)
	V = np.interp(H, HV[:,0], HV[:,1], left=0, right=0)
	HV = np.column_stack((H, V))
	return HV

def calcMSE(dfRef, dfTmp):
	listMSE = map(calcOneMSE, [dfRef, dfTmp])
	MSE = sum(listMSE)
	return MSE

def calcOneMSE(dfRef, dfTmp):
	MSE = (dfRef['U:0'] - dfTmp['U:0'])**2
	return math.sqrt(MSE.sum())

def runOF(caseDir):
	sp.call("cd "+caseDir+";\
			bash -i of2012;\
			bash -i ./Allclean;\
			sed \"s/alphaK1_pattern/	alphaK1			"+str(coeffs[0])+";/\" constant/turbulenceProperties > tmp;\
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
			bash -i ./Allrun;\
			cd ../", shell=True)

def calcLoss(coeffs, dfRefHV, caseDirs):
	with Pool() as pool:
		pool.map(runOF, caseDirs)
	dfTmpHV = map(readHV, map(lambda e : e + "data/OutletCalcKW.csv", caseDirs))
	MSE = calcMSE(dfRefHV, dfTmpHV)
	open("log.MLTransportCoeffsCorrection", "a").write("coeffs: "+str(coeffs)+"\n")
	open("log.MLTransportCoeffsCorrection", "a").write("MSE = "+str(MSE)+"\n")
	return MSE

def minimizeSciPy(initCoeffs, bounds, referenceValue, caseDir):
	res = minimize(calcLoss, initCoeffs, args=(referenceValue, caseDir), method='Nelder-Mead', tol=1e-6, bounds=bounds)
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
	dfHVRef = map(readHV, RefFiles)
	minimizeSciPy(coeffs, bounds, dfHVRef, TurbKWCaseDirs)

if __name__ == "__main__":
	main()
