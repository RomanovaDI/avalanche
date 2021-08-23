import subprocess as sp
import numpy as np
import pandas as pd
import fileinput as fi

def timeStepsList(DNSfolder):
	sp.call('ls -1 -d '+DNSfolder+'[0-9]* |xargs -n1 basename > timeStepsList.txt', shell=True)
	timeStepsList = np.loadtxt("timeStepsList.txt", dtype=str)
	index = np.argsort(timeStepsList.astype(np.float))
	timeStepsList = timeStepsList[index]
	return timeStepsList[1:]

def prepareFolders(DNSfolder, TSL, deltaT):
	sp.call('rm -rf TIF[0-9]*', shell=True)
	for time in TSL:
		sp.call('cp -r TIForig TIF'+time+';\
				cd TIF'+time+';\
				cp '+DNSfolder+time+'/USpAv 0/U;\
				cp '+DNSfolder+time+'/awSpAv 0/alpha.water;\
				mv 0 '+time, shell=True)
		with fi.FileInput('TIF'+time+'/system/controlDict', inplace=True) as file:
			for line in file:
				print(line.replace('startTimePattern', time), end='')
		with fi.FileInput('TIF'+time+'/system/controlDict', inplace=True) as file:
			for line in file:
				print(line.replace('endTimePattern', str(float(time)+deltaT)), end='')
		with fi.FileInput('TIF'+time+'/system/controlDict', inplace=True) as file:
			for line in file:
				print(line.replace('deltaTPattern', str(deltaT)), end='')
		sp.call('cd TIF'+time+';\
				./Allrun', shell=True)
	for n in range(len(TSL)-1):
		sp.call('cp '+DNSfolder+TSL[n+1]+'/USpAv '+'TIF'+TSL[n]+'/'+TSL[n+1]+'/Uref', shell=True)
	for n in range(len(TSL)-1):
		sp.call('cp -r TIF'+TSL[n]+'/'+TSL[n+1]+' TIF'+TSL[n]+'/'+TSL[n]+'/res', shell=True)

def main():
	DNSfolder = '/home/romanovadi/cases/OpenFOAM/tbnnTurbulenceInterFoam/constantAngleSlopeDNS_U4e-1_A5_H1e-2_NotDNS/'
	TSL = timeStepsList(DNSfolder)
	deltaT = 1e-06
	prepareFolders(DNSfolder, TSL, deltaT)

if __name__ == "__main__":
    main()
