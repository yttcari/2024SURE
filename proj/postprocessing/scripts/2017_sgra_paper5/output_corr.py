import numpy  as np
import pandas as pd

from matplotlib import pyplot as plt

from common import hallmark as hm

def getdist(path, dist):
    df = pd.read_csv(path, sep='\t')
    return df[dist].values

pf = hm.ParaFrame('cache/SPO2023/summ/{NGC}_a{aspin}_i{inc}_{freq}.tsv')

for k in set(pf.keys()) - {'path'}:
    globals()[k] = np.unique(pf[k])
    print(k, globals()[k][:16])

df3 = pd.read_csv(
    pf(freq='230GHz')(mag='M')(aspin=-0.5)(inc=50).path.iloc[0],
    sep='\t'
)
df4 = pd.read_csv(
    pf(freq='230GHz')(mag='M')(aspin=-0.5)(inc=50)(Rhigh=10)(win=4).path.iloc[0],
    sep='\t'
)
df5 = pd.read_csv(
    pf(freq='230GHz')(mag='M')(aspin=-0.5)(inc=50)(Rhigh=10)(win=5).path.iloc[0],
    sep='\t'
)

print(df3.columns)

cols = ['time', 'Mdot', 'Ftot', 'alpha0', 'beta0', 'major_FWHM', 'minor_FWHM', 'PA']
corr = df3[cols].corr()
plt.imshow(corr, vmin=-1, vmax=1, cmap='bwr')
plt.xticks(range(len(cols)), cols, rotation='vertical')
plt.yticks(range(len(cols)), cols)
plt.colorbar()
