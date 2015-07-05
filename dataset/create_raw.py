import argparse
import sys
from dataset.dataset import process_raw_data, add_trk_cfg, check_output_dir
import os
import shutil

def mv(infile, outdir):

  os.rename(infile, os.path.join(outdir, os.path.basename(infile)))

def mkmv(infile,outfile):

  if not os.path.exists(os.path.dirname(outfile)):
    os.makedirs(os.path.dirname(outfile))

  os.rename(infile,outfile)
  
def mk_dir_link(indir, outdir):

  if os.name == "posix":
    os.symlink(indir, outdir)
    
  elif os.name == "nt":
    import win32file
    win32file.CreateSymbolicLink(outdir, indir, 1)
    
  else:
    raise Exception("Unknown OS")
  
def mklink(infile, outdir):

  if os.name == "posix":
    os.symlink(infile, os.path.join(outdir, os.path.basename(infile)))
    
  elif os.name == "nt":
    import win32file
    win32file.CreateSymbolicLink(os.path.join(outdir, os.path.basename(infile)), infile, 0)
    
  else:
    raise Exception("Unknown OS")
    
def add_camera(cam_file, outdir):

  if not os.path.exists(outdir + "/camera"):
    os.mkdir(outdir + "/camera")
  mklink( cam_file, outdir + "/camera/" )
    
def add_classifier(classifier_file, outdir):
  
  if not os.path.exists(outdir + "/classifier"):
    os.mkdir(outdir + "/classifier")
  mklink( classifier_file, outdir + "/classifier/" )
  

parser = argparse.ArgumentParser(description='Quickly create a dataset.')
parser.add_argument('--raw-dir', type=str, help='The directory containing the raw da vinci files.', required=True)
parser.add_argument('--output-dir', type=str, help='The directory where the processed data files will be saved', required=True)
parser.add_argument('--rigid', dest='rigid_only', action="store_true", help='Only load the rigid pose parameter - i.e. ignore the articulated head.')
parser.add_argument('--psm1', action="store_true", help='Sequence contains PSM 1.')
parser.add_argument('--psm2', action="store_true", help='Sequence contains PSM 2.')
#parser.add_argument('--psm3', action="store_true", help='Sequence contains PSM 3.')
parser.add_argument("--model", type=str, help="JSON model file.")

parser.add_argument('--cam', type=str, help='Camera calibration file.')
parser.add_argument('--classifier', type=str, help='Pixel classifier file.')
parser.add_argument('--interpolate', type=int, help='Interpolate the values for smoother motion.', default=1) 

parser.add_argument('--stereo-split', action='store_true', help="Sequence recorded as a stereo feed in one file so needs splitting.")



args = parser.parse_args()

#check if the output directory exists, if not then create it.
if not os.path.exists(args.output_dir):
  os.mkdir(args.output_dir)
else:
  check_output_dir(args.output_dir)

#split the video and process the raw dv files
left_video_file, right_video_file, psm1_suj_file, psm1_j_file, psm2_suj_file, psm2_j_file, ecm_suj_file, ecm_j_file = process_raw_data(args.raw_dir, args.rigid_only, args.interpolate, args.stereo_split) 
  
#add the videos to the output directory
mklink(left_video_file, args.output_dir)
mklink(right_video_file, args.output_dir)

#add the pose data for the PSMs to the output directories and create the config files
if args.psm1:
  mkmv(psm1_suj_file, args.output_dir + "/trackables/psm1/psm1_suj.txt")
  mkmv(psm1_j_file, args.output_dir + "/trackables/psm1/psm1_j.txt")
  add_trk_cfg(args.output_dir + "/trackables/psm1/", "PSM1", args.model)
  
if args.psm2:  
  mkmv(psm2_suj_file, args.output_dir + "/trackables/psm2/psm2_suj.txt")
  mkmv(psm2_j_file, args.output_dir + "/trackables/psm2/psm2_j.txt")
  add_trk_cfg(args.output_dir + "/trackables/psm2/", "PSM2", args.model)
  
#if args.psm3:
#  mkmv(psm3_suj_file, args.output_dir + "/trackables/psm3/psm3_suj.txt")
#  mkmv(psm3_j_file, args.output_dir + "/trackables/psm3/psm3_j.txt")
#  add_trk_cfg(args.output_dir + "/trackables/psm3/", "PSM3", args.model)


#add the pose data for the ECMs to the output directories and create the config files
mkmv(ecm_suj_file, args.output_dir + "/trackables/cam/ecm_suj.txt")
mkmv(ecm_j_file, args.output_dir + "/trackables/cam/ecm_j.txt")
add_trk_cfg(args.output_dir + "/trackables/cam/", "ECM")

#add the camera configuration
if args.cam:

  add_camera(args.cam, args.output_dir)
  
#add the classifier configuration
if args.classifier:

  add_classifier(args.classifier, args.output_dir)





  
  


