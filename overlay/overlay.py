import cv2
from ..camera.camera import MonocularCamera, StereoCamera
import matplotlib.pyplot as plt
import numpy as np

class Point(object):

  def __init__(self,vertex,neighbors):
    self.vertex = vertex
    self.neighbors = neighbors


class Model(object):

  def __init__(self):
    
    self.points = []
    
    self.points.append( Point(np.asarray([5,0,0]),[1]) )
    self.points.append( Point(np.asarray([-5,0,0]),[0]) )
    
    self.points.append( Point(np.asarray([0,2,0]),[3]) )
    self.points.append( Point(np.asarray([0,-2,0]),[2]) )
    
    self.points.append( Point(np.asarray([0,0,2]),[5]) )
    self.points.append( Point(np.asarray([0,0,-2]),[4]) )


      
class StereoOverlay(object):

  def __init__(self, left_video_url, right_video_url, pose_url, calib_url):
    
    self.left_capture = cv2.VideoCapture(left_video_url)
    self.right_capture = cv2.VideoCapture(right_video_url)
    
    if not self.left_capture.isOpened():
      raise Exception("Error, could not open the capture at: " + left_video_url)
    if not self.right_capture.isOpened():
      raise Exception("Error, could not open the capture at: " + right_video_url)
    
    self.camera = StereoCamera(calib_url)
    self.poses = self.parse_pose_file(pose_url)
    self.model = Model()
  
  def parse_pose_file(self,pose_url):
    
    with open(pose_url,'r') as f:
      poses = f.readlines() 
    return poses
    
  def plot_to_video(self):    
    pass
    
  def plot_to_window(self):
  
    #fig = plt.figure()
    cv2.namedWindow("left window")
    cv2.namedWindow("right window")
    
    for l_im, r_im in self._plot_to_image():
    
      n_im = cv2.resize(l_im, tuple(reversed(map( lambda x: int(float(x)/3), l_im.shape[0:2] ) )))  
      cv2.imshow("left window",n_im)
      
      n_im = cv2.resize(r_im, tuple(reversed(map( lambda x: int(float(x)/3), r_im.shape[0:2] ) )))
      cv2.imshow("right window",n_im)
    
      key = cv2.waitKey(40)
      if key == ' ':
        break

  
  def _plot_to_image(self):
  
    for i in range(10): #there is a capture offset
      
      self.left_capture.read()
      self.right_capture.read()

    self.first = True
    
    #for pose in self.poses[146:-1]:#[5:-1]:
    for i in xrange(0,len(self.poses),1):
      pose = self.poses[i]      
      pose = self.parse_pose(pose)
      left_frame = self.left_capture.read()[1]
      right_frame = self.right_capture.read()[1]
      
      yield self._draw_on_frame(left_frame,right_frame,pose) 
  
  def _draw_on_frame(self,left_frame,right_frame,pose):
  
    transformed_points = self._transform_model(pose)
    
    for point in transformed_points:
      
      left_projected_point,right_projected_point = self.camera.project(point.vertex.reshape(1,3))
      
      for neighbor_index in point.neighbors:
      
        neighbor = transformed_points[neighbor_index]
        left_projected_neighbor,right_projected_neighbor = self.camera.project(neighbor.vertex.reshape(1,3))


        left_projected_point = left_projected_point.reshape(2).astype(np.int32)
        right_projected_point = right_projected_point.reshape(2).astype(np.int32)
        left_projected_neighbor = left_projected_neighbor.reshape(2).astype(np.int32)
        right_projected_neighbor = right_projected_neighbor.reshape(2).astype(np.int32)
    
        #note projected_pint,projected_neightbor need to be tuples
        cv2.line(left_frame,tuple(left_projected_point),tuple(left_projected_neighbor),(255,12,15),1,cv2.LINE_AA)
        
        cv2.line(right_frame,tuple(right_projected_point),tuple(right_projected_neighbor),(255,12,15),1,cv2.LINE_AA)
        
    return left_frame,right_frame 
      
      
  
  def _transform_model(self, pose):
  
    
    if self.first == True:
      self.start_pose = pose
      self.first = False
      
      
    #rotation_matrix,jacs = cv2.Rodrigues(np.asarray([pose[3]+1.1,pose[4],pose[5]-0.4]))
    try:
      rotation_matrix,jacs = cv2.Rodrigues(np.asarray([pose[3],pose[4],pose[5]]))
    except IndexError: #ie we don't have rotations
      rotation_matrix = np.eye(3)
    translation = np.asarray(pose[0:3])# - np.asarray([self.start_pose[0],self.start_pose[1],0])
    
    translation = translation + np.asarray([-5,-3,18])
    
    transformed_points = []
    
    for point in self.model.points:
    
      vertex = np.dot(rotation_matrix,point.vertex) + translation# + np.asarray([20.4,-18.5,0])
      transformed_points.append( Point(vertex, point.neighbors ) )
    
    return transformed_points
   
  def parse_pose(self,pose):
  
    return map(float,pose.strip("\n").split(","))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

      
class Overlay(object):

  def __init__(self, video_url, pose_url, calib_url, ):
      
    self.capture = cv2.VideoCapture(video_url)
    
    if not self.capture.isOpened():
      raise Exception("Error, could not open the capture at: " + video_url)
    
    self.camera = MonocularCamera(calib_url)
    
    self.poses = self.parse_pose_file(pose_url)
    self.model = Model()
    
  def parse_pose_file(self,pose_url):
    
    with open(pose_url,'r') as f:
      self.poses = f.readlines()
    
    return self.poses
    
  def plot_to_video(self):    
    pass
    
  def plot_to_window(self):
  
    #fig = plt.figure()
    cv2.namedWindow("window")
    
    for im in self._plot_to_image():
    
      n_im = cv2.resize(im, tuple(reversed(map( lambda x: int(float(x)/3), im.shape[0:2] ) )))
    
      cv2.imshow("window",n_im)
    
      key = cv2.waitKey(10)
      if key == ' ':
        break

  
  def _plot_to_image(self):
  
    for i in range(10): #there is a capture offset
      
      self.capture.read()
  
    self.first = True
    
    for pose in self.poses:#[5:-1]:
      
      pose = self.parse_pose(pose)
      frame = self.capture.read()[1]
      
      yield self._draw_on_frame(frame,pose)
  
  def _draw_on_frame(self,frame,pose):
  
    transformed_points = self._transform_model(pose)
    
    for point in transformed_points:
      
      projected_point = self.camera.project(point.vertex.reshape(1,3))
      
      for neighbor_index in point.neighbors:
      
        neighbor = transformed_points[neighbor_index]
        projected_neighbor = self.camera.project(neighbor.vertex.reshape(1,3))

        projected_point = projected_point.reshape(2).astype(np.int32)
        projected_neighbor = projected_neighbor.reshape(2).astype(np.int32)     
        #note projected_pint,projected_neightbor need to be tuples
        cv2.line(frame,tuple(projected_point),tuple(projected_neighbor),(255,12,15),1,cv2.LINE_AA)
        
    return frame    
      
      
  
  def _transform_model(self, pose):
  
    
    if self.first == True:
      self.start_pose = pose
      self.first = False
      
      
    #rotation_matrix,jacs = cv2.Rodrigues(np.asarray([pose[3]+1.1,pose[4],pose[5]-0.4]))
    rotation_matrix,jacs = cv2.Rodrigues(np.asarray([pose[3],pose[4],pose[5]]))
    translation = np.asarray(pose[0:3]) - np.asarray([self.start_pose[0],self.start_pose[1],0])
    
    transformed_points = []
    
    for point in self.model.points:
    
      vertex = np.dot(rotation_matrix,point.vertex) + translation# + np.asarray([20.4,-18.5,0])
      transformed_points.append( Point(vertex, point.neighbors ) )
    
    return transformed_points
   
  def parse_pose(self,pose):
  
    return map(float,pose.strip("\n").split(","))
    