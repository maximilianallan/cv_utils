from trainer import Trainer
from sys import exit

import cv2
import argparse
import os

parser = argparse.ArgumentParser(description='Train a random forest with little fuss.')

parser.add_argument('-t', '--training-data', nargs='+', type=str, help='The list of training data files.', required=True)
parser.add_argument('-m', '--masks', nargs='+', type=str, help='The list of mask files. Order should be the same as training data.', required=True)
parser.add_argument('-n', '--num-labels', type=int, help='The number of labels we are using. This is for sanity checking against the number of labels found in mask files. Defaults to 2.', default=2)
parser.add_argument('-o', '--output-file', type=str, help='Path to save the output file. If not supplied then $CWD/RF_N.xml will be used, where N is the number of classes.', default=None)
args = parser.parse_args()

if len(args.training_data) != len(args.masks):
  
  print("\nError, the number of training data file is not equal to the number of mask files!\n")
  parser.print_help()
  exit(1)
  
for f,g in zip(args.training_data, args.masks):

  if not os.path.exists(f):
    print("\nError, training data file \'{0}\' does not exist.\n".format(f))
    parser.print_help()
    exit(1)
  
  if not os.path.exists(g):
    print("\nError, mask file \'{0}\' does not exist.\n".format(g))
    parser.print_help()
    exit(1)
       
t = Trainer("rf", 4)
t.setup_training(args.training_data, args.masks, args.num_labels)
t.train(args.output_file)

for n, path in enumerate(args.training_data):
    im = cv2.imread(path)
    p = t.predict(im)
    cv2.namedWindow(path)
    cv2.imshow(path, p)
    key = cv2.waitKey(-1)
    if key & 255 == ord("q"):
        
        break
    
    elif key & 255 == ord("s"):
        
        cv2.imwrite(path.replace(".","_output{0}.".format(args.num_labels)), p)
    
    elif key & 255 == ord(" "):
    
        continue
