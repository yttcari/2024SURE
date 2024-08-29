import sys
import os
import numpy as np
import h5py
from tqdm import tqdm

path = sys.argv[1]
fdir = os.listdir(path)

avgI = 0

for fname in tqdm(fdir):
    if fname[-3:] == '.h5':
        hfp = h5py.File(path+fname,'r')
        scale = hfp['header']['scale'][()]
        #imagep = np.copy(hfp['pol']).transpose((1,0,2))
        #I = imagep[:,:,0]
        unpol = np.copy(hfp['unpol']).transpose((1,0))
        avgI += unpol.sum()*scale

avgI /= len(fdir)
print(avgI)
