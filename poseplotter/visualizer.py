"""visualizer.py 
A utility for producing visualizations of data from 2D/3D tracking algorithms.
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
import matplotlib
import numpy as np
import sys

import os
from dataplotter import *

class Visualizer(object):

    def __init__(self,layout):

      matplotlib.rcParams.update({'font.family': 'serif'})
      self.figure = plt.figure(figsize=(15,15),facecolor='white')
      self.artists = []
      self.layout = layout
                          
    def add_3dplot(self, estimated_pose_data, ground_truth_pose_data, position, rowspan, colspan, **kwargs):
      
      subplot = plt.subplot2grid(self.layout,position, rowspan, colspan,projection='3d')
      subplot.elev=50
      self.artists.append( PosePlotter3D(estimated_pose_data,ground_truth_pose_data, subplot) )
      self.artists[-1].setup(**kwargs)
      
    def add_2dplot(self, estimated_pose_data, ground_truth_pose_data, position, rowspan, colspan, **kwargs):
      
      subplot = plt.subplot2grid(self.layout,position, rowspan, colspan)
      self.artists.append( PosePlotter2D(estimated_pose_data,ground_truth_pose_data, subplot) )
      self.artists[-1].setup(**kwargs)
      
    def add_video(self, videofile, position, rowspan, colspan, **kwargs):
    
      subplot = plt.subplot2grid(self.layout,position, rowspan, colspan)
      self.artists.append( ImagePlotter( videofile, subplot) )
      self.artists[-1].setup(**kwargs)
      
    def init_plot(self):
    
      return
      #for artist in self.artists:
      #  artist.setup()
      
    def animate_plot(self,i):
    
      for artist in self.artists:
        artist.plot(i)
        artist.refresh_plot()
        
    def visualize(self):
    
      ani = animation.FuncAnimation(self.figure, self.animate_plot, init_func = self.init_plot, frames = 400)
      #plt.show()          
      ani.save('./poseplotter/output/vid2.avi',fps=10,clear_temp=False)


            
