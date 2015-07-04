import cv2
import os
import numpy as np

class Grabber(object):

  def __init__(self, split_stereo):
    self.__split_stereo = split_stereo
    pass
    
  def open(self,videofile,right_videofile=None):
  
    self.__cap = cv2.VideoCapture(videofile)
    if not self.__cap.isOpened():
      raise Exception("Error, could not open video file: {f}".format(f=videofile))
    
    self.__count = 0
    self.__WIN_ID = "capture"
    self.__save_dir = "frames"
    
    n=0
    while os.path.exists(self.__save_dir):
      self.__save_dir = "frames{count}".format(count = n)
      n+=1
    
    os.mkdir(self.__save_dir)

    if right_videofile is not None:
      self.__right_cap = cv2.VideoCapture(right_videofile)
    else:
      self.__right_cap = None
      
    if self.__split_stereo or right_videofile is not None:
      os.mkdir(self.__save_dir + "/left")
      os.mkdir(self.__save_dir + "/right")
    
    
  def run(self):
  
    print("Hit space to capture frames and q to quit!")
    
    cv2.namedWindow(self.__WIN_ID)
    
    while True:
    
      frame = self.__cap.read()
      if frame[0] == False:
        break

      if self.__right_cap is not None:
        right_frame = self.__right_cap.read()
        if right_frame[0] == False:
          break
        frame_ = np.ndarray(shape=(frame[1].shape[0], frame[1].shape[1]+right_frame[1].shape[1],3),dtype=frame[1].dtype)
        frame_[:,0:frame[1].shape[1],:] = frame[1]
        frame_[:,frame[1].shape[1]:,:] = right_frame[1]
        frame = frame_
      else:
        frame = frame[1]
      
      cv2.imshow(self.__WIN_ID,frame)
      
      key = cv2.waitKey(40)
           
      if key == ord(" "):
      
        self.save(frame)

      elif key == ord("q"):
        
        break
        
    
  def save(self,frame):
    #save as jpg as bouguet calib software doesn't support png
    if self.__split_stereo or self.__right_cap is not None:
      
      width = int(frame.shape[1]/2)
      
      left = frame[:,0:width]
      right = frame[:,width:2*width]
    
      cv2.imwrite(os.path.join(self.__save_dir,"left/frame{count}.bmp".format(count=self.__count)),left)
      cv2.imwrite(os.path.join(self.__save_dir,"right/frame{count}.bmp".format(count=self.__count)),right)
    else:
      cv2.imwrite(os.path.join(self.__save_dir,"frame{count}.bmp".format(count=self.__count)),frame)
    
    self.__count+=1
    
      
    
