import cv2

class ChopViewer:

  def __init__(self, input_video_file, output_dir):
  
    self.save_count = 0
    self.vid_cap = cv2.VideoCapture(input_video_file)
    
    self.output_dir = output_dir
    self.frame_buffer = []
    self.max_num_frames = 80
    self.read_idx = 0
    self.save_toggle = False
    self.vid_writer = None
    self.running = True
    
  def pause(self):
    self.running = False
    
  def play(self):
    self.running = True
    
  def read(self):
        
    if self.running is False and self.read_idx < len(self.frame_buffer):
      return self.frame_buffer[self.read_idx]
      
    #print self.running
    #print self.read_idx
    #print len(self.frame_buffer)
   
    if self.read_idx < len(self.frame_buffer):
      self.read_idx += 1
      return self.frame_buffer[self.read_idx-1]
    
    f = self.vid_cap.read()
    if f[0] is False:
      return None
  
    self.frame_buffer.append(f[1])
  
    if len(self.frame_buffer) > self.max_num_frames:
      self.frame_buffer.pop(0)
    
    return self.frame_buffer[-1]
  
  def toggle_save(self):
  
    if self.save_toggle:
      if self.vid_writer is not None:
        del self.vid_writer
        self.vid_writer = None
        self.save_count += 1
  
    self.save_toggle = not self.save_toggle
    
  def is_saving(self):
    
    return self.save_toggle
  
  
  def save(self, frame):
  
    if self.vid_writer is None:
      self.vid_writer = cv2.VideoWriter(self.output_dir + "/crop_{0}.avi".format(self.save_count), cv2.cv.CV_FOURCC(*"DIB "), 25, (frame.shape[1], frame.shape[0]))
      
    self.vid_writer.write(frame)
    
  def forward(self):
    
    if self.read_idx < len(self.frame_buffer) - 1:
      self.read_idx += 1
   
  def backward(self):
    
    if self.read_idx > 0:
      self.read_idx -= 1
    
    
     
     
    
      
    
    
