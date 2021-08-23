import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

def timeStepsList():
	timeStepsList = np.loadtxt("timeStepsList.txt", dtype=str)
	index = np.argsort(timeStepsList.astype(np.float))
	timeStepsList = timeStepsList[index]
	return timeStepsList[1:-2]

def readVec(folder, fileName, sz):
	arr = pd.read_csv(folder+'/'+fileName, header=None, skiprows=23, nrows=sz, dtype=str)
	arr.iloc[:,0] = arr.iloc[:,0].str.replace('[(,)]', '')
	arr = arr.iloc[:,0].str.split(expand=True)

def readScalar(folder, fileName, sz):
	arr = pd.read_csv(folder+'/'+fileName, header=None, skiprows=23, nrows=sz, dtype=str)
	arr = arr.iloc[:,0].str.split(expand=True)

def spaceMean(TSL, Fs, size):
	for folder in TSL:
		for fileName in Fs:
			if fileName == 'U':
				readVec('TIF'+folder, fileName, size)
			elif fileName == 'alpha.water':
				spaceMeanAlphaWater(folder, fileName, size)

def main():
	DNSfolder = '/home/romanovadi/cases/OpenFOAM/tbnnTurbulenceInterFoam/constantAngleSlopeDNS_U4e-1_A5_H1e-2_NotDNS/'
	TSL = timeStepsList(DNSfolder)
	deltaT = 1e-06
	Fs = list(['alpha.water', 'U', 'res/U', 'res/p', 'res/T0', 'T1', 'I1', 'I2', 'Uref'])
	size = 27500
	spaceMean(TSL, Fs, size)


if __name__ == "__main__":
    main()

