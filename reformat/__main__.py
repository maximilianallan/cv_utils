import os
import argparse
import cv2
from sys import exit

parser = argparse.ArgumentParser(description='Quickly convert all images in directory to a different format.')

parser.add_argument('-i', '--input-dir', type=str, help='The directory to use for finding images. Required for safety.', required=True)
parser.add_argument('-f', '--format', type=str, choices=['png', 'bmp', 'jpg', 'jpeg'], help='The target formats.', required=True)
parser.add_argument('-r', '--recursive', action="store_true", help='Apply reformat recursively.')
parser.add_argument('-d', '--delete', action="store_true", help='Delete old images after reformat.')
parser.add_argument('-v', '--verbose', action="store_true", help='Print progress messages.')
args = parser.parse_args()

if not os.path.exists(args.input_dir):
  print("Error, {0} does not exist.".format(args.input_dir))
  parser.print_help()
  exit(1)
  
os.chdir(args.input_dir)

def vprint(to_print):
  
  if args.verbose:
    print(to_print)


vprint("Starting processing")
    
for root,dirs,files in os.walk("."):

  for f in [os.path.join(root,fl) for fl in files]:
    
    try:
      i = cv2.imread(f)
      if i is None:
        continue
        
      bname,ext = os.path.splitext(f)
      if cv2.imwrite(bname + "." + args.format, i):
        vprint("Reformatted {0} to {1}".format(f, bname + "." + args.format))
        if args.delete:
          os.remove(f)
      else:
        vprint("Unable to save {0}".format(f))
    except Exception as e:
      vprint("Error processing {0}. \nMessage: {1}".format(f,e))
  
  if not args.recursive:
    break

vprint("Done!")