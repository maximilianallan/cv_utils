import numpy as np
import abc
import cv2

class BaseCamera(object):
  
  def __init__(self):
    __metaclass__ = abc.ABCMeta
    
  def project(self, world_point):
    raise NotImplementedError
    
  def unproject(self, pixel):
    pass
    
  def load_from_calibration_file(self):
    raise NotImplementedError

  def str_to_mat(self,string):
    
    s = [ f for f in string.split("\n") if len(f) > 0 ]
    s = [ f.split(" ") for f in s ]
    for l in s:
      try:
        l.remove("")
      except ValueError:
        pass
   
    rows = len(s)
    cols = len(s[0])
   
    s = [ map(float,f) for f in s ]
    return np.asarray(s)

   
class MonocularCamera(BaseCamera):

  def __init__(self,calibration_file=None,intrinsic_parameters=None,distortion_parameters=None):
    super(MonocularCamera,self).__init__()
    
    if calibration_file is not None:
      self.load_from_calibration_file(calibration_file)
    
    elif intrinsic_parameters is not None and distortion_parameters is not None:
      self.camera_matrix = intrinsic_parameters
      self.distortion_parameters = distortion_parameters
      
    else:
      raise Exception("Error, must either supply calibration file or parameters!")
    
  def load_from_calibration_file(self,calibration_file):
    from xml.dom import minidom
    xmldoc = minidom.parse(calibration_file)
    self.camera_matrix = self.str_to_mat( xmldoc.getElementsByTagName("Camera_Matrix")[0].getElementsByTagName("data")[0].childNodes[0].nodeValue )
    self.distortion_parameters = self.str_to_mat( xmldoc.getElementsByTagName("Distortion_Coefficients")[0].getElementsByTagName("data")[0].childNodes[0].nodeValue )
  
  def project(self, world_point):
    
    return cv2.projectPoints(world_point,np.eye(3),np.zeros(shape=(3,1),dtype=np.float64),self.camera_matrix,self.distortion_parameters)[0]
   
  def __str__(self):
    return "Monocular camera"
    
class StereoCamera(BaseCamera):

  def __init__(self,calibration_file):
    super(StereoCamera,self).__init__()
    
    self.load_from_calibration_file(calibration_file)
  
  
  def __str__(self):
    return "Stereo camera"
 
  def load_from_calibration_file(self,calibration_file):
    from xml.dom import minidom
    xmldoc = minidom.parse(calibration_file)
    self.extrinsic_camera_rotation = self.str_to_mat( xmldoc.getElementsByTagName("Extrinsic_Camera_Rotation")[0].getElementsByTagName("data")[0].childNodes[0].nodeValue )
    self.extrinsic_camera_translation = self.str_to_mat( xmldoc.getElementsByTagName("Extrinsic_Camera_Translation")[0].getElementsByTagName("data")[0].childNodes[0].nodeValue )
    
    left_cam =  self.str_to_mat( xmldoc.getElementsByTagName("Left_Camera_Matrix")[0].getElementsByTagName("data")[0].childNodes[0].nodeValue )
    left_dist = self.str_to_mat( xmldoc.getElementsByTagName("Left_Distortion_Coefficients")[0].getElementsByTagName("data")[0].childNodes[0].nodeValue )
    self.left_eye = MonocularCamera(intrinsic_parameters=left_cam,distortion_parameters=left_dist)
    
    right_cam =  self.str_to_mat( xmldoc.getElementsByTagName("Right_Camera_Matrix")[0].getElementsByTagName("data")[0].childNodes[0].nodeValue )
    right_dist = self.str_to_mat( xmldoc.getElementsByTagName("Right_Distortion_Coefficients")[0].getElementsByTagName("data")[0].childNodes[0].nodeValue )
    self.right_eye = MonocularCamera(intrinsic_parameters=right_cam,distortion_parameters=right_dist)