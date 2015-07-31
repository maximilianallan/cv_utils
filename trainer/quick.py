import cv2
import numpy as np
import sys
sys.path.append("z:/cv_utils")
import argparse
from recolor import ColorSpace
from trainer import RandomForest, Trainer


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

for file in args.test_data:  
  
  f = cv2.imread(file)
  if f is None:
    continue
  
  p = t.predict(f)
  
  cv2.imwrite(file.replace(".","_test."),p)
  
  