'''
Make video from image frames
Runs in terminal: python mkvid.py [path].

In [path], it should contains [path/img], 
which contains all the image frames needed.
Should change the prefix of the name in code.

Output will be [path/video.mp4]
'''

import subprocess
import sys
import os

path = sys.argv[1]
directories = os.listdir(path)

# Parameters
fps = 60
fname = path + 'img/86.e9_50_s5%03d.png'
vid_name = 'video.mp4'

print(directories)

if 'img' in directories:
    subprocess.call(['ffmpeg', '-framerate', str(fps),
                     '-i', fname, '-r', '30', '-pix_fmt', 'yuv420p', vid_name])
else:
    print('The given path does not contain [path]/img folder. Please ensure all the image frames are stored in the folder.')
