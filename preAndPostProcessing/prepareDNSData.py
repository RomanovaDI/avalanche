import subprocess as sp
import numpy as np
import pandas as pd
import fileinput as fi

def timeStepsList():
	sp.call("ls -1 -d [0-9]* > timeStepsList.txt", shell=True)
	timeStepsList = np.loadtxt("timeStepsList.txt", dtype=str)
	index = np.argsort(timeStepsList.astype(np.float))
	timeStepsList = timeStepsList[index]
#	timeStepsList = pd.read_csv("timeStepsList.txt")
#	index = np.argsort(timeStepsList.to_numpy())
	print(timeStepsList)
	return timeStepsList

def spaceMean(TSL, Fs, sizes):
	for folder in TSL:
		for fileName in Fs:
			if fileName == 'U':
				spaceMeanU(folder, fileName, sizes)
	return

def spaceMeanU(folder, fileName, sz):
	sz1 = sz[0]
	sz1S = sz1[0]*sz1[1]*sz1[2]
	sz2 = sz[1]
	uArr = pd.read_csv(folder+'/'+fileName, header=None, skiprows=23, nrows=220000, dtype=str)
	uArr.iloc[:,0] = uArr.iloc[:,0].str.replace('[(,)]', '')
	uArr = uArr.iloc[:,0].str.split(expand=True)
	uArrXNp = np.concatenate((uAvComp(uArr.iloc[:sz1S,0].to_numpy(dtype=float), sz1), uAvComp(uArr.iloc[sz1S:,0].to_numpy(dtype=float), sz2)))
	uArrYNp = np.concatenate((uAvComp(uArr.iloc[:sz1S,1].to_numpy(dtype=float), sz1), uAvComp(uArr.iloc[sz1S:,1].to_numpy(dtype=float), sz2)))
	uArrZNp = np.concatenate((uAvComp(uArr.iloc[:sz1S,2].to_numpy(dtype=float), sz1), uAvComp(uArr.iloc[sz1S:,2].to_numpy(dtype=float), sz2)))
	uArrAv = pd.DataFrame(data=np.transpose(np.stack((uArrXNp, uArrYNp, uArrZNp))), dtype=str, columns=['x', 'y', 'z'])
	uArrAv['strings'] = '( '+uArrAv['x']+' '+uArrAv['y']+' '+uArrAv['z']+' )'
	sp.call("cp patterns/USpaceAvaragePatternBeginning "+folder+"/USpAv", shell=True)
	with fi.FileInput(folder+'/USpAv', inplace=True) as file:
		for line in file:
			print(line.replace('folderName', '"'+folder+'"'), end='')
	uArrAv['strings'].to_csv(folder+'/USpAv', mode='a', index=False, header=False)
	with open(folder+'/USpAv', 'a') as fout, fi.input('patterns/USpaceAvaragePatternEnding') as fin:
		for line in fin:
			fout.write(line)

def uAvComp(uArr, sz):
	uArr = np.average(np.reshape(uArr, (-1,2)), axis=1)
	uArr = np.transpose(np.reshape(np.average(np.reshape(np.transpose(np.reshape(uArr, (-1,int(sz[2]/2)))), (-1,2)), axis=1), (int(sz[2]/2),-1)))
	uArr = np.transpose(np.reshape(np.average(np.reshape(np.transpose(np.reshape(uArr, (-1,int(sz[2]*sz[1]/4)))), (-1,2)), axis=1), (int(sz[2]*sz[1]/4),-1)))
	uArr = uArr.flatten()
	return uArr

def main():
	TSL = timeStepsList()
	Fs = list(['alpha.water', 'U', 'p_rgh'])
	sizes = list([[100, 20, 100], [100, 20, 10]])
	spaceMeanU('1e-07', 'U', sizes)

if __name__ == "__main__":
    main()
