import sys
sys.path.insert(0, r"C:\sdks\opencv\build-x64\lib\Release")

from trainer import Trainer
from sys import exit
import cv2
import argparse
import os


parser = argparse.ArgumentParser(description='Test a random forest with little fuss.')

parser.add_argument('-l', '--load-file', type=str, help='Load file for Random Forest. OpenCV .xml format.', required=True)
parser.add_argument('-v', '--video-file', type=str, help='Video file to test the trained classifier on.')
parser.add_argument('-j', '--images', nargs='+', type=str, help='Image files to test the trained classifier on.')
parser.add_argument('-i', '--image', type=str, help='Image file to test the trained classifier on.')
parser.add_argument('-s', '--save-file', type=str, help='File to save the output video. Leave blank to display in window.')

args = parser.parse_args()

if not os.path.exists(args.load_file):
    print("Error, could not load model!\n")
    exit(1)

if args.video_file is None and args.images is [] and args.image is None:
    print args.print_help()
    exit(1)
    
if args.video_file and not os.path.exists(args.video_file) :
    print("Error, could not find video!\n")
    exit(1)

t = Trainer("rf", 4)
t.model.load(args.load_file)


if args.video_file:

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

          
if args.image:

    image = cv2.imread(args.image)
    f = t.predict(image)
    cv2.imwrite(args.save_file, f)
          
if args.images:

    if args.save_file is None:
    
        cv2.namedWindow("Output")
        print("\nRunning video. Use 'q' to quit.\n")

    n = 0
        
    for image_file in args.images:
    
        image = cv2.imread(image_file)
        f = t.predict(image)
        
        if args.save_file:
        
            cv2.imwrite(args.save_file + "/output" + str(n) + ".png", f)
            n += 1
            
        else:
        
            cv2.imshow("Output", f)
            key = cv2.waitKey(5) & 255
            
            if key == ord("q"):
                break
        
    
    
    