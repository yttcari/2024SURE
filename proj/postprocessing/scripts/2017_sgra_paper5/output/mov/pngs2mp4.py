import cv2
import sys
import os
from tqdm import tqdm

image_folder = 'images'
video_name = 'video.mp4'

path = sys.argv[1] + "/"

images = [img for img in os.listdir(path) if img.endswith(".png")]
frame = cv2.imread(path + images[0])
height, width, layers = frame.shape

print(f'All images read, total {len(images)} frames')

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(video_name, fourcc, 10.0, (width,height))

for image in tqdm(images):
    video.write(cv2.imread(path + image))

cv2.destroyAllWindows()
video.release()
