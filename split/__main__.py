import os
import sys
from split import split, split_video, split_images


def is_image(filename):

  _,ext = os.path.splitext(filename)
  ext = ext.lower()
  if ext == ".png" or ext == ".bmp" or ext == ".jpg" or ext == ".jpeg":
    return True
  else:
    return False


if len(sys.argv) != 2:

  print("Error, run as:\n\n\t python split infile\n\n")
  sys.exit(1)

infile = sys.argv[1]

if os.path.isdir(infile):
  split_images(infile)

else:
  split_video(infile)
