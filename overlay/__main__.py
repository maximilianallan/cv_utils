from overlay import Overlay
import argparse

parser = argparse.ArgumentParser(description="Overlay tracking pose data on a video file.")
parser.add_argument("video",type=str,help="The video file to overlay on.")
parser.add_argument("tracking_data",type=str,help="The tracking data file. Each line should correspond to a frame pose in the format x, y, z, r1, r2, r3 where the rotation is a vector from Rodrigues formula.")
parser.add_argument("camera_calib",type=str,help="Camera calibration file in the OpenCV XML format.")
parser.add_argument("model",type=str,help="A 3D point file containing the data for the model.")
args = parser.parse_args()

o = Overlay(args.video,args.tracking_data,args.camera_calib,args.model,True)

o.plot_to_window()