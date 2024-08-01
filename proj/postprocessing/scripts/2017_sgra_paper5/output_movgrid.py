import numpy  as np
import pandas as pd
import h5py
import tqdm

from matplotlib import pyplot as plt, cm

from common import dalt
from common import hallmark as hm
from common import viz
from common import io_ipole as io

import matplotlib.animation as animation

#pf = hm.ParaFrame('cache/SPO2023/avg/{NGC}_a{aspin:g}_i{inc:g}_f{freq}.h5')
pf = hm.ParaFrame('/xdisk/rtilanus/home/yitungtsang/{NGC}_{aspin:g}_{freq}_{inc:g}/{snapshot:d}.h5')
pf_summ = hm.ParaFrame('cache/SPO2023/summ/{NGC}_a{aspin:g}_i{inc:g}_{freq}.tsv')
for k in set(pf.keys()) - {'path'}:
    globals()[k] = np.unique(pf[k])
    print(k, globals()[k][:16])


def grid(pf, pf_summ, n, i, ylabel=None, title=None, xtitle=None, xlabel=None, **kwargs):
    pf = pf.sort_values('aspin')
    keys   = list(kwargs.keys())
    colkey = keys[0]
    cols   = kwargs.pop(keys[0])
    rowkey = keys[1]
    rows   = kwargs.pop(keys[1])

    fig, axes = plt.subplots(ncols=len(cols), nrows=len(rows), figsize=(11,11), sharex=True, sharey=True, squeeze=False)
    plt.subplots_adjust(wspace=0, hspace=0)

    frames = []

    for i, x in enumerate(rows):
        for j, y in enumerate(cols):
            
            print(i, j)
            ax = axes[i][j]
           
            sel = pf(freq=y)(aspin=x)
            sel_summ = pf_summ(freq=y)(aspin=x) 
            print(sel['path'].iloc[0])
            print(sel_summ['path'].iloc[0])
            df = pd.read_csv(sel_summ['path'].iloc[0], sep='\t')
            vmax = np.max(df['Imax'])
            print(vmax)
            
            ims = []
      
            img_avg = io.load_mov(sel(snapshot=5000)['path'].iloc[0])
            img = img_avg.value.astype(float)
            ax.imshow(img[:,:,0], cmap='afmhot', vmin=0, vmax=vmax)

            for s in tqdm.tqdm(range(1000)):
                img_avg = io.load_mov(sel(snapshot=s+5000)['path'].iloc[0])
                img = img_avg.value.astype(float)

                f = ax.imshow(img[:,:,0], cmap='afmhot', animated=True, vmin=0, vmax=vmax)
                ims.append(f)
   
            frames.append(np.array(ims))            
 
            ax.set_title(title.format(y, x))

            if j == len(rows)-1:
                ax.set_xlabel(xlabel)
            else:
                ax.set_xticklabels([])

    ani_frames = np.stack(np.array(frames), axis=-1)
    print(ani_frames.shape)
    fig.tight_layout()

    ani = animation.ArtistAnimation(fig, ani_frames, repeat_delay=1000, interval=15, blit=True,)
    writer = animation.PillowWriter(fps=60)
    ani.save("output/mov/test.gif", writer=writer)
 
for OBJ in NGC:
    for INC in inc:
        col = np.sort(pf(NGC=OBJ)(inc=INC)['freq'].unique())
        row = np.sort(pf(NGC=OBJ)(inc=INC)['aspin'].unique())
        #print(pf(NGC=OBJ)(inc=INC))
        grid(pf(NGC=OBJ)(inc=INC), pf_summ(NGC=OBJ)(inc=INC), OBJ, INC, freq=col, aspin=row, 
                title=r'a={}, f={}',
                xlabel=r'$x$ [$\mu$as]', ylabel=r'$y$ [$\mu$as]')
