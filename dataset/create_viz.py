import argparse
import sys
from dataset.dataset import TTrackAppCfg, VizAppCfg, process_raw_data, clean_win_path

parser = argparse.ArgumentParser(description='Quickly create a dataset.')
parser.add_argument('--data-dir', type=str, help='The directory containing the processed dataset files.', required=True)
parser.add_argument('--viz-dir', type=str, help='The directory to save viz configuration data.', required=True)
parser.add_argument('--win-width', type=int, help='The width of the camera viewport.', required=True)
parser.add_argument('--win-height', type=int, help='The height of the camera viewport.', required=True)
parser.add_argument('--viz-width', type=int, help='The width of the 3d viz viewport.', default=600)
parser.add_argument('--viz-height', type=int, help='The height of the 3d viz viewport.', default=600)
#parser.add_argument('-t', '--trackable-cfg', nargs='+', type=str, help='The ny of tracked objects (e.g. PSM1).', required=True)
parser.add_argument('--num-trackables', type=int, help='The number of trackables. Will set up configs for PSM 1, 2.. N', required=True)
args = parser.parse_args()

args.viz_dir = clean_win_path(args.viz_dir)
args.data_dir = clean_win_path(args.data_dir)

v = VizAppCfg(args.data_dir, args.viz_dir, "left.avi", "right.avi", "camera/config.xml", (args.win_width,args.win_height), "left_output.avi", "right_output.avi", (args.viz_width, args.viz_height), args.num_trackables)
v.create()
  
  
  
  
  


