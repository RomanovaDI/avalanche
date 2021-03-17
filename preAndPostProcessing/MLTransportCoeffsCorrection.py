import os
import subprocess as sp
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import math

def readAlphaWaterLoss(caseDir):
	finishAreaFile = caseDir+"/postProcessing/finishAreaIntegrateAlphaWater/0/volFieldValue.dat"
	calculationAreaFile = caseDir+"/postProcessing/calculationAreaIntegrateAlphaWater/0/volFieldValue.dat"
	finishAreaIntegrateAlphaWater = pd.read_table(finishAreaFile, header=3)
	calculationAreaIntegrateAlphaWater = pd.read_table(calculationAreaFile, header=3)
	print(finishAreaIntegrateAlphaWater)
	print(calculationAreaIntegrateAlphaWater)
	alphaWaterInFinishArea = finishAreaIntegrateAlphaWater.iloc[-1,1]
	alphaWaterInCalculationAreaAtStart = calculationAreaIntegrateAlphaWater.iloc[0,1]
	alphaWaterInCalculationAreaAtFinish = calculationAreaIntegrateAlphaWater.iloc[-1,1]
	print(alphaWaterInCalculationAreaAtStart)
	print(alphaWaterInCalculationAreaAtFinish)
	print(alphaWaterInFinishArea)
	loss = alphaWaterInCalculationAreaAtStart * 2 - alphaWaterInCalculationAreaAtFinish - alphaWaterInFinishArea
	print(loss)
	return loss

def calcLoss(coeffs, caseDir):
	sp.call("rm -rf "+caseDir+";\
			cp -r "+caseDir+"_orig "+caseDir+";\
			cd "+caseDir+";\
			bash -i of1912;\
			sed \"s/n_pattern/	n		[0 0 0 0 0 0 0]	"+str(coeffs[0])+";/\" constant/transportProperties > tmp;\
			mv tmp constant/transportProperties;\
			sed \"s/k_pattern/	k		[0 2 -1 0 0 0 0]	"+str(coeffs[1])+";/\" constant/transportProperties > tmp;\
			mv tmp constant/transportProperties;\
			sed \"s/tau0_pattern/	tau0		[0 2 -2 0 0 0 0]	"+str(coeffs[2])+";/\" constant/transportProperties > tmp;\
			mv tmp constant/transportProperties;\
			sed \"s/nu0_pattern/	nu0		[0 2 -1 0 0 0 0]	"+str(coeffs[3])+";/\" constant/transportProperties > tmp;\
			mv tmp constant/transportProperties;\
			sed \"s/rho_pattern/	rho		[1 -3 0 0 0 0 0]	"+str(coeffs[4])+";/\" constant/transportProperties > tmp;\
			mv tmp constant/transportProperties;\
			bash -i ./Allrun;\
			cd ../", shell=True)
	loss = readAlphaWaterLoss(caseDir)
	print(loss)
	print(coeffs)
	return loss

def minimizeSciPy(initCoeffs, caseDir):
	res = minimize(calcLoss, initCoeffs, args=(caseDir), method='Nelder-Mead', tol=1e-6)
	print(res.x)

def main():
	coeffs = [0.7, 4.0, 9.0, 1.0e07, 200.0]
#	coeffs = [0.09]
	caseDir = "blockMesh_setFields"
	minimizeSciPy(coeffs, caseDir)

if __name__ == "__main__":
	main()
