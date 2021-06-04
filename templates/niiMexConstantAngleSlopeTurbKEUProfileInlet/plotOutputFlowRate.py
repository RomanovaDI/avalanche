import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dfOutletExp = pd.read_csv('outlet.txt', delimiter="\t", header=None)
zExp = dfOutletExp[0].to_numpy()
uExp = dfOutletExp[1].to_numpy()
dfOutletCalc = pd.read_csv('outputFlowRate.csv')
zCalc = dfOutletCalc["Points:2"].to_numpy()
uCalc = dfOutletCalc["U:0"].to_numpy()
uCalc[0] = 0
alphaWaterCalc = dfOutletCalc["alpha.water"].to_numpy()
print(uCalc*alphaWaterCalc)
a = np.arange(5)
b = np.arange(5)
print(a*b)
plt.plot(uExp, zExp*0.001, label="experiment")
plt.plot(uCalc*alphaWaterCalc, zCalc, label="calculated")
plt.legend()
plt.show()
