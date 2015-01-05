import os,sys,subprocess
import cv_utils.davinci.parse as parse
import cv_utils.split.split as split
import re

def add_trk_cfg(root_dir, joint, model_file = None, arm_offsets = None, base_offsets = None):
  
  if not joint in ["PSM1", "PSM2", "PSM3", "ECM"]:
    raise Exception("Error, joint id: {0} is invalid.\n".format(joint))
  
  if model_file is None:
    model_file = "fake"
    if joint is not "ECM":
      raise Exception("Null model file only valid for ECM.\n")
      
  elif not os.path.exists(model_file):
    raise Exception("Model file: {0} does not exist.\n".format(model_file))
  
  if arm_offsets is None:
    arm_offsets = [0] * 7
  if base_offsets is None:
    base_offsets = [0] * 6
  
  if not len(arm_offsets) == 7 or not len(base_offsets) == 6:
    raise Exception("Error, offsets are invalid.\n")
  
  with open(root_dir + "/trk.cfg", "w") as f :
  
    f.write("#" + joint + "\n\n")
    f.write("name=dh-davinci-grabber\n")
    f.write("joint={0}\n".format(joint))
    f.write("model-file={0}\n".format(model_file))
    f.write("base-joint-file={0}/{1}_suj.txt\n".format(root_dir,joint.lower()))
    f.write("arm-joint-file={0}/{1}_j.txt\n".format(root_dir,joint.lower()))
    f.write("\n#offsets\n")
    f.write("arm-offset={0}\n".format(" ".join(str(a) for a in arm_offsets)))
    f.write("base-offset={0}\n\n".format(" ".join(str(a) for a in base_offsets)))
    f.write("#Output files are given relative to output-dir\n")
    f.write("output-base-joint-file={0}_suj.txt\n".format(joint.lower()))
    f.write("output-arm-joint-file={0}_j.txt\n".format(joint.lower()))
    f.write("output-se3-file={0}_se3.txt\n".format(joint.lower()))
    

def process_raw_data(raw_data_dir, rigid_only, interpolate):

  cwd = os.getcwd()
  
  os.chdir(raw_data_dir)
  
  files = os.listdir(".")
    
  video_file = filter(lambda x : os.path.splitext(x)[1] == ".avi", files)[0]
    
  #split.split_video(video_file)
  
  psm1_file = filter(lambda x : len(re.findall("psm1",x,re.IGNORECASE)) == 1, files)[0]
  psm2_file = filter(lambda x : len(re.findall("psm2",x,re.IGNORECASE)) == 1, files)[0]
  psm3_file = filter(lambda x : len(re.findall("psm3",x,re.IGNORECASE)) == 1, files)[0]
  ecm_file = filter(lambda x : len(re.findall("ecm",x,re.IGNORECASE)) == 1, files)[0]
  
  parse.run(psm1_file, "psm1_suj.txt", "psm1_j.txt", interpolate, rigid_only)
  parse.run(psm2_file, "psm2_suj.txt", "psm2_j.txt", interpolate, rigid_only)
  parse.run(psm3_file, "psm3_suj.txt", "psm3_j.txt", interpolate, rigid_only)
  parse.run(ecm_file, "ecm_suj.txt", "ecm_j.txt", interpolate, False)
   
  os.chdir(cwd)
  
  return (os.path.join(raw_data_dir, "left.avi"),
          os.path.join(raw_data_dir, "right.avi"),
          os.path.join(raw_data_dir, "psm1_suj.txt"),
          os.path.join(raw_data_dir, "psm1_j.txt"),
          os.path.join(raw_data_dir, "psm2_suj.txt"),
          os.path.join(raw_data_dir, "psm2_j.txt"),
          os.path.join(raw_data_dir, "psm3_suj.txt"),
          os.path.join(raw_data_dir, "psm3_j.txt"),
          os.path.join(raw_data_dir, "ecm_suj.txt"),
          os.path.join(raw_data_dir, "ecm_j.txt")
         )
  

class Trackables(object):

  LND = 1 #Large Needle Driver
  
  @staticmethod
  def convert_trackables(trackable):
    if trackable == "LND":
      return Trackables.LND
    else:
      raise Exception("Invalid trackable id: " + trackable)

class BasicAppCfg(object):

  def __init__(self, root_dir, output_dir, left_input_video, right_input_video, camera_cfg_file, window_dims, left_output_video, right_output_video):
  
    self.root_dir = self.check_file(root_dir)
    self.output_dir = self.check_file(output_dir)
    self.left_input_video = self.check_file(left_input_video)
    self.right_input_video = self.check_file(right_input_video)
    self.camera_cfg_file = self.check_file(camera_cfg_file)
    self.window_dims = window_dims
    self.left_output_video = left_output_video
    self.right_output_video = right_output_video
    
  def check_file(filepath):
    
    if os.path.exists(filepath):
      return filepath
    else:
      raise Exception("Error, file: " + filepath + " doesn't exist")

      
class TTrackAppCfg(BasicAppCfg):

  def __init__(self, root_dir, output_dir, left_input_video, right_input_video, camera_cfg_file, window_dims, left_output_video, right_output_video, classifier_cfg_file, classifier_type, trackable_cfg_file ):
    
    """
    right now we assume the starting pose is identity/home
    """
    super(TTrackAppCfg, self).__init__(root_dir, output_dir, left_input_video, right_input_video_camera_cfg_file, window_dims, left_output_video, right_output_video)
    
    self.classifier_cfg_file = self.check_file(classifier_cfg_file)
    self.classifier_type = self.check_classifier_type(classifier_type)
    self.trackable_cfg_file = self.check_file(trackable_cfg_file)

  def create(self):
  
    with open(self.ttrack_ + "/app.cfg","w") as f:
      
      f.write("# Root directory\n")
      f.write("root-dir={0}\n".format(self.root_dir))
      f.write("output-dir={0}\n".format(self.output_dir))
      f.write("\n# Input video files\n")
      f.write("left-input-video={0}\n".format(self.left_output_video))
      f.write("right-output-video={0}\n".format(self.right_output_video))
      f.write("\n# Camera/window config\n")
      f.write("camera-config={0}\n".format(self.camera_cfg_file))
      f.write("window-width={0}\n".format(self.window_dims[0]))
      f.write("window-height={0}\n".format(self.window_dims[1]))
      f.write("\n# Detector \n")
      f.write("classifier-cfg={0}\n".format(self.classifier_cfg_file))
      f.write("classifier-type={0}\n".format(self.classifier_type))
      f.write("\n# Trackables \n")
      f.write("trackable={0}\n".format(self.trackable_cfg_file))
      f.write("starting-pose=1 0 0 0 0 1 0 0 0 0 1 60 0 0 0 0\n")
      f.write("\n# Outputs \n")
      f.write("left-output-video={0}\n".format(self.left_output_video))
      f.write("right-output-video={0}\n".format(self.right_output_video))

      
class VizAppCfg(BasicAppCfg):

  def __init__(self, root_dir, output_dir, left_input_video, right_input_video, camera_cfg_file, window_dims, left_output_video, right_output_video, viz_dims, camera_is_movable, camera_is_tracked, trackables ):
    
    """
    right now we assume the starting pose is identity/home
    """
    super(TTrackAppCfg, self).__init__(root_dir, output_dir, left_input_video, right_input_video_camera_cfg_file, window_dims, left_output_video, right_output_video)
    
    self.camera_is_movable = camera_is_movable
    self.camera_is_tracked = camera_is_tracked
    self.trackables = self.check_trackables(trackables)
  
  
  def create(self):
  
    with open(self.viz_dir + "/app.cfg","w") as f:
    
      pass
  
  @property
  def num_trackables(self):
    try:
      return len(self.trackables)
    except:
      return 0
  
  def check_trackables(self,trackables):
  
    return [ Trackables.convert_trackable(t) for t in trackables]
        
  
    
  
  