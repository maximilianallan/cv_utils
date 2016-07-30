__author__ = 'max'

import cv2

class VideoPlayer:

    def __init__(self, video_file):

      self.frames = []
      self.current_frame = None
      self.index = -1
      self.MAX_VAL = 100
      self.video_file = cv2.VideoCapture(video_file)
      self.count = 0
      if not self.video_file.isOpened():
        raise Exception("Error, could not open video file\n")


    def get_current_frame(self):

      return self.frames[self.index]


    def add_new(self, frame):

      while len(self.frames) > self.MAX_VAL:
        self.frames.pop(0)
        self.index -= 1

      self.frames.append(frame)

      self.index += 1

      self.current_frame = self.frames[self.index]


    def rewind(self):

      if self.index <= 0:
        return

      self.index -= 1
      self.current_frame = self.frames[self.index]

    def forward(self):

      if self.index >= self.MAX_VAL or self.index >= len(self.frames) - 1:
        return self.load_new()

      self.index += 1
      self.current_frame = self.frames[self.index]
      return True

    def load_new(self):

      frame = self.video_file.read()
      if frame[0] is False:
        print "Done"
        return False
      
      self.count+=1
      print "Playing frame {0}".format(self.count)
      frame = frame[1]

      self.add_new(frame)
      return True
