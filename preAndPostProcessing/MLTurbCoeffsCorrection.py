# Two unadapted parameters in code: Hstep variable and the last time step

import subprocess as sp
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import math
from multiprocessing import Pool
from functools import partial
from datetime import datetime

def readLoss(fileName):
	loss = float(open(fileName, "r").read())
	return loss

def runOF(caseDir, coeffs, coeffsKeys):
	for key, value in list(zip(coeffsKeys, coeffs)):
	    open(caseDir+'default.parameters', 'a').write(key+' '+str(value)+';\n')
	sp.call("cd "+caseDir+";\
			sbatch -n8 -W -o log.sbatch runStep.sh;\
			cd ../", shell=True)

def calcLoss(coeffs, caseDirs, coeffsKeys):
	open("log.MLTransportCoeffsCorrection", "a").write(str(datetime.now()))
	with Pool() as pool:
		pool.map(partial(runOF, coeffs=coeffs, coeffsKeys=coeffsKeys), caseDirs)
	open("log.MLTransportCoeffsCorrection", "a").write("coeffs: "+coeffs+"\n")
	lossList = list(map(readLoss, list(map(lambda e : e + "data/loss", caseDirs))))
	loss = sum(lossList)
	open("log.MLTransportCoeffsCorrection", "a").write("lossList = "+str(lossList)+"\n")
	open("log.MLTransportCoeffsCorrection", "a").write("loss = "+str(loss)+"\n")
	return loss

def minimizeSciPy(initCoeffs, bounds, calcLoss, caseDirs):
	res = minimize(calcLoss, list(initCoeffs.values()), args=(caseDirs, list(initCoeffs.keys())), method='Nelder-Mead', tol=1e-6)#, bounds=bounds)
	print(res.x)

def main():
	bounds = [[0.5, 1.0], [0.5, 2.5], [0.2, 0.8], [0.7, 1.0], [0.0, 0.15], [0.0, 0.15], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.5, 1.5], [5.0, 15.0]]
#	coeffs = [0.85, 0.5]
#	coeffs = [0.85, 1.0, 0.5, 0.856, 0.075, 0.0828, 0.09, 0.5555556, 0.44, 0.31, 1.0, 10.0]
#	coeffs = [0.88008914, 1.03075748, 0.51309077, 0.86802803, 0.07284852, 0.08184439, 0.08787684, 0.57862255, 0.43953477, 0.28480838, 1.04687694, 10.11244013]
#	coeffs = [1.27764503, 1.03143375, 0.36743293, 1.09145347, 0.0528126,  0.07580153, 0.05859115, 0.78402053, 0.48373129, 0.30037991, 1.32160641, 7.98319326]
	coeffs = {}
#	coeffs.update(alphaK1=0.85)
#	coeffs.update(alphaK2=1.0)
#	coeffs.update(alphaOmega1=0.5)
#	coeffs.update(alphaOmega2=0.856)
#	coeffs.update(beta1=0.075)
#	coeffs.update(beta2=0.0828)
#	coeffs.update(betaStar=0.09)
#	coeffs.update(gamma1=0.5555556)
#	coeffs.update(gamma2=0.44)
#	coeffs.update(a1=0.31)
#	coeffs.update(b1=1.0)
#	coeffs.update(c1=10.0)
	coeffs.update(Ceps2=1.9)
	coeffs.update(Ck=-0.416)
	coeffs.update(Bk=8.366)
	coeffs.update(C=11.0)
	coeffs.update(value=0.1)
	caseDirs = ["constantAngleSlopeTurbKWUProfileInlet180321/",
				"constantAngleSlopeTurbKWUProfileInlet230421/",
				"constantAngleSlopeTurbKWUProfileInlet100621/"]
	print(list(coeffs.values()))
	minimizeSciPy(coeffs, bounds, calcLoss, caseDirs)

if __name__ == "__main__":
	main()
