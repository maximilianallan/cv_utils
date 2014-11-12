import sys

def print_error_and_exit():
  print("Error, incorrect arguments. Run as:\n\n\t\tpython grabber INFILE\n")
  print("Optional argument --stereo if frames grabbed should be split and dumped in a left and right folder.\n\n")
  sys.exit(1)


if len(sys.argv) == 3: 
 
  if sys.argv[2] != "--stereo":  
    print_error_and_exit()
  else:
    do_stereo = True
elif len(sys.argv) == 2:

  do_stereo = False
  
else:

  print_error_and_exit()
  
from grabber import Grabber

g = Grabber(do_stereo)
g.open(sys.argv[1])
g.run()

print("\nDone extracting frames!\n\n")