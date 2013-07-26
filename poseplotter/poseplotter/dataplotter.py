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

class DataPlotter(object):

  def __init__(self,estimated_pose_data,ground_truth_data,subplot):
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
    self.estimated_pose_data = self.parse_pose_file(estimated_pose_data)
    self.ground_truth_data = self.parse_pose_file(ground_truth_data)
    
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
        points = points - points[0,:]
      return points
  
  def setup(self, **kwargs):

    self.title = kwargs.get("title","3D Pose Plot")
 
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
 
    self.refresh_plot()

  def refresh_plot(self):
  
    self.subplot.set_title(self.title)
    self.subplot.set_xlim3d( self.xrange[0], self.xrange[1] )
    self.subplot.set_ylim3d( self.yrange[0], self.yrange[1] )
    self.subplot.set_zlim3d( self.zrange[0], self.zrange[1] )
    self.subplot.set_xlabel( self.xlabel )
    self.subplot.set_ylabel( self.ylabel )
    self.subplot.set_zlabel( self.zlabel )
    self.subplot.legend(loc="upper right")
    
  def plot(self,i):
    print i
    
    
    
    

          
class PosePlotter2D(DataPlotter):
  
  def __init__(self,estimated_pose_data,ground_truth_data,subplot):
  
    super(PosePlotter2D,self).__init__(subplot)
    self.estimated_pose_data = estimated_pose_data
    self.ground_truth_data = ground_truth_data
    
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
  
  def refresh_plot(self):
    
    self.subplot.set_title(self.title)
    self.subplot.set_xlim( self.xrange[0], self.xrange[1] )
    self.subplot.set_ylim( self.yrange[0], self.yrange[1] )
    self.subplot.set_xlabel( self.xlabel )
    self.subplot.set_ylabel( self.ylabel )
    self.subplot.legend(loc="upper right")
  
  def plot(self,i):
    print "2d"
    print i
  
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
    
  def refresh_plot(self):
    pass
    
    
  def plot(self,i):
    self.subplot.imshow( cv2.cvtColor(self.capture.read()[1],cv2.cv.CV_BGR2RGB) )