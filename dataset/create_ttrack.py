import argparse
import sys
from dataset import TTrackAppCfg, VizAppCfg, process_raw_data

parser = argparse.ArgumentParser(description='Quickly create a dataset.')
parser.add_argument('--raw-dir', type=str, help='The directory containing the raw da vinci files.', required=True)
parser.add_argument('--is-raw', action='store_true', help='Initialize from a raw dataset in the \'raw_dir\' directory')
parser.add_argument('--ttrack', dest='ttrack', action="store_true", help='Create a ttrack configuration file.')
parser.add_argument('--viz', dest='viz', action="store_true", help='Create a viz configuration file.')
parser.add_argument('--rigid', dest='rigid_only', action="store_true", help='Only load the rigid pose parameter - i.e. ignore the articulated head.')
parser.add_argument('-t', '--trackable-cfg', nargs='+', type=str, help='The list of trackable config files.', required=True)
parser.add_argument('--ttrack-dir', type=str, help='The directory to save ttrack configuration data.')
parser.add_argument('--viz-dir', type=str, help='The directory to save viz configuration data.')
parser.add_argument('--interpolate', type=int, help='Interpolate the values for smoother motion.', default=1)
parser.add_argument('--camera-cfg', type=str, help='The camera configation file.', required=True)
parser.add_argument('--classifier-cfg', type=str, help='The classifier configation file (ttrack only).')
parser.add_argument('--classifier-type', type=str, help='The type of classifier (ttrack only).')
parser.add_argument('--win-width', type=int, help='The width of the camera viewport.', required=True)
parser.add_argument('--win-height', type=int, help='The height of the camera viewport.', required=True)
parser.add_argument('--viz-width', type=int, help='The width of the 3d viz viewport (viz only).')
parser.add_argument('--viz-height', type=int, help='The height of the 3d viz viewport (viz only).')
parser.add_argument('--camera-moveable', action='store_true', help='The camera is movable (viz only).')
parser.add_argument('--camera-tracked', action='store_true', help='The camera is tracked (viz only).')
args = parser.parse_args()

if not args.ttrack and not args.viz:
  print "Error, invalid usage. Either a viz or ttrack file must be selected.\n\n"
  parser.print_help()
  sys.exit(1)

if args.is_raw:

  process_raw_data(args.raw_dir)
  
  
if args.ttrack:

  d = TTrackAppCfg(args.ttrack_dir, args.ttrack_dir + "/output", args.raw_dir + "/left_video.avi", args.raw_dir + "/right_video.avi", args.raw_dir + "/" + args.camera_cfg, (args.win_width,args.win_height),  "left_output.avi", "right_output.avi", args.raw_dir + "/" + args.classifer_cfg, args.classifier_type, args.trackable_cfg)
  d.create()
  
if args.viz:

  v = VizAppCfg(args.viz_dir, args.viz_dir + "/output", args.raw_dir + "/left_video.avi", args.raw_dir + "/right_video.avi", args.raw_dir + "/" + args.camera_cfg, (args.win_width,args.win_height), "left_output.avi", "right_output.avi", (args.viz_width, args.viz_height), args.camera_moveable, args.camera_tracked, args.trackable_cfg)
  v.create()
  
  
  
  
  


