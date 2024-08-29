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

from matplotlib.patches import Ellipse

pf = hm.ParaFrame('/xdisk/rtilanus/home/yitungtsang/{NGC}_{aspin:g}_{freq}_{inc:g}/{snapshot:d}.h5')
pf_summ = hm.ParaFrame('cache/SPO2023/summ/{NGC}_a{aspin:g}_i{inc:g}_{freq}.tsv')

for k in set(pf.keys()) - {'path'}:
    globals()[k] = np.unique(pf[k])
    print(k, globals()[k][:16])

freq = ['86.e9', '230.e9', '345.e9']
NGC = ['NGC3998', 'NGC4261', 'NGC4594']

# Filter the desired conditions
f = '86.e9'
i = 50

# Desired x and y axis of the scatter corr graph
X = 'alpha0'
Y = 'PA'
ylim_path = pf_summ(freq='86.e9')(inc=50).path

lim_df = pd.DataFrame()
for path in ylim_path:
    temp_df = pd.read_csv(path, sep='\t')
    temp_df['alpha0'] = temp_df['alpha0'] - temp_df['alpha0'].iloc[0]
    lim_df = pd.concat([lim_df, pd.DataFrame({X: temp_df[X], Y: temp_df[Y]})])
Xlim = (np.min(lim_df[X]), np.max(lim_df[X]))
Ylim = (np.min(lim_df[Y]), np.max(lim_df[Y]))

print(X, Xlim, Y, Ylim)

def ellipse(img, ax):
    '''
    Plot second moment of the image, 
    ellipse with centre (alpha0, beta0), major_FWHM and minor_FWHM
    '''
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
    '''
    Plot the intensity of the images 
    ''' 
    if len(pf) != 1:
        return
    
    # Find vmax for 1000 snapshot    
    df_summ = pd.read_csv(pf_summ(NGC=pf.NGC.iloc[0])(aspin=pf.aspin.iloc[0])(freq=pf.freq.iloc[0])(inc=pf.inc.iloc[0]).path.iloc[0], sep='\t')
    vmax = np.max(df_summ['Imax'])

    # Load image
    img = io.load_img(pf.path.iloc[0])
    viz.show(img, s=0, ax=ax, vmin=0, vmax=vmax, labels=False, cmap='afmhot', aspect='equal')
    
    # Plot second moment of the image
    ellipse(img, ax)

    ax.xaxis.set_ticks(np.linspace(-25,25,5))
    ax.yaxis.set_ticks(np.linspace(-25,25,5))
    ax.tick_params(color='w')
    for spine in ax.spines.values():
        spine.set_edgecolor('w')

def check_rel(ax, pf):
    '''
    Plot the scattered corr graph
    TODO: change a better way to set for ylim, xlim, and relative alpha0....
    '''
    df = pd.read_csv(pf_summ(freq=pf.freq.iloc[0])(inc=pf.inc.iloc[0])(NGC=pf.NGC.iloc[0])(aspin=pf.aspin.iloc[0]).path.iloc[0], sep='\t')
    sno = pf.snapshot.iloc[0] - 5000 
    
    # From absolute alpha0 to relative alpha0/beta0
    df['alpha0'] = df['alpha0'] - df['alpha0'].iloc[0]
    df['beta0'] = df['beta0'] - df['beta0'].iloc[500]

    # Set scale, factor 1.1 is to center the data
    ax.set_ylim(bottom=np.min(lim_df[Y]), top=np.max(lim_df[Y]))
    ax.set_xlim(left=np.min(lim_df[X]), right=np.max(lim_df[X]))

    filtered_df = df[df.index <= sno]
    
    ax.scatter(filtered_df[filtered_df.index < sno][X], filtered_df[filtered_df.index < sno][Y], s=1, color='b')
    ax.scatter(filtered_df[filtered_df.index == sno][X], filtered_df[filtered_df.index == sno][Y], s=1, color='r')

def grid(pf, plot,
         fout   = None,
         title  = None,
         rowmap = None,
         colmap = None,
         xtitle = None,
         ytitle = None,
         xlabel = None,
         ylabel = None,
         xspace = 0.05,
         yspace = 0,
         legend = None,
         **kwargs):
    '''
    modified for side-by-side comparison of intensity image and scatter graph of quantities
    '''

    keys   = list(kwargs.keys())
    colkey = keys[0]
    cols   = kwargs.pop(keys[0])
    rowkey = keys[1]
    rows   = kwargs.pop(keys[1])

    fig, axes = plt.subplots(len(rows), len(cols)*2, **kwargs)
    if len(rows) == 1:
        axes = [axes]
    if len(cols) == 1:
        axes = [[a] for a in axes]

    for i, c in enumerate(cols):
        for j, r in enumerate(rows):
            plot[0](axes[j][i*2], pf(**{colkey:c})(**{rowkey:r}))
            plot[1](axes[j][i*2+1], pf(**{colkey:c})(**{rowkey:r}))

            # align axis of scatter plot
            axes[j][i*2+1].set_xlim(Xlim[1], Xlim[0]) # swap the direction of x-lim to match the intensity image
            axes[j][i*2+1].set_ylim(Ylim[0], Ylim[1])

            if i == 0:
                axes[j][i*2].set_ylabel(ylabel[0])
                axes[j][i*2+1].set_ylabel(ylabel[1])
            elif i != len(cols)-1:
                axes[j][i*2+1].set_yticklabels([])
                axes[j][i*2].set_yticklabels([])
            elif i == len(cols)-1:
                axes[j][i*2+1].yaxis.set_tick_params(labelright=True)
                axes[j][i*2].set_yticklabels([])

            if i == len(cols)-1 and ytitle is not None:
                ax_r = axes[j][i*2+1] #ax_r = axes[j][i].twinx()
                ax_r.yaxis.set_label_position("right")
                if rowmap is not None:
                    ax_r.set_ylabel(ytitle.format(rowmap[r]))
                else:
                    ax_r.set_ylabel(ytitle.format(r))

            if j == 0 and xtitle is not None:
                if colmap is not None:
                    axes[j][i].set_title(xtitle.format(colmap[c]))
                else:
                    axes[j][i*2].set_title(xtitle.format(c))

            if j == len(rows)-1:
                axes[j][i*2].set_xlabel(xlabel[0])
                axes[j][i*2+1].set_xlabel(xlabel[1])
            else:
                axes[j][i*2].set_xticklabels([])
                axes[j][i*2+1].set_xticklabels([])

            axes[j][i].tick_params(axis='both',
                                   direction='in',
                                   top=True,
                                   right=True)
            axes[j][i*2+1].tick_params(axis='both',
                                   direction='in',
                                   top=True,
                                   right=True)

    if legend is not None:
        axes[0][-1].legend(loc=legend)

    fig.suptitle(title)
    #fig.tight_layout()
    fig.subplots_adjust(wspace=xspace, hspace=yspace)
    if fout:
        fig.savefig(fout+'.png', dpi=300)
        #fig.savefig(fout+'.png', dpi=300)

    return fig

if True:
    for s in tqdm(range(1000)):
        fig = grid(pf(freq=f)(inc=i)(snapshot=s+5000), [plot, check_rel], aspin=aspin, NGC=NGC,
                        figsize=(15, 5), title=f'Moment  (freq={f}, inc={i})',
                        xtitle=r'$a_\mathrm{{spin}}={}$',  ytitle=r'{}'+ f' {Y} [deg]',
                        xlabel=[r'$x$ [$\mu$as]', f'{X}'+r' [$\mu$as]'], ylabel=[r'$y$ [$\mu$as]', f'{Y}'+r' [deg]'], 
                        fout=f'output/mov/moment/imgwgraph/{f}_{i}_s{s+5000}')
        plt.close(fig)
