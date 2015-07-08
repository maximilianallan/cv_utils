from trainer import Trainer
from sys import exit
import cv2
import argparse
import os

parser = argparse.ArgumentParser(description='Train a random forest with little fuss.')

parser.add_argument('-t', '--training-data', nargs='+', type=str, help='The list of training data files.', required=True)
parser.add_argument('-m', '--masks', nargs='+', type=str, help='The list of mask files. Order should be the same as training data.', required=True)
parser.add_argument('-n', '--num-labels', type=int, help='The number of labels we are using. This is for sanity checking against the number of labels found in mask files. Defaults to 2.', default=2)
parser.add_argument('-v', '--video-file', type=str, help='Run the trained classifier on a video for testing. Leave blank to just test on the training data.')
parser.add_argument('-s', '--save-file', type=str, help='File to save the output video. Leave blank to display in window.')


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
       
  
t = Trainer(args.training_data, args.masks, "rf", args.num_labels)
t.train()

if args.video:

  cap = cv2.VideoCapture(args.video)
  if args.save_file:
    writer = cv2.VideoWriter(args.save_file, cv2.cv.FOURCC(*"DIB "),
    int(cap.get(cv2.cv.CV_CAP_PROP_FPS)),
    ( int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)),
      int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)))
    )
  else:
    writer = None
    cv2.namedWindow("Output")
    print("\nRunning video. Use 'q' to quit.\n")
  
  
  
  while True:
    f = cap.read()
    if not f[0]:
      break
    f = f[1]
    
    if writer is not None:
      writer.write(f)
    else:
      cv2.imshow("Output", f)
      key = cv2.waitKey(20) & 255
      
      if key == ord("q"):
        break
      