import sys

if len(sys.argv) != 2:
  print("Error, incorrect arguments. Run as:\n\n\t\tpython grabber INFILE\n\n")
  sys.exit(1)
  
from grabber import Grabber

g = Grabber()
g.open(sys.argv[1])
g.run()

print("\nDone extracting frames!\n\n")