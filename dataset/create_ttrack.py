import argparse
import sys
from dataset.dataset import TTrackAppCfg, VizAppCfg, process_raw_data, clean_win_path

parser = argparse.ArgumentParser(description='Quickly create a dataset.')
parser.add_argument('--data-dir', type=str, help='The directory containing the processed dataset files.', required=True)
parser.add_argument('-t', '--trackable-cfg', nargs='+', type=str, help='The list of trackable config files.', required=True)
parser.add_argument('--ttrack-dir', type=str, help='The directory to save ttrack configuration data.', required=True)

parser.add_argument('--classifier-type', type=str, help='The type of classifier.', required=True)
parser.add_argument('--localizer-type', type=str, help='The type of localizer', required=True)
parser.add_argument('--win-width', type=int, help='The width of the camera viewport.', required=True)
parser.add_argument('--win-height', type=int, help='The height of the camera viewport.', required=True)
args = parser.parse_args()

args.ttrack_dir = clean_win_path(args.ttrack_dir)
args.data_dir = clean_win_path(args.data_dir)
  
d = TTrackAppCfg(args.data_dir, args.ttrack_dir, "left.avi", "right.avi", "camera/config.xml", (args.win_width,args.win_height),  "left_output.avi", "right_output.avi", "classifier/config.xml", args.classifier_type, args.localizer_type, args.trackable_cfg)
d.create()
  

  
  
  


