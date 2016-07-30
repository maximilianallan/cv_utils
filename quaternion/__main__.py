import numpy as np
import sys

class vector:

  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

    

def to_rotation_matrix(w, v):

  mV =  np.ndarray(shape=(4,4), dtype=np.float32)
  
  xs = v.x + v.x   
  ys = v.y + v.y
  zs = v.z + v.z
  wx = w * xs
  wy = w * ys
  wz = w * zs
  xx = v.x * xs
  xy = v.x * ys
  xz = v.x * zs
  yy = v.y * ys
  yz = v.y * zs
  zz = v.z * zs
  
  mV[0,0] = 1 - ( yy + zz )
  mV[0,1] = xy - wz
  mV[0,2] = xz + wy
  mV[0,3] = 0
  
  mV[1,0] = xy + wz
  mV[1,1] = 1 - ( xx + zz )
  mV[1,2] = yz - wx
  mV[1,3] = 0
  
  mV[2,0] = xz - wy
  mV[2,1] = yz + wx
  mV[2,2] = 1 - ( xx + yy )
  mV[2,3] = 0
  
  mV[3,0] = 0
  mV[3,1] = 0
  mV[3,2] = 0
  mV[3,3] = 1
  
  return mV


if len(sys.argv) != 5:
  print "Error run as quaternion qw qx qy qz\n"
  sys.exit(1)
  
qw = float(sys.argv[1])
qx = float(sys.argv[2])
qy = float(sys.argv[3])
qz = float(sys.argv[4])

print to_rotation_matrix(qw, vector(qx, qy, qz))

