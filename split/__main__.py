import os
import cv2

import sys

from split import split

def split_video(infile):

  import subprocess
  
  v = cv2.VideoCapture(infile)
  encoder =  int(v.get(cv2.CAP_PROP_FOURCC))
  encoder = cv2.VideoWriter_fourcc("D","I","B"," ")
  size = (int(v.get(cv2.CAP_PROP_FRAME_WIDTH)/2),int(v.get(cv2.CAP_PROP_FRAME_HEIGHT)))
  del v
  
  left_cmd = "ffmpeg -i {input} -ss 00:00:20 -t 00:01:40 -filter:v crop={width}:{height}:{left_x_start}:{left_y_start} -b:v 3M {output}".format(input=infile,width=size[0],height=size[1],left_x_start=0,left_y_start=0,output="left.avi")
  right_cmd = "ffmpeg -i {input} -ss 00:00:20 -t 00:01:40 -filter:v crop={width}:{height}:{right_x_start}:{right_y_start} -b:v 3M {output}".format(input=infile,width=size[0],height=size[1],right_x_start=size[0],right_y_start=0,output="right.avi")

  p = subprocess.Popen(left_cmd)
  ret_code = p.wait()
  p = subprocess.Popen(right_cmd)
  ret_code_ = p.wait()
  
  print "Ret code = {0} and ret_code_ = {1}".format(ret_code,ret_code_)

  """
  v = cv2.VideoCapture(infile)
  encoder =  int(v.get(cv2.CAP_PROP_FOURCC))
  encoder = cv2.VideoWriter_fourcc("D","I","B"," ")
  size = (int(v.get(cv2.CAP_PROP_FRAME_WIDTH)/2),int(v.get(cv2.CAP_PROP_FRAME_HEIGHT)))

  left = cv2.VideoWriter("left.avi", encoder, 25, size)
  right = cv2.VideoWriter("right.avi", encoder, 25, size)

  while True:

    f = v.read()
    
    if f[0] is False:
      break
    else:
      f = f[1]
    
    l,r = split(f)
      
    left.write(l)
    right.write(r)
  """
  
def is_image(filename):

  _,ext = os.path.splitext(filename)
  ext = ext.lower()
  if ext == ".png" or ext == ".bmp" or ext == ".jpg" or ext == ".jpeg":
    return True
  else:
    return False

def split_images(indir):
  
  cwd = os.getcwd()
  os.chdir(indir)
  os.mkdir("left")
  os.mkdir("right")
  ims = [ f for f in os.listdir(".") if is_image(f) ]
  
  for f in ims:
  
    im = cv2.imread(f)
    l,r = split(im)
    
    cv2.imwrite(os.path.join("left",f),l)
    cv2.imwrite(os.path.join("right",f),r)    

    
  os.chdir(cwd)
  
if len(sys.argv) != 2:

  print("Error, run as:\n\n\t python split infile\n\n")
  sys.exit(1)
  
infile = sys.argv[1]

if os.path.isdir(infile):
  split_images(infile)
  
else:
  split_video(infile)
