from trainer import Trainer
from sys import argv,exit
import cv2

if len(argv) != 4:
  print("\nError, run as: \n\n\tpython trainer IMAGE_PATH MASK_PATH NUM_CLASSES\n\n")
  exit(1)

t = Trainer(argv[1],argv[2], int(argv[3]))
t.train()

t.predict(t.image)
