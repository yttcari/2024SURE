from astropy.io import fits
import numpy  as np
import pandas as pd
import h5py

from tqdm import tqdm
from astropy import units
from astropy import units as u
from scipy.interpolate import interp1d
from scipy.interpolate import RegularGridInterpolator
from scipy.signal      import argrelextrema

#import ehtplot
from matplotlib import pyplot as plt, cm

plt.rcParams.update({
#    "text.usetex": True,
#    "font.family": "serif",
#    "font.serif": ["Palatino"],
#    'mathtext.fontset': 'custom',
#    'mathtext.rm': 'Bitstream Vera Sans',
#    'mathtext.it': 'Bitstream Vera Sans:italic',
#    'mathtext.bf': 'Bitstream Vera Sans:bold',   
    'mathtext.fontset': 'stix',
    'font.family': 'STIXGeneral',
})

from common import dalt
from common import hallmark as hm
from common import viz
from common import io_ipole as io
from common import mockservation as ms

import os

NGC = 'NGC4261'
SPIN = '+0.94'

freqcgs = ['230.e9', '345.e9']
thetacam = ['50', '160']
vmax = [0.0014, 0.003]
fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(11,4), sharex=True, sharey=True)
plt.subplots_adjust(wspace=0, hspace=0)

for row in range(2):
    for col in range(2):
        print(row, col)
        
        img_frame  = io.load_mov(['/xdisk/rtilanus/home/yitungtsang/' + '_'.join([NGC, SPIN, freqcgs[col], thetacam[row]]) + f'/5000.h5'], mean=True)
        viz.show(img_frame, ax=axes[row, col*2+1], cmap='afmhot', vmin=0, vmax=vmax[col], interpolation='none')
 
        for i in range(1000): 
            img_avg  = io.load_mov(['/xdisk/rtilanus/home/yitungtsang/' + '_'.join([NGC, SPIN, freqcgs[col], thetacam[row]]) + f'/5{i:03}.h5'], mean=True)
            viz.show(img_avg, ax=axes[row, col*2], cmap='afmhot', vmin=0, vmax=vmax[col], interpolation='none')
        print(np.max(img_avg))
        axes[row,col].tick_params(
        axis='both',
        direction='in',
        top=True,
        right=True,
        color='w',
        )   

        axes[row, col*2].set_xlabel('$x$ [$\mu$as], avg')
        axes[row, col*2+1].set_xlabel('$x$ [$\mu$as], snap')

        axes[row, col*2].set_ylabel(None)
        axes[row, col*2+1].set_ylabel(None)
    
        axes[0, col*2].set_title(freqcgs[col])
    axes[row, 0].set_ylabel('$y$ [$\mu$as], th=' + thetacam[row])
    for col in range(4):
        for spine in axes[row, col].spines.values():
            spine.set_edgecolor('w')
        axes[row, col].xaxis.set_ticks([20, 10, 0, -10, -20])
        axes[row, col].xaxis.set_ticks([20, 10, 0, -10, -20])

#plt.show()
fig.savefig('_'.join([NGC, SPIN, 'output']) + '.pdf', bbox_inches='tight')
