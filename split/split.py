def split(frame):
  
  width = int(frame.shape[1]/2)
  
  try:
    return frame[:,0:width,:],frame[:,width:width*2,:]
  except:
    return frame[:,0:width],frame[:,width:width*2] #single channel
 
    