from overlay import StereoOverlay
import argparse

parser = argparse.ArgumentParser(description="Overlay tracking pose data on a video file.")
parser.add_argument("left_video",type=str,help="The video file to overlay on.")
parser.add_argument("right_video",type=str,help="The video file to overlay on.")
parser.add_argument("tracking_data",type=str,help="The tracking data file. Each line should correspond to a frame pose in the format x, y, z, r1, r2, r3 where the rotation is a vector from Rodrigues formula.")
parser.add_argument("camera_calib",type=str,help="Camera calibration file in the OpenCV XML format.")
args = parser.parse_args()

#o = Overlay(args.video,args.tracking_data,args.camera_calib,args.model,True)
o = StereoOverlay(args.left_video, args.right_video,args.tracking_data,args.camera_calib)

o.plot_to_window()