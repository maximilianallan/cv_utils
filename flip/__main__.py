import sys
from flip import flip_video

if len(sys.argv) != 3:
  print "Error, run as flip IN_FILE OUT_FILE"
  sys.exit(1)

flip_video(sys.argv[1],sys.argv[2])

print "Done"
