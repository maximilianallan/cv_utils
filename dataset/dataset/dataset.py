import os,sys,subprocess
import cv_utils.davinci.parse as parse
import cv_utils.split.split as split
import re
import shutil

def is_float(number):

  try:
    float(number)
    return True
  except:
    return False

def clear_directory(folder):

  for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
          os.unlink(file_path)
        elif os.path.isdir(file_path):
          shutil.rmtree(file_path, ignore_errors=True)          
    except Exception, e:
        print e



def check_output_dir(output_dir_path):

  if not os.path.exists(output_dir_path):
    os.mkdir(output_dir_path)
    return

  files = os.listdir(output_dir_path)
  if files == []:
    return

  input = raw_input("Output directory is not empty, empty directory and continue? (y/n) ")
  while True:
    if input.lower() == "y":
      #[shutil.rmtree(output_dir_path + "/" + file) for file in files]
      clear_directory(output_dir_path)
      return
    elif input.lower() == "n":
      sys.exit(0)
    else:
      input = raw_input("Unrecognised input. Please enter y to empty directory and continue and n to exit. ")
          

def clean_dir_end(path):

  if path[-1] != '/':
    path = path + '/'
    
  return path
          
def clean_win_path(win_path):

  return win_path.replace("\\","/")


def add_trk_cfg(root_dir, joint, model_file = None, arm_offsets = None, base_offsets = None):
  
  root_dir = root_dir.replace("\\","/")
  
  if not joint in ["PSM1", "PSM2", "PSM3", "ECM"]:
    raise Exception("Error, joint id: {0} is invalid.\n".format(joint))
  
  if model_file is None:
    model_file = "fake"
    if joint is not "ECM":
      raise Exception("Null model file only valid for ECM.\n")
      
  elif not os.path.exists(model_file):
    raise Exception("Model file: {0} does not exist.\n".format(model_file))
  
  else:
    model_file = clean_win_path(model_file)
  
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
    

def process_raw_data(raw_data_dir, rigid_only, interpolate, split_video, use_psm1, use_psm2, classic_capture):

  cwd = os.getcwd()
  
  os.chdir(raw_data_dir)
  
  files = os.listdir(".")
    
    
  if split_video:
  
    video_file = filter(lambda x : os.path.splitext(x)[1] == ".avi", files)[0]
    split.split_video(video_file)
  
  if use_psm1:
    psm1_files = filter(lambda x : len(re.findall("psm1",x,re.IGNORECASE)) == 1, files)
    if classic_capture:
      if len(psm1_files) != 1:
        raise Exception("Could not find the correct number of psm1 files in the raw data directory!\n")
    else:
      if len(psm1_files) != 2:
        raise Exception("Could not find the correct number of psm1 files in the raw data directory!\n")
        
    psm1_suj_file = filter(lambda x : len(re.findall("capture",x,re.IGNORECASE)) == 1, psm1_files)[0]
    if classic_capture:
      psm1_j_file = psm1_suj_file
      parse.run_classic(psm1_suj_file, "psm1_suj.txt", "psm1_j.txt")
    else:
      psm1_j_file = [j for j in psm1_files if j != psm1_suj_file][0]
      parse.run_dvrk(psm1_suj_file, psm1_j_file, "psm1_suj.txt", "psm1_j.txt", len(open(psm1_j_file,"r").readlines()), False)
  
  if use_psm2:
    psm2_files = filter(lambda x : len(re.findall("psm2",x,re.IGNORECASE)) == 1, files)  
    if classic_capture:
      if len(psm2_files) != 1:
        raise Exception("Could not find the correct number of psm2 files in the raw data directory!\n")
    else:
      if len(psm2_files) != 2:
        raise Exception("Could not find the correct number of psm2 files in the raw data directory!\n")
        
    psm2_suj_file = filter(lambda x : len(re.findall("capture",x,re.IGNORECASE)) == 1, psm2_files)[0]
    if classic_capture:
      psm2_j_file = psm2_suj_file
      parse.run_classic(psm2_j_file, "psm2_suj.txt", "psm2_j.txt")
    else:
      psm2_j_file = [j for j in psm2_files if j != psm2_suj_file][0]
      parse.run_dvrk(psm2_suj_file, psm2_j_file, "psm2_suj.txt", "psm2_j.txt", len(open(psm2_j_file,"r").readlines()), False)  
  
  
  ecm_file = filter(lambda x : len(re.findall("ecm",x,re.IGNORECASE)) == 1, files)
  if len(ecm_file) != 1:
    raise Exception("Could not find the ecm file in the raw data directory!\n")
    
  if classic_capture:
    parse.run_classic(ecm_file[0], "ecm_suj.txt", "ecm_j.txt")
  else:
    parse.run_dvrk(ecm_file[0], ecm_file[0], "ecm_suj.txt", "ecm_j.txt", len(open(psm1_j_file,"r").readlines()), True)
   
  os.chdir(cwd)
  
  return (os.path.join(raw_data_dir, "left.avi"),
          os.path.join(raw_data_dir, "right.avi"),
          os.path.join(raw_data_dir, "psm1_suj.txt"),
          os.path.join(raw_data_dir, "psm1_j.txt"),
          os.path.join(raw_data_dir, "psm2_suj.txt"),
          os.path.join(raw_data_dir, "psm2_j.txt"),
          #os.path.join(raw_data_dir, "psm3_suj.txt"),
          #os.path.join(raw_data_dir, "psm3_j.txt"),
          os.path.join(raw_data_dir, "ecm_suj.txt"),
          os.path.join(raw_data_dir, "ecm_j.txt")
         )
  

class Trackables(object):

  LND = 1 #Large Needle Driver
  
  @staticmethod
  def convert_trackable(trackable):
    if trackable == "LND":
      return Trackables.LND
    else:
      raise Exception("Invalid trackable id: " + trackable)

class BasicAppCfg(object):

  def __init__(self, root_dir, output_dir, left_input_video, right_input_video, camera_cfg_file, window_dims, left_output_video, right_output_video):
  
    self.root_dir = self.check_file(root_dir)
    check_output_dir(output_dir)
    self.output_dir = output_dir
    self.left_input_video = self.check_file(left_input_video, root_dir)
    self.right_input_video = self.check_file(right_input_video, root_dir)
    self.camera_cfg_file = self.check_file(camera_cfg_file, root_dir)
    self.window_dims = window_dims
    self.left_output_video = left_output_video
    self.right_output_video = right_output_video
    
  def check_file(self, filepath, root=None):
    
    if filepath is None:
       return filepath
    
    if root is None:
      root = ""
    
    if os.path.exists(os.path.join(root,filepath)):
      return filepath
    else:
      raise Exception("Error, file: " + os.path.join(root,filepath) + " doesn't exist")

      
class TTrackAppCfg(BasicAppCfg):

  def __init__(self, root_dir, output_dir, left_input_video, right_input_video, camera_cfg_file, window_dims, left_output_video, right_output_video, classifier_cfg_file, classifier_type, localizer_type, trackable_cfg_files, trackable_starting_poses):
    
    """
    right now we assume the starting pose is identity/home
    """
    super(TTrackAppCfg, self).__init__(root_dir, output_dir, left_input_video, right_input_video, camera_cfg_file, window_dims, left_output_video, right_output_video)
    
    self.classifier_cfg_file = self.check_file(classifier_cfg_file, root_dir)
    self.classifier_type = self.check_classifier_type(classifier_type)
    self.trackable_cfg_files = [clean_win_path(self.check_file(fl)) for fl in trackable_cfg_files]
    self.localizer_type = self.check_localizer_type(localizer_type)
    self.trackable_starting_poses = trackable_starting_poses
    
  def create(self):
  
    with open(self.output_dir + "/app.cfg","w") as f:
      
      f.write("# Root directory\n")
      f.write("root-dir={0}\n".format(self.root_dir))
      f.write("output-dir={0}\n".format(self.output_dir))
      f.write("\n# Input video files\n")
      f.write("left-input-video={0}\n".format(self.left_input_video))
      f.write("right-input-video={0}\n".format(self.right_input_video))
      f.write("\n# Camera/window config\n")
      f.write("camera-config={0}\n".format(self.camera_cfg_file))
      f.write("window-width={0}\n".format(self.window_dims[0]))
      f.write("window-height={0}\n".format(self.window_dims[1]))
      f.write("\n#Localizer \n")
      f.write("localizer-type={0}\n".format(self.localizer_type))
      f.write("\n# Detector \n")
      f.write("classifier-config={0}\n".format(self.classifier_cfg_file))
      f.write("classifier-type={0}\n".format(self.classifier_type))
      if self.classifier_type == "MCRF":
        f.write("num-labels=3\n")
      else:
        f.write("num-labels=2\n")
        
      f.write("\n# Trackables \n")
      for n,trck_file in enumerate(self.trackable_starting_poses):
        if n == 0:
          f.write("trackable={0}\n".format(self.trackable_cfg_files[0])) #only support one now
        #f.write("starting-pose-{0}=1 0 0 0 0 1 0 0 0 0 1 60 0 0 0 0\n".format(n))
        f.write("starting-pose-{0}={1}\n".format(n, self.get_starting_pose(self.trackable_starting_poses[n])))
        
      f.write("\n# Outputs \n")
      f.write("left-output-video={0}\n".format(self.left_output_video))
      f.write("right-output-video={0}\n".format(self.right_output_video))
      
  def check_classifier_type(self, classifier_type):
  
    if classifier_type == "RF" or classifier_type == "SVM" or classifier_type == "NB" or classifier_type == "MCRF":
      return classifier_type
    else:
      raise Exception("Error, " + classifier_type + " is not valid!\n")
      
  def check_localizer_type(self, localizer_type):
  
    if localizer_type == "PWP3D" or localizer_type == "ArticulatedComponentLS" or localizer_type == "CompLS":
      return localizer_type
    else:
      raise Exception("Error, " + localizer_type + " is not valid!\n")
      
      
  def get_starting_pose(self, starting_pose_file):
  
    rval = "1 0 0 0 0 1 0 0 0 0 1 60 0 0 0"
    with open(starting_pose_file, 'r') as f:
        
      try:
        l = f.readlines()
  
        l = l[0:8]
        l = [line.strip("\n").strip("|") for line in l]
        l = [line.split(" ") for line in l]
        se3_pose = [val for val in l[0] if is_float(val)] + [val for val in l[1] if is_float(val)] + [val for val in l[2] if is_float(val)]
        arti_pose = [v[0] for v in l[-3:]]
        
        pose = se3_pose + arti_pose
        
        if len(pose) != 15:
          raise Exception("")
        
        rval = " ".join(pose)
                
      except:
        print ("Error setting pose automatically from SE3 file. Set this manually.")
        pass
        
  
    return rval
  
class VizAppCfg(BasicAppCfg):

  def __init__(self, root_dir, output_dir, left_input_video, right_input_video, camera_cfg_file, window_dims, left_output_video, right_output_video, viz_dims, num_trackables ):

    """
    right now we assume the starting pose is identity/home
    """
    super(VizAppCfg, self).__init__(root_dir, output_dir, left_input_video, right_input_video, camera_cfg_file, window_dims, left_output_video, right_output_video)
    
    self.num_trackables = num_trackables
    
    self.viz_dims = viz_dims
    if not len(self.viz_dims) == 2:
      raise Exception("Error, a width and height for the viz window was not selected.\n")
  
  def create(self):
    
    with open(self.output_dir + "/app.cfg","w") as f:
      
      f.write("# Root directory\n")
      f.write("root-dir={0}\n".format(self.root_dir))
      f.write("output-dir={0}\n".format(self.output_dir))
      f.write("\n# Input video files\n")
      f.write("left-input-video={0}\n".format(self.left_input_video))
      f.write("right-input-video={0}\n".format(self.right_input_video))
      f.write("\n# Camera/window config\n")
      f.write("camera-config={0}\n".format(self.camera_cfg_file))
      f.write("window-width={0}\n".format(self.window_dims[0]))
      f.write("window-height={0}\n".format(self.window_dims[1]))
      f.write("viz-width={0}\n".format(self.viz_dims[0]))
      f.write("viz-height={0}\n".format(self.viz_dims[1]))
      f.write("\n# Trackables \n")
      f.write("moveable-camera={0}\n".format("trackables/cam/trk.cfg")) #should be relative     
      for n in range(self.num_trackables):
        f.write("trackable-{0}=trackables/psm{1}/trk.cfg\n".format(n,n+1))
      f.write("\n# Outputs \n")
      f.write("left-output-video={0}\n".format(self.left_output_video))
      f.write("right-output-video={0}\n".format(self.right_output_video))
    
  
  #@property
  #def num_trackables(self):
  #  try:
  #    return len(self.trackables)
  #  except:
  #    return 0
  
  #def check_trackables(self,trackables):
  
  #  return [ Trackables.convert_trackable(t) for t in trackables]
        
  
    
  
  