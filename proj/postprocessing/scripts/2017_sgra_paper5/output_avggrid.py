import numpy  as np
import pandas as pd
import h5py

from matplotlib import pyplot as plt, cm

from common import dalt
from common import hallmark as hm
from common import viz

pf = hm.ParaFrame('cache/SPO2023/avg/{NGC}_a{aspin:g}_i{inc:g}_f{freq}.h5')

for k in set(pf.keys()) - {'path'}:
    globals()[k] = np.unique(pf[k])
    print(k, globals()[k][:16])

def readimg(f):
    with h5py.File(f) as h:
        m    = h['meta']
        meta = dalt.ImageMeta(**{k:m[k][()] for k in m.keys()})
        data = h['data'][:]
    return dalt.Image(data, meta=meta)

def plot(ax, pf):
    if len(pf) != 1:
        return
    
    if pf.freq.iloc[0] == '230GHz':
        vmax = .75e-3
    else:
        vmax = None    

    img = readimg(pf.path.iloc[0])
    viz.show(img, s=0, ax=ax, cmap='afmhot', vmin=0, vmax=vmax, labels=False)
    ax.xaxis.set_ticks(np.linspace(-75,75,7))
    ax.yaxis.set_ticks(np.linspace(-75,75,7))
    ax.tick_params(color='w')
    for spine in ax.spines.values():
        spine.set_edgecolor('w')

for obj in NGC:
    for f in freq:
        fig = viz.grid(pf(freq=f)(NGC=obj), plot, aspin=aspin, inc=inc,
                           figsize=(6,6), title=f'Averaged image, inclincation $NGC={obj}^\circ$, freq {freq}',
                           xtitle=r'$a_\mathrm{{spin}}={}$',  ytitle=r'Object={}$',
                           xlabel=r'$x$ [$\mu$as]', ylabel=r'$y$ [$\mu$as]', 
                           fout=f'output/plot/{obj}_{f}')
        plt.close(fig)
