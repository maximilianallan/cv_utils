from trainer import Trainer
from sys import exit
import cv2
import argparse
import os


parser = argparse.ArgumentParser(description='Test a random forest with little fuss.')

parser.add_argument('-l', '--load-file', type=str, help='Load file for Random Forest. OpenCV .xml format.', required=True)
parser.add_argument('-v', '--video-file', type=str, help='Video file to test the trained classifier on.', required=True)
parser.add_argument('-s', '--save-file', type=str, help='File to save the output video. Leave blank to display in window.')

args = parser.parse_args()

if not os.path.exists(args.load_file):
    print("Error, could not load model!\n")
    exit(1)

if not os.path.exists(args.video_file):
    print("Error, could not video model!\n")
    exit(1)

t = Trainer("rf", 4)
t.model.load(args.load_file)

cap = cv2.VideoCapture(args.video_file)

if args.save_file:
    writer = cv2.VideoWriter(args.save_file, cv2.cv.FOURCC(*"DIB "),int(cap.get(cv2.cv.CV_CAP_PROP_FPS)),(int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)),int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))))
else:
    writer = None
    cv2.namedWindow("Output")
    print("\nRunning video. Use 'q' to quit.\n")
    
while True:

    for i in range(50):
        f = cap.read()
    if not f[0]:
      break
    f = t.predict(f[1])  
    
    if writer is not None:
      writer.write(f)
    else:
      cv2.imshow("Output", f)
      key = cv2.waitKey(5) & 255
      
      if key == ord("q"):
        break
        
