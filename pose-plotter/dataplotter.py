"""DataPlotter.py 
A utility for producing 3D plots from calibrated tracking data.
Copyright (C) 2013 Max Allan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>."""
    
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import numpy as np
import abc
import scipy.signal
import cv2

class DataPlotter(object):

  def __init__(self,subplot):
    __metaclass__ = abc.ABCMeta
    self.subplot = subplot
    
  @abc.abstractmethod
  def setup(self,**kwargs):
    return
  
  @abc.abstractmethod
  def refresh_plot(self):
    return
    
  @abc.abstractmethod
  def plot(self):
    return
    
  def _init_plot(self):
    return
   
  @abc.abstractmethod
  def _animate_plot(self,i):
    return
    
class PosePlotter3D(DataPlotter):

  def __init__(self,estimated_pose_data,ground_truth_data,subplot):
    super(PosePlotter3D,self).__init__(subplot)
    self.estimated_pose_data = self.parse_pose_file(estimated_pose_data,normalize=True)
    self.ground_truth_data = self.parse_pose_file(ground_truth_data,normalize=True)
    
  def parse_pose_file(self,pose_file,normalize=False,med_filt=False,kernel_width=5):
    """Load in the pose data from the input files. Optionally clean the data up with a 1D 
    median filter and/or offset the data to start at (0,0,0,0,0,0)
    """    
    with open(pose_file,'r') as f:
      
      points =  np.asarray(map(lambda x: map(float, x.strip("\n").split(',')),f.readlines()))
            
      #median filter the point with a kernel of width kernel_width 
      #1D filters work better
      if med_filt:
        for dof in range(6):
          points[:,dof] = scipy.signal.medfilt(points[:,dof],kernel_width)

      #force the plot to start from (0,0,0,0,0,0)
      if normalize:
        points[:,3:6] = points[:,3:6] - points[200,3:6]

      return points
  
  def setup(self, **kwargs):

    self.title = kwargs.get("title","")
 
    #if the user does not specify the range for the plots just bound them with the max,min of the data
    self.xrange = kwargs.get("xrange",(min(min(self.estimated_pose_data[:,0]),min(self.ground_truth_data[:,0])), 
                                       max(max(self.estimated_pose_data[:,0]),max(self.ground_truth_data[:,0]))) )
    self.yrange = kwargs.get("yrange",(min(min(self.estimated_pose_data[:,1]),min(self.ground_truth_data[:,1])), 
                                       max(max(self.estimated_pose_data[:,1]),max(self.ground_truth_data[:,1]))) )
    self.zrange = kwargs.get("zrange",(min(min(self.estimated_pose_data[:,2]),min(self.ground_truth_data[:,2])), 
                                       max(max(self.estimated_pose_data[:,2]),max(self.ground_truth_data[:,2]))) )

    self.units = kwargs.get("units","mm")     
    self.xlabel = "x position ({0})".format(self.units)
    self.ylabel = "y position ({0})".format(self.units)
    self.zlabel = "z position ({0})".format(self.units)
    
    self.subplot.set_title(self.title) #BUG: location of title moves if reset in refresh plot
    #self.subplot.legend(loc="upper right")
    self.subplot.set_xlabel( self.xlabel )
    self.subplot.set_ylabel( self.ylabel )
    self.subplot.set_zlabel( self.zlabel )
    self.refresh_plot()

  def refresh_plot(self):
  
    self.subplot.legend(loc="upper right")
    self.subplot.set_xlim3d( self.xrange[0], self.xrange[1] )
    self.subplot.set_ylim3d( self.yrange[0], self.yrange[1] )
    self.subplot.set_zlim3d( self.zrange[0], self.zrange[1] )  
    
  def plot(self,i):
    
    while 1:
      try:
        line = self.subplot.lines.pop(0)
        del line
      except:
        break
    
    self.plot_data( self.estimated_pose_data, "estimated", "red" , i)
    self.plot_data( self.ground_truth_data, "ground truth", "blue", i)
    self.draw_camera()
    
  def draw_camera(self):
    camera_width = 2
    camera_height = 2
    camera_depth = 6 #make this larger as axes scale
    self.subplot.plot(xs = [0,camera_width],ys = [0,camera_height],zs = [0,camera_depth], color="black")
    self.subplot.plot(xs = [0,-camera_width],ys = [0,camera_height],zs = [0,camera_depth], color="black")
    self.subplot.plot(xs = [0,camera_width],ys = [0,-camera_height],zs = [0,camera_depth], color="black")
    self.subplot.plot(xs = [0,-camera_width],ys = [0,-camera_height],zs = [0,camera_depth], color="black")
    self.subplot.plot(xs = [camera_width,-camera_width],ys = [camera_height,camera_height],zs = [camera_depth,camera_depth], color="black")
    self.subplot.plot(xs = [camera_width,camera_width],ys = [camera_height,-camera_height],zs = [camera_depth,camera_depth], color="black")
    self.subplot.plot(xs = [-camera_width,-camera_width],ys = [-camera_height,camera_height],zs = [camera_depth,camera_depth], color="black")
    self.subplot.plot(xs = [-camera_width,camera_width],ys = [-camera_height,-camera_height],zs = [camera_depth,camera_depth], color="black")
    
    
  def plot_data(self, dataset, line_label, line_color, i):
  
    rotation,jacs = cv2.Rodrigues( dataset[i,3:6] )

    start = np.dot(rotation,np.asarray([-2,0,0])) + dataset[i,0:3]
    end = np.dot(rotation,np.asarray([5,0,0])) + dataset[i,0:3]

    top = np.dot(rotation,np.asarray([0,1,0])) + dataset[i,0:3]
    bottom = np.dot(rotation,np.asarray([0,-1,0])) + dataset[i,0:3]

    left = np.dot(rotation,np.asarray([0,0,1])) + dataset[i,0:3]
    right = np.dot(rotation,np.asarray([0,0,-1])) + dataset[i,0:3]

    x = self.subplot.plot(xs = [start[0],dataset[i,0],end[0]],
                          ys = [start[1],dataset[i,1],end[1]],
                          zs = [start[2],dataset[i,2],end[2]],
                          label=line_label,
                          color=line_color)
            
    y = self.subplot.plot(xs = [bottom[0],dataset[i,0],top[0]],
                          ys = [bottom[1],dataset[i,1],top[1]],
                          zs = [bottom[2],dataset[i,2],top[2]],
                          #label=line_label,
                          color=line_color)
            
    z = self.subplot.plot(xs = [left[0],dataset[i,0],right[0]],
                          ys = [left[1],dataset[i,1],right[1]],
                          zs = [left[2],dataset[i,2],right[2]],
                          #label=line_label,
                          color=line_color)
    

          
class PosePlotter2D(DataPlotter):
  
  def __init__(self,estimated_pose_data,ground_truth_data,subplot):
  
    super(PosePlotter2D,self).__init__(subplot)
    self.estimated_pose_data = self.parse_pose_file(estimated_pose_data,normalize=True)
    self.ground_truth_data = self.parse_pose_file(ground_truth_data,normalize=True)
  
  def parse_pose_file(self,pose_file,normalize=False,med_filt=False,kernel_width=5):
    """Load in the pose data from the input files. Optionally clean the data up with a 1D 
    median filter and/or offset the data to start at (0,0,0)
    """    
    with open(pose_file,'r') as f:

      points =  np.asarray(map(lambda x: map(float, x.strip("\n").split(',')),f.readlines()))
            
      #median filter the point with a kernel of width kernel_width 
      #1D filters work better
      if med_filt:
        for dof in range(3):
          points[:,dof] = scipy.signal.medfilt(points[:,dof],kernel_width)

      #force the plot to start from (0,0,0)
      if normalize:
        points = points - points[0,:]
      return points
      
  def setup(self,**kwargs):
    
    self.title = kwargs.get("title","2D Pose Plot")
 
    #if the user does not specify the range for the plots just bound them with the max,min of the data
    self.xrange = kwargs.get("xrange",(min(min(self.estimated_pose_data[:,0]),min(self.ground_truth_data[:,0])), 
                                       max(max(self.estimated_pose_data[:,0]),max(self.ground_truth_data[:,0]))) )
    self.yrange = kwargs.get("yrange",(min(min(self.estimated_pose_data[:,1]),min(self.ground_truth_data[:,1])), 
                                       max(max(self.estimated_pose_data[:,1]),max(self.ground_truth_data[:,1]))) )
    

    self.units = kwargs.get("units","mm")     
    self.xlabel = "x position ({0})".format(self.units)
    self.ylabel = "y position ({0})".format(self.units)
    
    self.subplot.set_title(self.title) #BUG: location of title moves if reset in refresh plot
    self.subplot.set_xlabel( self.xlabel )
    self.subplot.set_ylabel( self.ylabel )
    self.subplot.legend(loc="upper right")
    self.refresh_plot()
  
  def refresh_plot(self):
    
    self.subplot.set_xlim( self.xrange[0], self.xrange[1] )
    self.subplot.set_ylim( self.yrange[0], self.yrange[1] )

  def plot(self,i):
    raise NotImplementedError()
  
class ImagePlotter(DataPlotter):

  def __init__(self,datafile,subplot):
    super(ImagePlotter,self).__init__(subplot)
    self.datafile = datafile
    
  def setup(self,**kwargs):
  
    self.title = kwargs.get("title","")
    self.capture = cv2.VideoCapture(self.datafile)
    if not self.capture.isOpened():
      raise Exception("Error, could not open capture from file: " + self.datafile)
    
    self.subplot.axes.get_xaxis().set_visible(False)
    self.subplot.axes.get_yaxis().set_visible(False)
    self.subplot.set_title(self.title)
    self.refresh_plot()
    
  def refresh_plot(self):
    return    
    
  def plot(self,i):
    im = self.capture.read()[1]
    resiz = np.ndarray( shape=(640,480,3), dtype=np.uint8 )
    resiz = cv2.resize(im,resiz.shape[0:2])
    self.subplot.imshow(cv2.cvtColor(resiz,cv2.cv.CV_BGR2RGB) )