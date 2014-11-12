import os
import sys
import time
  
from chomp import chomp_video
  
if len(sys.argv) != 5:

  print("Error, run as:\n\n\t python chomp infile start_time end_time outfile\n\n")
  sys.exit(1)
  
infile = sys.argv[1]
starttime = time.strptime(sys.argv[2], "%H:%M:%S")
endtime = time.strptime(sys.argv[3], "%H:%M:%S")
outfile = sys.argv[4]

chomp_video(infile,starttime,endtime,outfile)
