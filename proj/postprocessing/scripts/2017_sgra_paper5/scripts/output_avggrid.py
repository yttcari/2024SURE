from common import dalt
from common import hallmark as hm
from common import viz
from common import io_ipole as io
from common import mockservation as ms
import numpy as np
from matplotlib import pyplot as plt, cm
import os
import h5py

#pf = hm.ParaFrame('/Users/caritsang/desktop/project/2024SURE/dump/{NGC}_{aspin:g}_{freq}_{inc:g}/')
pf = hm.ParaFrame('../cache/SPO2023/avg/{NGC}_a{aspin:g}_i{inc:g}_f{freq}.h5')

for k in set(pf.keys()) - {'path'}:
    globals()[k] = np.unique(pf[k])
    print(k, globals()[k][:16])

#NGC = 'NGC3998'
#SPIN = 0.94


def readimg(f):
    with h5py.File(f) as h:
        m    = h['meta']
        meta = dalt.ImageMeta(**{k:m[k][()] for k in m.keys()})
        data = h['data'][:]
    return dalt.Image(data, meta=meta)

def grid(pf, xtitle=None, xlabel=None, ytitle=None, ylabel=None, fout=None, **kwargs):

    keys   = list(kwargs.keys())
    colkey = keys[0]
    cols   = kwargs.pop(keys[0])
    rowkey = keys[1]
    rows   = kwargs.pop(keys[1])
    print(len(cols), len(rows))
    if len(cols) != 0 and len(rows) != 0:
        if len(cols) == 1 or len(rows) == 1:
            fig, axes = plt.subplots(nrows=len(rows), ncols=len(cols), sharex=True, sharey=True, squeeze=False)
        else:
            fig, axes = plt.subplots(nrows=len(rows), ncols=len(cols), sharex=True, sharey=True, squeeze=False)
 
        plt.subplots_adjust(wspace=0, hspace=0)
 
        for i, x in enumerate(cols):
            for j, y in enumerate(rows):
                ax = axes[j][i]
                #img_avg  = io.load_mov([pf(**{colkey:x})(**{rowkey:y})['path'][0] + f'/5{i:03}.h5' for i in range(1000)], mean=True)
                try: 
                    img_avg = readimg(pf(**{colkey:x})(**{rowkey:y})['path'].iloc[0])
                    viz.show(img_avg, ax=ax, cmap='afmhot', vmin=0, interpolation='none', s=0)
                    print(np.max(img_avg))
                except: pass
    
                if i == 0:
                    axes[j][i].set_ylabel(colkey[0])
                else:
                    axes[j][i].set_yticklabels([])
    
                #if i == len(cols)-1 and ytitle is not None:
                #    ax_y = axes[j][i].twinx()
                #    ax_y.set_ylabel(ytitle.format(y))
                #    ax_y.yaxis.set_ticks([])
    
                if j == 0 and xtitle is not None:
                    axes[j][i].set_title(xtitle.format(x))
    
                if j == len(rows)-1:
                    axes[j][i].set_xlabel(xlabel)
                else:
                    axes[j][i].set_xticklabels([])
    
                axes[j][i].tick_params(axis='both',
                                       direction='in',
                                       top=True,
                                       right=True)
    
        
        if fout != None:
            fig.savefig(fout + '.pdf', bbox_inches='tight')
    
for obj in NGC:
    for a in aspin:         
        
        row = pf(NGC=obj)(aspin=a)['freq'].unique()
        col = pf(NGC=obj)(aspin=a)['inc'].unique()

        grid(pf(NGC=obj)(aspin=a), freq=row, inc=col, 
        ytitle=r'inc={}',  xtitle=r'freq={}',
        xlabel=r'$x$ [$\mu$as]', ylabel=r'$y$ [$\mu$as]',
        fout=f'../output/plot/{obj}_{a}')
        plt.clf()
