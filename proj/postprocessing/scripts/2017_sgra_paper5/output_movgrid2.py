import numpy  as np
import pandas as pd
import h5py
import tqdm
import sys
from matplotlib import pyplot as plt, cm

from common import dalt
from common import hallmark as hm
from common import viz
from common import io_ipole as io

import matplotlib.animation as animation

#pf = hm.ParaFrame('cache/SPO2023/avg/{NGC}_a{aspin:g}_i{inc:g}_f{freq}.h5')
pf = hm.ParaFrame('/xdisk/rtilanus/home/yitungtsang/{NGC}_{aspin:g}_{freq}_{inc:g}/{snapshot:d}.h5')
pf_summ = hm.ParaFrame('cache/SPO2023/summ/{NGC}_a{aspin:g}_i{inc:g}_{freq}.tsv')

sorter = ['86.e9', '230.e9', '345.e9']
pf = pf.sort_values(by='freq', key=lambda col: col.map(lambda e : sorter.index(e)))

for k in set(pf.keys()) - {'path'}:
    globals()[k] = np.unique(pf[k])
    print(k, globals()[k][:16])


def grid(pf, pf_summ, n, deg, ylabel=None, title=None, xtitle=None, xlabel=None, ytitle=None, xspace=None, yspace=None, **kwargs):
    pf = pf.sort_values('aspin')
    keys   = list(kwargs.keys())
    colkey = keys[0]
    cols   = kwargs.pop(keys[0])
    rowkey = keys[1]
    rows   = kwargs.pop(keys[1])

    fig, axes = plt.subplots(ncols=len(cols), nrows=len(rows), figsize=(11,11), sharex=True, sharey=True)
    plt.subplots_adjust(wspace=0, hspace=0)

    frames = []

    for i, x in enumerate(rows):
        for j, y in enumerate(cols):
            
            print(i, j)
            ax = axes[i][j]
           
            sel = pf(freq=x)(aspin=y)
            sel_summ = pf_summ(freq=x)(aspin=y) 
            print(sel['path'].iloc[0])
            print(sel_summ['path'].iloc[0])
            df = pd.read_csv(sel_summ['path'].iloc[0], sep='\t')
            vmax = np.max(df['Imax'])
            print(vmax)
            
            ims = []
      
            img_avg = io.load_mov(sel(snapshot=5000)['path'].iloc[0])
            img = img_avg.value.astype(float)
            ax.imshow((img[:,:,0].T), cmap='afmhot', vmin=0, vmax=vmax, origin='lower', extent=img_avg.extent)

            for s in tqdm.tqdm(range(1000)):
                img_avg = io.load_mov(sel(snapshot=s+5000)['path'].iloc[0])
                img = img_avg.value.astype(float)

                f = ax.imshow((img[:,:,0].T), cmap='afmhot', animated=True, vmin=0, vmax=vmax, origin='lower', extent=img_avg.extent)
                ims.append(f)

            frames.append(np.array(ims))

            if j == 0:
                ax.set_ylabel(ytitle.format(x))
                ax.set_yticks([])
            else:
                ax.set_yticks([])
            if i  == len(row)-1 :
                ax.set_xlabel(xtitle.format(y))
                ax.set_xticks([])
            else:
                ax.set_xticks([])
            #ax.tick_params(labelbottom=False, labelleft=False)

            ax.tick_params(axis='both', direction='out', bottom=True, left=True)
    fig.suptitle(title.format(n, deg))
    fig.tight_layout()
    ani_frames = np.stack(np.array(frames), axis=-1)
    print(ani_frames.shape)
    fig.tight_layout()

    ani = animation.ArtistAnimation(fig, ani_frames, repeat_delay=1000, interval=15, blit=True,)
    writer = animation.PillowWriter(fps=60)
    ani.save("output/mov/{}_{}.gif".format(n, deg), writer=writer)

OBJ = NGC[int(sys.argv[1])]
INC = 160
col = np.sort(pf(NGC=OBJ)(inc=INC)['aspin'].unique())
row = (pf(NGC=OBJ)(inc=INC)['freq'].unique())
grid(pf(NGC=OBJ)(inc=INC), pf_summ(NGC=OBJ)(inc=INC), n=OBJ, deg=INC, freq=col, aspin=row, 
xtitle=r'$a_\mathrm{{spin}}={}$', ytitle=r'$\nu={}$',
ylabel=r'$y$ [$\mu$as]', xlabel=r'$x$ [$\mu$as]', title=r'{} i={}$^\circ$')
