"""PosePlotter.py 
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
import sys
import scipy.signal
import cv2
import os

class PosePlotter:

    def __init__(self,estimated_pose_file,ground_truth_pose_file,video_file,tracking_videofile,num_frames=400):

        self.estimated_pose_data = self.parse_pose_file(estimated_pose_file,True,True,5)
        self.ground_truth_data = self.parse_pose_file(ground_truth_pose_file,True)
        self.video_file = video_file
        self.tracking_file = tracking_videofile
        self.num_frames = num_frames
        self.plotting_2dpose = False
        self.plotting_3dpose = False
        self.plotting_error = False
        
    def setup_plot3d(self,**kwargs):

        if "title3d" in kwargs:
            self.title3d = kwargs["title3d"]
        else:
            self.title3d = "3D Pose Plot"
        
        if "xrange" in kwargs:
            xrange = kwargs["xrange"]
            self.xrange3d = [xrange[0],xrange[1]]            
        else:
            self.xrange3d = [ min(min(self.estimated_pose_data[:,0]),
                                  min(self.ground_truth_data[:,0])), 
                              max(max(self.estimated_pose_data[:,0]),
                                  max(self.ground_truth_data[:,0])) ]

        if "yrange" in kwargs:
            yrange = kwargs["yrange"]
            self.yrange3d = [yrange[0],yrange[1]]          
        else:
            self.yrange3d = [ min(min(self.estimated_pose_data[:,1]),
                                  min(self.ground_truth_data[:,1])), 
                              max(max(self.estimated_pose_data[:,1]),
                                  max(self.ground_truth_data[:,1])) ]

        if "zrange" in kwargs:
            zrange = kwargs["zrange"]
            self.zrange3d = [zrange[0],zrange[1]]
        else:
            self.zrange3d = [ min(min(self.estimated_pose_data[:,2]),
                                  min(self.ground_truth_data[:,2])), 
                              max(max(self.estimated_pose_data[:,2]),
                                  max(self.ground_truth_data[:,2])) ]

        if "units" in kwargs:
            self.units3d = kwargs["units"]
        else:
            self.units3d = "mm"               

        self.xlabel3d = "x position ({0})".format(self.units3d)
        self.ylabel3d = "y position ({0})".format(self.units3d)
        self.zlabel3d = "z position ({0})".format(self.units3d)

    def setup_plot2d(self,**kwargs):
        if "title2d" in kwargs:
            self.title2d = kwargs["title2d"]
        else:
            self.title2d = "2D Pose Plot"
        
        if "xrange" in kwargs:
            xrange = kwargs["xrange"]
            self.xrange2d = [xrange[0],xrange[1]]            
        else:
            self.xrange2d = [0,self.num_frames]

        if "yrange" in kwargs:
            yrange = kwargs["yrange"]
            self.yrange2d = [yrange[0],yrange[1]]          
        else:
            self.yrange2d = [ 99999.0,0 ]            
            for dof in range(3):
                self.yrange2d = [ min(np.concatenate((np.asarray([self.yrange2d[0]]),self.ground_truth_data[:,dof]))),
                                  max(np.concatenate((np.asarray([self.yrange2d[1]]),self.ground_truth_data[:,dof]))) ]
                self.yrange2d = [ min(np.concatenate((np.asarray([self.yrange2d[0]]),self.estimated_pose_data[:,dof]))),
                                  max(np.concatenate((np.asarray([self.yrange2d[1]]),self.estimated_pose_data[:,dof]))) ]
                
        if "units" in kwargs:
            self.units2d = kwargs["units"]
        else:
            self.units2d = "mm"                       

        if "xlabel2d" in kwargs:
            self.xlabel2d = kwargs["xlabel2d"]
        else:
            self.xlabel2d = "Frame number"
        if "ylabel2d" in kwargs:
            self.ylabel2d = kwargs["ylabel2d"]
        else:
            self.ylabel2d = "Position ({0})".format(self.units2d)
                 



    """Load in the pose data from the input files. Optionally clean the data up with a 1D 
    median filter and/or offset the data to start at (0,0,0,0,0,0)
    """    
    def parse_pose_file(self,pose_file,normalize=False,med_filt=False,kernel_width=5):

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
  

    
        
    def initialize_video(self,filepath,subplot,title):
       
        #open videofile
        subplot.set_title(title)
        video_capture = cv2.VideoCapture(filepath)
        subplot.axes.get_xaxis().set_visible(False)
        subplot.axes.get_yaxis().set_visible(False)
        return video_capture
    
    def initialize_3d(self,subplot,**kwargs):
        
        self.plotting_3dpose = True
        self.setup_plot3d(**kwargs)
        subplot.set_title(self.title3d)
        subplot.set_xlim3d(self.xrange3d)
        subplot.set_ylim3d(self.yrange3d)
        subplot.set_zlim3d(self.zrange3d)
        subplot.set_xlabel(self.xlabel3d)
        subplot.set_ylabel(self.ylabel3d)
        subplot.set_zlabel(self.zlabel3d)
        self.line3d_estimated = subplot.plot(xs=[],ys=[],zs=[],label="estimated",color="red")
        self.line3d_groundtruth = subplot.plot(xs=[],ys=[],zs=[],label="groundtruth",color="blue")
        subplot.legend(loc="upper right")
        
    def initialize_2d(self,subplot_x,subplot_y,subplot_z,**kwargs):
        
        self.plotting_2dpose = True
        self.setup_plot2d(**kwargs)
        subplot_x.set_title(self.title2d)
        #subplot.set_xlim(self.xrange2d)
        #subplot.set_ylim(self.yrange2d)
        subplot_x.set_xlabel(self.xlabel2d)
        subplot_x.set_ylabel(self.ylabel2d)
        subplot_y.set_xlabel(self.xlabel2d)
        subplot_y.set_ylabel(self.ylabel2d)
        subplot_z.set_xlabel(self.xlabel2d)
        subplot_z.set_ylabel(self.ylabel2d)

        self.line2d_xdata_estimated, = subplot_x.plot([],[],label="estimated (x)",color="red")
        self.line2d_xdata_groundtruth, = subplot_x.plot([],[],label="ground truth (x)",color="blue")
        self.line2d_ydata_estimated, = subplot_y.plot([],[],label="estimated (y)",color="green")
        self.line2d_ydata_groundtruth, = subplot_y.plot([],[],label="ground truth (y)",color="black")
        self.line2d_zdata_estimated, = subplot_z.plot([],[],label="estimated (z)",color="pink")
        self.line2d_zdata_groundtruth, = subplot_z.plot([],[],label="ground truth (z)",color="yellow")
        subplot_x.legend(loc="upper right")        
        subplot_y.legend(loc="upper right")        
        subplot_z.legend(loc="upper right")        
        
    def initialize_error(self,subplot,**kwargs):
           
        self.plotting_error = True
        self.setup_plot2d(**kwargs)
        subplot.set_title(self.title2d)
        #subplot.set_xlim(self.xrange2d)
        #subplot.set_ylim(self.yrange2d)
        subplot.set_xlabel(self.xlabel2d)
        subplot.set_ylabel(self.ylabel2d)
        self.line2d_xdata, = subplot.plot([],[],label="estimated (x)",color="red")
        self.line2d_ydata, = subplot.plot([],[],label="estimated (y)",color="blue")
        self.line2d_zdata, = subplot.plot([],[],label="estimated (z)",color="green")
        subplot.legend(loc="upper right")        
     
    def visualize_translations(self):

        """fig = plt.figure(figsize=(25,12))#,dpi=1000)      
        video_plot = fig.add_subplot(221)
        tracking_plot = fig.add_subplot(222)
        #plot_3d = fig.add_subplot(223,projection='3d') #2rows,2cols,plot1
        plot_2d = fig.add_subplot(223)
        #plt.legend(loc='upper left')
        plot_2d_err = fig.add_subplot(224)
        #plt.legend(loc='upper right')
        """
        fig = plt.figure(figsize=(25,12))
        video_plot = plt.subplot2grid( (4,4),(0,0),colspan=2,rowspan=1 )
        tracking_plot=plt.subplot2grid( (4,4),(0,2),colspan=2,rowspan=1 )
        plot_2d_x = plt.subplot2grid( (4,4), (1,0),colspan=2,rowspan=1 )
        plot_2d_y = plt.subplot2grid( (4,4), (2,0),colspan=2,rowspan=1 )
        plot_2d_z = plt.subplot2grid( (4,4), (3,0),colspan=2,rowspan=1 )
        plot_2d_err = plt.subplot2grid( (4,4), (2,2),colspan=2,rowspan=3)
        
        self.video_capture = self.initialize_video(self.video_file,video_plot,"Raw Data")
        self.tracking_capture = self.initialize_video(self.tracking_file,tracking_plot,"Tracking")
        #self.initialize_3d(plot_3d)
        self.initialize_2d(plot_2d_x)
        self.initialize_2d(plot_2d_y)
        self.initialize_2d(plot_2d_z)
        self.initialize_error(plot_2d_err,title2d="Pose Errors",ylabel2d="Error (mm)")
        
        def init():
            video_frame = video_plot.imshow(cv2.cvtColor(self.video_capture.read()[1],cv2.cv.CV_BGR2RGB))
            tracking_frame = tracking_plot.imshow(cv2.cvtColor(self.tracking_capture.read()[1],cv2.cv.CV_BGR2RGB))
            
        
        def animate(i):
            
            video_frame = video_plot.imshow(cv2.cvtColor(self.video_capture.read()[1],cv2.cv.CV_BGR2RGB))
            tracking_frame = tracking_plot.imshow(cv2.cvtColor(self.tracking_capture.read()[1],cv2.cv.CV_BGR2RGB))

            try:
                l = plot_3d.lines.pop(0)
                del l
                l = plot_3d.lines.pop(0)
                del l
            except:
                pass
            
            back_step = 100
            if(i < back_step):
                back_step = i

            rets = []
                
            if(self.plotting_3dpose):
                self.line3d_estimated, = plot_3d.plot(xs=self.estimated_pose_data[i-back_step:i,0],
                                                      ys=self.estimated_pose_data[i-back_step:i,1],
                                                      zs=self.estimated_pose_data[i-back_step:i,2],
                                                      label='estimated',
                                                      color='red')
            
                self.line3d_groundtruth, = plot_3d.plot(xs=self.ground_truth_data[i-back_step:i,0],
                                                        ys=self.ground_truth_data[i-back_step:i,1],
                                                        zs=self.ground_truth_data[i-back_step:i,2],
                                                        label="ground truth",
                                                        color='blue')
                rets.append(self.line3d_estimated)
                rets.append(self.line3d_groundtruth)
                
            x_vals = np.linspace(0,i-1,i)
            if self.plotting_2dpose:

                self.line2d_xdata_estimated, = plot_2d.plot(x_vals,
                                                            self.estimated_pose_data[0:i,0],
                                                            label="estimated",
                                                            color="red")
                self.line2d_xdata_groundtruth, = plot_2d.plot(x_vals,
                                                              self.ground_truth_data[0:i,0],
                                                              label='ground truth',
                                                              color='blue')
                self.line2d_ydata_estimated, = plot_2d.plot(x_vals,
                                                            self.estimated_pose_data[0:i,1],
                                                            label="estimated",
                                                            color="green")
                self.line2d_ydata_groundtruth, = plot_2d.plot(x_vals,
                                                              self.ground_truth_data[0:i,1],
                                                              label='ground truth',
                                                              color='black')
                self.line2d_zdata_estimated, = plot_2d.plot(x_vals,
                                                            self.estimated_pose_data[0:i,2],
                                                            label="estimated",
                                                            color="pink")
                self.line2d_zdata_groundtruth, = plot_2d.plot(x_vals,
                                                              self.ground_truth_data[0:i,2],
                                                              label='ground truth',
                                                              color='yellow')
                rets.append(self.line2d_xdata_estimated)
                rets.append(self.line2d_xdata_groundtruth)
                rets.append(self.line2d_ydata_estimated)
                rets.append(self.line2d_ydata_groundtruth)
                rets.append(self.line2d_zdata_estimated)
                rets.append(self.line2d_zdata_groundtruth)

            if self.plotting_error:
                self.line2d_xdata,=plot_2d_err.plot(x_vals,abs(self.ground_truth_data[0:i,0]-self.estimated_pose_data[0:i,0]),
                                                 label="estimated (x)",color="red")
                self.line2d_ydata,=plot_2d_err.plot(x_vals,abs(self.ground_truth_data[0:i,1]-self.estimated_pose_data[0:i,1]),
                                                label="estimated (y)",color="blue")
                self.line2d_zdata,=plot_2d_err.plot(x_vals,abs(self.ground_truth_data[0:i,2]-self.estimated_pose_data[0:i,2]),
                                                label="estimated (z)",color="green")
                rets.append(self.line2d_xdata)
                rets.append(self.line2d_ydata)
                rets.append(self.line2d_zdata)
            
            return tuple(rets)
            
                
        ani = animation.FuncAnimation(fig, animate,init_func=init,frames=self.num_frames)#, blit=True)
                
        
        try:
            os.mkdir("output")
        except:
            pass
        #ani.save('./output/pose2d2d_nwq.avi',fps=10,clear_temp=False)
            
        plt.show()
            
    

if __name__ == '__main__':

    #pose_plotter = PosePlotter("pose_2.csv","optotrak_pose.csv")
    #pose_plotter = PosePlotter("pose_2.csv","pose_1.csv")
    pose_plotter = PosePlotter("estimated_results.csv","ground_truth_results.csv","video.avi","tracking.avi",15)
    
    pose_plotter.visualize_translations()

            
