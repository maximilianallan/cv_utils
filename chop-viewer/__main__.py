import argparse
import cv2
from chop_viewer import ChopViewer

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Chop a video into segments on the fly')
  parser.add_argument('-i', '--input', type=str, help='The input video file', required=True)
  parser.add_argument('-o', '--output', type=str, help='Directory to save the output files', required=True)
  args = parser.parse_args()

  c = ChopViewer(args.input, args.output)
  
  win = "Chop Viewer"
  cv2.namedWindow(win)
  
  while True:
    
    #if c.running:
    frame = c.read()
    
    if frame is None:
      break
      
    cv2.imshow(win, frame)
    
    key = cv2.waitKey(40)
    
    if key & 255 == ord(' '):
      
      if c.running:
        #print "Pausing"
        c.pause()
      else:
        #print "Playing"
        c.play()
    
    if key & 255 == ord('s'):
    
      c.toggle_save()
      
    if key & 255 == 37:
      c.backward()
      c.pause()
      
    if key & 255 == 39:
      c.forward()
      c.pause()
      
    if c.is_saving():
      c.save(frame)
      
    if key & 255 == ord('q'):
    
      break
    
    