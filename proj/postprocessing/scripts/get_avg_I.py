'''
find average flux of all the snapshots in the directory for debug use
'''
import numpy as np
import h5py
import os

imgdump_dir = '/xdisk/rtilanus/home/yitungtsang/NGC4594_+0.94_230.e9_50/'
imgdump = os.listdir(imgdump_dir)

avg_I = 0

for fname in imgdump:
    if fname[-3:] != ".h5":
        continue

    hfp = h5py.File(imgdump_dir + fname,'r')
    scale = hfp['header']['scale'][()]

    imagep = np.copy(hfp['pol']).transpose((1,0,2))
    I = imagep[:,:,0]

    avg_I += I.sum()*scale

print(avg_I/1000)
