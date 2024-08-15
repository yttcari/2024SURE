import numpy  as np
import pandas as pd
import h5py

from matplotlib import pyplot as plt, cm

from tqdm import tqdm
from common import dalt
from common import hallmark as hm
from common import viz
from common.shadow import *
from common import analyses as nn
from common import io_ipole as io

pf = hm.ParaFrame('/xdisk/rtilanus/home/yitungtsang/{NGC}_{aspin:g}_{freq}_{inc:g}/{snapshot:d}.h5')
pf_summ = hm.ParaFrame('cache/SPO2023/summ/{NGC}_a{aspin:g}_i{inc:g}_{freq}.tsv')
for k in set(pf.keys()) - {'path'}:
    globals()[k] = np.unique(pf[k])
    print(k, globals()[k][:16])

freq = ['86.e9', '230.e9', '345.e9']

from matplotlib.patches import Ellipse
def ellipse(img, ax):
    _, alpha0, beta0, major_PWHM, minor_PWHM, PA = nn.moments(img.value, *img.fov.value, FWHM=True)

    ellipse = Ellipse(
        xy = (alpha0, beta0),
        width=minor_PWHM,
        height=major_PWHM,
        angle=-PA,
        facecolor='none',
        edgecolor='b'
    )
    ax.add_patch(ellipse)
    ax.scatter(alpha0, beta0)

def plot(ax, pf):
    if len(pf) != 1:
        return
    
    # Find vmax for 1000 snapshot    
    df_summ = pd.read_csv(pf_summ(NGC=pf.NGC.iloc[0])(aspin=pf.aspin.iloc[0])(freq=pf.freq.iloc[0])(inc=pf.inc.iloc[0]).path.iloc[0], sep='\t')
    vmax = np.max(df_summ['Imax'])

    img = io.load_img(pf.path.iloc[0])
    viz.show(img, s=0, ax=ax, vmin=0, vmax=vmax, labels=False, cmap='afmhot')
    #quiver(img, ax)
    #findring(img, ax, pf.aspin.iloc[0], pf.inc.iloc[0], pf.NGC.iloc[0])
    ellipse(img, ax)

    ax.xaxis.set_ticks(np.linspace(-25,25,5))
    ax.yaxis.set_ticks(np.linspace(-25,25,5))
    ax.tick_params(color='w')
    for spine in ax.spines.values():
        spine.set_edgecolor('w')

f = '86.e9'
i = 50
if True:
    for s in tqdm(range(1000)):
        fig = viz.grid(pf(freq=f)(inc=i)(snapshot=s+5000), plot, aspin=aspin, NGC=NGC,
                        figsize=(10,10), title=f'Moment  (freq={f}, inc={i})',
                        xtitle=r'$a_\mathrm{{spin}}={}$',  ytitle=r'{}$',
                        xlabel=r'$x$ [$\mu$as]', ylabel=r'$y$ [$\mu$as]', 
                        fout=f'output/mov_moment/{f}_{i}_s{s+5000}')
        plt.close(fig)
