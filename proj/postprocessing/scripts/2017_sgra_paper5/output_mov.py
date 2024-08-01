import numpy  as np
import pandas as pd
import h5py

import matplotlib.animation as animation
from matplotlib import pyplot as plt, cm
from tqdm       import tqdm
#plt.rcParams['animation.ffmpeg_path'] = r'/opt/ohpc/pub/apps/ffmpeg/4.1/bin/ffmpeg'

from common import io_ipole as io
from common import dalt
from common import hallmark as hm
from common import viz

pf_summ = hm.ParaFrame('cache/SPO2023/summ/{NGC}_a{aspin:g}_i{inc:g}_{freq}.tsv')
pf = hm.ParaFrame('/xdisk/rtilanus/home/yitungtsang/{NGC}_{aspin:g}_{freq}_{inc:g}/{snapshot:d}.h5')

for k in set(pf.keys()) - {'path'}:
    globals()[k] = np.unique(pf[k])
    print(k, globals()[k][:16])

for obj in NGC:
    for a in aspin:
        for i in inc:
            for f in freq:
                sel = pf(aspin=a)(freq=f)(inc=i)(NGC=obj)
                sel_summ = pf_summ(aspin=a)(freq=f)(inc=i)(NGC=obj)

                df = pd.read_csv(sel_summ['path'].iloc[0], sep='\t')
                vmax = np.max(df['Imax'])
                print(vmax)

                fig, ax = plt.subplots()
                ims = []
                for s in tqdm(range(1000)):
                    img_avg = io.load_mov(sel(snapshot=s+5000)['path'].iloc[0])
                    img = img_avg.value.astype(float)
                
                    f = ax.imshow(img[:,:,0], cmap='afmhot', animated=True, vmin=0, vmax=0.0003)
                
                    ims.append([f])
                    if s == 0:
                        ax.imshow(img[:,:,0], cmap='afmhot')
                
                ani = animation.ArtistAnimation(fig, ims, repeat_delay=1000, interval=16, blit=True,)
                #ani.save('output/mov/{}_{}_{}_{}.mp4'.format(obj, a, i ,f))

                writer = animation.PillowWriter(fps=60)
                ani.save("output/mov/test.gif", writer=writer)
