import cv2
from ..camera.camera import MonocularCamera
import matplotlib.pyplot as plt
import numpy as np

class Point(object):

  def __init__(self,vertex,neighbors):
    self.vertex = vertex
    self.neighbors = neighbors
  
  
    

class Model(object):

  def __init__(self,calibration_file):
    
    self.points = []
    
    self.points.append( Point(np.asarray([5,0,0]),[1]) )
    self.points.append( Point(np.asarray([-5,0,0]),[0]) )
    
    self.points.append( Point(np.asarray([0,2,0]),[3]) )
    self.points.append( Point(np.asarray([0,-2,0]),[2]) )
    
    self.points.append( Point(np.asarray([0,0,2]),[5]) )
    self.points.append( Point(np.asarray([0,0,-2]),[4]) )
    
    return
    
    with open(calibration_file,'r') as f:
    
      lines = f.readlines()
      for line in lines:
        vals = line.strip("\n").split(" ")
        self.points.append( Point( map(float,np.asarray(vals[0:3])), map(int,vals[4:len(vals)]) ) )
      
      
      
    
  


class Overlay(object):

  def __init__(self, video_url, pose_url, calib_url, model_file, stereo=False):
      
    self.capture = cv2.VideoCapture(video_url)
    
    if not self.capture.isOpened():
      raise Exception("Error, could not open the capture at: " + video_url)
    
    self.camera = MonocularCamera(calib_url)
    
    with open(pose_url,'r') as f:
      
      self.poses = f.readlines()
      
    self.model = Model(model_file)
    
  def plot_to_video(self):
  
    
    pass
    
  def plot_to_window(self):
  
    #fig = plt.figure()
    cv2.namedWindow("window")
    
    for im in self._plot_to_image():
    
      cv2.imshow("window",im)
    
      key = cv2.waitKey(200)
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
        cv2.line(frame,tuple(projected_point),tuple(projected_neighbor),(255,12,15),1,cv2.cv.CV_AA)
        
    return frame    
      
      
  
  def _transform_model(self, pose):
  
    
    if self.first == True:
      self.start_pose = pose
      self.first = False
      
      
    #rotation_matrix,jacs = cv2.Rodrigues(np.asarray([pose[3]+1.1,pose[4],pose[5]-0.4]))
    rotation_matrix,jacs = cv2.Rodrigues(np.asarray([pose[3],pose[4],pose[5]]))
    translation = np.asarray(pose[0:3]) - np.asarray([self.start_pose[0],self.start_pose[1],0])
    print translation
    
    transformed_points = []
    
    for point in self.model.points:
    
      vertex = np.dot(rotation_matrix,point.vertex) + translation# + np.asarray([20.4,-18.5,0])
      transformed_points.append( Point(vertex, point.neighbors ) )
    
    return transformed_points
   
  def parse_pose(self,pose):
  
    return map(float,pose.strip("\n").split(","))
    