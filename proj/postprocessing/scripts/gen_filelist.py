'''
Generate the file list for the mring fitting code in csv format
$ python gen_filelist.py [path]
'''

import os
import sys
import subprocess
import csv

# As for each snapshot = 5 GM/c^3
sample_window = 500/5

input_dir = sys.argv[1]

fdir = os.listdir(input_dir)
fdir.sort()
with open('filelist.csv', 'w', newline='') as csvfile:
    for fname in fdir:
        if fname[-3:] != '.h5':
            fdir.remove(fname)
        elif (fdir.index(fname)+1) % sample_window == 0:
            writer = csv.writer(csvfile)
            writer.writerow([input_dir+fname])

