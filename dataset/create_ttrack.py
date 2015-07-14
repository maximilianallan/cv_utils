import argparse
import sys
from dataset.dataset import TTrackAppCfg, VizAppCfg, process_raw_data, clean_win_path,clean_dir_end

parser = argparse.ArgumentParser(description='Quickly create a dataset.')
parser.add_argument('--data-dir', type=str, help='The directory containing the processed dataset files.', required=True)
parser.add_argument('-t', '--trackable-cfg', nargs='+', type=str, help='The list of trackable config files.', required=True)
parser.add_argument('--ttrack-dir', type=str, help='The directory to save ttrack configuration data.', required=True)

parser.add_argument('--classifier-type', type=str, help='The type of classifier.', required=True)
parser.add_argument('--localizer-type', type=str, help='The type of localizer', required=True)
parser.add_argument('--win-width', type=int, help='The width of the camera viewport.', required=True)
parser.add_argument('--win-height', type=int, help='The height of the camera viewport.', required=True)
parser.add_argument('--camera-calib', type=str,  nargs='?', const='camera/config.xml', default='camera/config.xml', help='The path to the camera calibration file, relative to the data directory root.')
parser.add_argument('--left-video', type=str,  nargs='?', const='left.avi', default='left.avi', help='The path to the left video file, relative to the data directory root.')
parser.add_argument('--right-video', type=str,  nargs='?', const='right.avi', default='right.avi', help='The path to the right video file, relative to the data directory root.')
parser.add_argument('--classifier-config', nargs='?', type=str, const='classifier/config.xml', default='classifier/config.xml', help='The path to the classifier configuration file, relative to the data directory root.')
parser.add_argument('--trackable-pose-files', nargs='+', type=str, help='Set the path to the files which contains the starting poses for each trackable object, this should be an SE3 file.', required=True)

args = parser.parse_args()

args.ttrack_dir = clean_dir_end(clean_win_path(args.ttrack_dir))
args.data_dir = clean_dir_end(clean_win_path(args.data_dir))


args.trackable_cfg = [clean_win_path(f) for f in args.trackable_cfg]
  
d = TTrackAppCfg(args.data_dir, args.ttrack_dir, args.left_video, args.right_video, args.camera_calib, (args.win_width,args.win_height),  "left_output.avi", "right_output.avi", args.classifier_config, args.classifier_type, args.localizer_type, args.trackable_cfg, args.trackable_pose_files)
d.create()