import os
import subprocess as sp
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import math

def readAlphaWaterLoss(caseDir):
	finishAreaFile = caseDir+"/postProcessing/finishAreaIntegrateAlphaWater/0/volFieldValue.dat"
	calculationAreaFile = caseDir+"/postProcessing/calculationAreaIntegrateAlphaWater/0/volFieldValue.dat"
	calculationAreaVelocityFile = caseDir+"/postProcessing/calculationAreaMaxVelocity/0/volFieldValue.dat"
	finishAreaIntegrateAlphaWater = pd.read_table(finishAreaFile, header=3)
	calculationAreaIntegrateAlphaWater = pd.read_table(calculationAreaFile, header=3)
	calculationAreaMaxVelocity = pd.read_table(calculationAreaVelocityFile, header=3)
	alphaWaterInFinishArea = finishAreaIntegrateAlphaWater.iloc[-1,1]
	alphaWaterInCalculationAreaAtStart = calculationAreaIntegrateAlphaWater.iloc[0,1]
	alphaWaterInCalculationAreaAtFinish = calculationAreaIntegrateAlphaWater.iloc[-1,1]
	maxVelocity = calculationAreaMaxVelocity.iloc[-1,1]
	lastTime = calculationAreaIntegrateAlphaWater.iloc[-1,0]
	regionAreaFile = caseDir+"/postProcessing/sample/0/region_slope_vtk.raw"
	alphaWaterAreaFile = caseDir+"/postProcessing/sample/"+str(lastTime)+"/alpha.water_slope_vtk.raw"
	regionArea = pd.read_table(regionAreaFile, header=1, sep=' ')
	alphaWaterArea = pd.read_table(alphaWaterAreaFile, header=1, sep=' ')
	regionArr = regionArea.iloc[:,3].to_numpy()
	alphaWaterArr = alphaWaterArea.iloc[:,3].to_numpy()
	lossAlphaWater = alphaWaterInCalculationAreaAtStart - alphaWaterInCalculationAreaAtFinish
	lossFinishArea = alphaWaterInCalculationAreaAtStart - alphaWaterInFinishArea
	lossVelocity = np.linalg.norm(np.fromstring(maxVelocity))
	lossFinishArea = np.sum(regionArr * alphaWaterArr)
	loss = lossAlphaWater + lossFinishArea + lossVelocity + lossFinishArea
	open("log.MLTransportCoeffsCorrection", "a").write("lossAlphaWater = "+str(lossAlphaWater)+"\n")
	open("log.MLTransportCoeffsCorrection", "a").write("lossFinishArea = "+str(lossFinishArea)+"\n")
	open("log.MLTransportCoeffsCorrection", "a").write("lossVelocity = "+str(lossVelocity)+"\n")
	open("log.MLTransportCoeffsCorrection", "a").write("lossFinishArea = "+str(lossFinishArea)+"\n")
	open("log.MLTransportCoeffsCorrection", "a").write("loss = "+str(loss)+"\n")
	print(loss)
	return loss

def calcLoss(coeffs, caseDir):
	print(coeffs)
	open("log.MLTransportCoeffsCorrection", "a").write("coeffs: "+str(coeffs)+"\n")
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
			bash -i ./Allrun;\
			cd ../", shell=True)
	loss = readAlphaWaterLoss(caseDir)
	return loss

def minimizeSciPy(initCoeffs, caseDir):
	res = minimize(calcLoss, initCoeffs, args=(caseDir), method='Nelder-Mead', tol=1e-6)
	print(res.x)

def main():
	coeffs = [0.8, 4.64, 11.0]
#	coeffs = [0.09]
	caseDir = "blockMesh_setFields"
#	loss = readAlphaWaterLoss(caseDir)
	minimizeSciPy(coeffs, caseDir)

if __name__ == "__main__":
	main()
