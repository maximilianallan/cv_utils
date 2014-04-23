import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Join two independent video files side by side as a stereo pair.")
parser.add_argument("leftvideo",type=str,help="The left input file.")
parser.add_argument("rightvideo",type=str,help="The right input file.")
parser.add_argument("output",type=str,help="The output video file.")
args = parser.parse_args()

left = cv2.VideoCapture(args.leftvideo)
right = cv2.VideoCapture(args.rightvideo)

if not left.isOpened() or not right.isOpened():
  raise Exception("Error, could not open video file.")
  
while True:


  l = left.read()
  r = right.read()
  
  if not l[0] or not r[0]:
    break
    
  l = l[1]
  r = r[1]
  
  stereo = np.ndarray(shape=(l.shape[0],2*l.shape[1],3),dtype=np.uint8)
  
  stereo[:,0:l.shape[1],:] = l
  stereo[:,l.shape[1]:(2*l.shape[1]),:] = r
  
  cv2.imwrite("stereo.png",stereo)
  break
