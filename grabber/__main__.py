import argparse, os.path

parser = argparse.ArgumentParser(description='Quickly extract frames from a single video or synchronously from a stereo video.')
parser.add_argument('--video-file', type=str, help='The video file.', required=True)
parser.add_argument('--right-video-file', type=str, help='The optional right video file for stereo setups.')
parser.add_argument('--split', dest='split', action="store_true", help='Assume the video file is side-by-side stereo and split the frames into left and right.')

args = parser.parse_args()

if not os.path.exists(args.video_file):
  parser.print_help()
  import sys
  sys.exit(1)

if args.right_video_file is not None and args.split is True:
  print args.right_video_file
  print args.split
  parser.print_help()
  import sys
  sys.exit(1)
  
                                
from grabber import Grabber

g = Grabber(args.split)
g.open(args.video_file, args.right_video_file)
g.run()

print("\nDone extracting frames!\n\n")
