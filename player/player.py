import cv2
import os
import sys
import numpy as np
import math

class VideoPlayer:

    def __init__(self, video_file, poses_file, image_file):
    
      self.poses = []
      self.frames = []
      self.current_frame = None
      self.current_pose = None
      self.index = -1
      self.MAX_VAL = 100
      self.video_file = cv2.VideoCapture(video_file)
      if not self.video_file.isOpened():
        raise Exception("Error, could not open video file\n")

      try:
        self.poses_file = open(poses_file, 'r')
      except IOError:
        raise Exception('Error, could not open pose file\n')

      self.image = cv2.imread(image_file)
      if self.image is None:
        raise Exception('Error, could not open image file\n')

    def get_current_frame(self):
    
      return self.frames[self.index]
    
    def get_current_pose(self):
    
      return self.poses[self.index]
    
    def add_new(self, frame, pose):
    
      while len(self.poses) > self.MAX_VAL:
        self.poses.pop(0)
        self.frames.pop(0)
        self.index -= 1
     
      self.poses.append(pose)
      self.frames.append(frame)
      
      self.index += 1
      
      self.current_frame = self.frames[self.index]
      self.current_pose = self.poses[self.index]
      
    def rewind(self):
    
      if self.index <= 0:
        return 
        
      self.index -= 1
      self.current_frame = self.frames[self.index]
      self.current_pose = self.poses[self.index]
      
    def forward(self):
      
      if self.index >= self.MAX_VAL or self.index >= len(self.frames) - 1:
        return self.load_new()

      self.index += 1
      self.current_frame = self.frames[self.index]
      self.current_pose = self.poses[self.index]
      return True

    def load_new(self):

      frame = self.video_file.read()
      
      if frame[0] is False:
        print "Done reading"
        return False

      frame = frame[1]

      try:

        pose = read_pose(self.poses_file)

      except Exception as e:
        print e.args
        print "Done"
        return False

      self.add_new(frame, pose)
      return True


def compare_images(image1, image2):

  if image1.shape != image2.shape or image1.dtype != image2.dtype:
    return 99999999

  height, width, channels = image1.shape

  return np.mean(np.abs(image1.astype(np.float32)-image2.astype(np.float32)))

def clean_line(pose_line):

  
  pose_line = pose_line.strip()
  pose_line = pose_line.replace("|","")
  pose_line = pose_line.strip(" ")
  vals = pose_line.split(" ")
  
  fvals = []
  for v in vals:
    try:
      fvals.append(float(v))
    except:
      pass
  
  return fvals
      
def read_pose(pose_file):

  gl_pose = np.eye(4,4,dtype=np.float32)
  a1 = 0
  a2 = 0
  a3 = 0
  
  try:
    #read 9 lines
    l1_f = pose_file.readline()
    l2_f = pose_file.readline()
    l3_f = pose_file.readline()
    
    l1 = clean_line(l1_f)
    l2 = clean_line(l2_f)
    l3 = clean_line(l3_f)
    
    pose_file.readline()
    pose_file.readline()
    
    a1_f = pose_file.readline().strip("\n")
    a2_f = pose_file.readline().strip("\n")
    a3_f = pose_file.readline().strip("\n")
    
    a1 = float(a1_f)
    a2 = float(a2_f)
    a3 = float(a3_f)
    pose_file.readline()
    
    
    gl_pose[0,:] = l1
    gl_pose[1,:] = l2
    gl_pose[2,:] = l3
  except Exception as e:
    pass

  return (gl_pose,[a1,a2,a3])

def combine_images(image1, image2):

  if image1.shape[0] != image2.shape[0] or image1.dtype != image2.dtype:
    raise Exception('Error, image dimensions or type do not match')

  if len(image1.shape) == 2:
    new_image = np.ndarray(shape=(image1.shape[0], image1.shape[1]+image2.shape[1]), dtype = image1.dtype)
  else:
    new_image = np.ndarray(shape=(image1.shape[0], image1.shape[1]+image2.shape[1], image1.shape[2]), dtype = image1.dtype)
  new_image[:,0:image1.shape[1],:] = image1
  new_image[:,image1.shape[1]:image1.shape[1]*2,:] = image2
  return new_image

  
  
  

  

