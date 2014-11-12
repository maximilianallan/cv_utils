from trainer import Trainer
from sys import argv,exit
import cv2

if len(argv) != 3:
  print("\nError, run as: \n\n\tpython trainer IMAGE_PATH MASK_PATH\n\n")
  sys.exit(1)

t = Trainer(argv[1],argv[2])
t.train()
#t.rf = cv2.RTrees()
#t.rf.load("z:/phd/ttrack/data/lnd/classifier/config.xml")

t.predict(t.image)
