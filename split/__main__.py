import os
os.environ["PATH"] = "c:/users/max/projects/opencv/build32/install/x86/vc12/bin/" + ";" + os.environ["PATH"]
import cv2

import sys

from split import split

if len(sys.argv) != 2:

  print("Error, run as:\n\n\t python split infile\n\n")
  sys.exit(1)
  
infile = sys.argv[1]

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
  