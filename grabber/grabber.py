import cv2
import os

class Grabber(object):

  def __init__(self):
    
    pass
    
  def open(self,videofile):
  
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
    
    
  def run(self):
  
    print("Hit space to capture frames and q to quit!")
    
    cv2.namedWindow(self.__WIN_ID)
    
    while True:
    
      frame = self.__cap.read()
      if frame[0] == False:
        break
      
      frame = frame[1]
      
      cv2.imshow(self.__WIN_ID,frame)
      
      key = cv2.waitKey(40)
           
      if key == ord(" "):
      
        self.save(frame)
        
      elif key == ord("q"):
        
        break
        
    
  def save(self,frame):
  
    cv2.imwrite(os.path.join(self.__save_dir,"frame{count}.png".format(count=self.__count)),frame)
    
    self.__count+=1
    
      
    