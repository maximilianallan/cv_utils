import cv2
import numpy as np
import sys
import argparse
from cv_utils.recolor import ColorSpace
from trainer import RandomForest, Trainer

import os

parser = argparse.ArgumentParser(description='Test a random forest with little fuss.')

parser.add_argument('-m', '--model-file', type=str, help='The OpenCV XML model file.', required=True)
parser.add_argument('-t', '--test-data', nargs='+', type=str, help='The list of test data files.', required=True)
parser.add_argument('-n', '--num-labels', type=int, help='The number of labels we are using. This is for sanity checking against the number of labels found in mask files. Defaults to 2.', default=2)

args = parser.parse_args()

t = Trainer("rf",4)
t.model.model.load(args.model_file)

#v = cv2.VideoCapture(r"C:\Users\max\Documents\phd\pubs\miccai_2015\media\second.avi")
#w = cv2.VideoWriter("z:/output.avi", cv2.cv.CV_FOURCC('M','J','P','G'), 25, (int(v.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),                                                                            int(v.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))))

#total = v.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)                                                                             
#n = 0 

#while True:

#f = v.read()
#if f[0] == False:
#break
#f = f[1]
def predict_and_save(filename, model, outdir = None):

  f = cv2.imread(filename)
  if f is None:
    return
  
  print "Predicting"
  p = model.predict(f)
  
  print "Done predicting"
  if outdir is not None:
    cv2.imwrite(outdir + "/" + filename,p)
    print outdir + "/" + filename
  else:
    cv2.imwrite(filename.replace(".","_output."),p)

  
  
for file in args.test_data:  

  if os.path.isdir(file):
    
    cwd = os.getcwd()
    os.chdir(file)
      
    outdir = "output"
    try:
      os.mkdir(outdir)
    except OSError:
      pass    
    
    for nfile in os.listdir("."):
      
      predict_and_save(nfile, t, outdir + "/")
    
    os.chdir(cwd)
    
  else:
  
    predict_and_save(file, t)
  
  
    
  
