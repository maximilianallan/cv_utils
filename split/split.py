import cv2
import os

def split(frame):
  
  width = int(frame.shape[1]/2)
  
  try:
    return frame[:,0:width,:],frame[:,width:width*2,:]
  except:
    return frame[:,0:width],frame[:,width:width*2] #single channel
 

def split_video(infile):

  import subprocess

  v = cv2.VideoCapture(infile)
  encoder =  int(v.get(cv2.CAP_PROP_FOURCC))
  encoder = cv2.VideoWriter_fourcc("D","I","B"," ")
  size = (int(v.get(cv2.CAP_PROP_FRAME_WIDTH)/2),int(v.get(cv2.CAP_PROP_FRAME_HEIGHT)))
  del v

  #-ss 00:00:20 -t 00:01:40
  left_cmd = "ffmpeg -i {input} -filter:v crop={width}:{height}:{left_x_start}:{left_y_start} -b:v 3M {output}".format(input=infile,width=size[0],height=size[1],left_x_start=0,left_y_start=0,output="left.avi")
  right_cmd = "ffmpeg -i {input} -filter:v crop={width}:{height}:{right_x_start}:{right_y_start} -b:v 3M {output}".format(input=infile,width=size[0],height=size[1],right_x_start=size[0],right_y_start=0,output="right.avi")

  p = subprocess.Popen(left_cmd)
  ret_code = p.wait()
  p = subprocess.Popen(right_cmd)
  ret_code_ = p.wait()

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