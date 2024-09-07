import os
import sys
import cv2  
from PIL import Image  
from tqdm import tqdm
  
# Checking the current directory path 
  
# Folder which contains all the images 
# from which video is to be generated 
path = './' + sys.argv[1] + "/img"
  
mean_height = 0
mean_width = 0
import pandas as pd

# print(num_of_images) 
lst = pd.DataFrame(os.listdir(path), columns=['fname'])
lst = lst.set_index(pd.to_numeric(lst['fname'].str.removeprefix("86.e9_50_s").str.removesuffix('.png')))
lst = (lst.sort_index())['fname']

num_of_images = len(lst) 
for file in lst: 
    im = Image.open(os.path.join(path, file)) 
    width, height = im.size 
    mean_width += width 
    mean_height += height 
    # im.show()   # uncomment this for displaying the image 
  
# Finding the mean height and width of all images. 
# This is required because the video frame needs 
# to be set with same width and height. Otherwise 
# images not equal to that width height will not get  
# embedded into the video 
mean_width = int(mean_width / num_of_images) 
mean_height = int(mean_height / num_of_images) 
  
# print(mean_height) 
# print(mean_width) 
  
# Video Generating function 
def generate_video(): 
    #image_folder = path + "/video" # make sure to use your folder 
    video_name = 'output.avi'
      
    images = [img for img in lst
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")] 
     
    # Array images should only consider 
    # the image files ignoring others if any 
  
    frame = cv2.imread(os.path.join(path, images[0])) 
  
    # setting the frame width, height width 
    # the width, height of first image 
    height, width, layers = frame.shape   
  
    video = cv2.VideoWriter(video_name, 0, 7, (width, height))  
  
    # Appending the images to the video one by one 
    for image in tqdm(images):  
        frame = cv2.imread(os.path.join(path, image))
        #frame = cv2.putText(frame, image.replace("img_", '').replace(".png", ''), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0))
        video.write(frame)  
      
    # Deallocating memories taken for window creation 
    cv2.destroyAllWindows()  
    video.release()  # releasing the video generated 
  
  
# Calling the generate_video function 
generate_video()
