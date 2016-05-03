import numpy as np
import math
import copy


PI = 3.14159265358979323846
PI_2 = 1.57079632679489661923
PI_4 = 0.785398163397448309616

def enum(**enums):
    return type('Enum', (), enums)
    
class GeneralFrame:

  def __init__(self, tx, ty, tz, r11, r12, r13, r21, r22, r23, r31, r32, r33):
  
    self.rotation = np.asarray( [[r11, r12, r13], [r21, r22, r23], [r31, r32, r33]], dtype=np.float32)
    self.translation = np.asarray( [tx,ty,tz], dtype=np.float32)
    
    np.testing.assert_approx_equal(np.linalg.det(self.rotation), 1.0, 5, err_msg='Error, rotation matrix does not have determinant 1')

  def as_4x4(self):
  
    r = np.eye(4, dtype=np.float32)
    r[0:3,0:3] = self.rotation
    r[0:3,3] = self.translation * DHFrame.SCALE
        
    return r

class DHFrame:
   
  SCALE = 1000
   
  def __init__(self, joint_type, a, alpha, d, theta):
    assert(joint_type in ["FIXED", "ROTARY", "PRISMATIC"])
    self.joint_type = joint_type
    self.a = a
    self.alpha = alpha
    self.theta = theta
    self.d = d
    

def mult_matrix(A, B):
  
  try:
    return np.dot(B,A)
  except Exception as e:
    print B
    print A
    raise e

class Transform:

  def __init__(self, t4x4):

    self.rotation = t4x4[0:3,0:3]
    self.translation = t4x4[0:3,3]


class DaVinciClassicArm:

  def __init__(self):
  
    self.world_to_suj_origin = []
    self.suj_origin_to_suj_tip = []
    self.suj_tip_to_psm_origin = []
    self.psm_origin_to_psm_tip = []

  def get_transforms(self):

    for t in self.world_to_suj_origin + self.suj_origin_to_suj_tip + self.suj_tip_to_psm_origin + self.psm_origin_to_psm_tip:
      yield Transform(t)

class DaVinciMTM:

  def __init__(self):
  
    self.mtm_base_to_mtm_tip = []

  def get_transforms(self):

    for mtm_t in self.mtm_base_to_mtm_tip:
      yield Transform(mtm_t)

class DaVinciClassicRobot:

  def __init__(self):
    self.create_psm1()
    self.create_psm2()
    self.create_ecm()
    self.mtml = self.create_mtm()
    self.mtmr = self.create_mtm()

  def create_psm1(self):
  
    self.psm1 = DaVinciClassicArm()
    self.psm1.world_to_suj_origin.append( GeneralFrame(-0.1016, -0.1016, 0.43, -1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 1.0))
    
    self.psm1.suj_origin_to_suj_tip.append( DHFrame("PRISMATIC", 0.08979, 0.0, 0.0, 0.0) )
    self.psm1.suj_origin_to_suj_tip.append( DHFrame("ROTARY", 0.0, 0.0, 0.4166, 0.0) )
    self.psm1.suj_origin_to_suj_tip.append( DHFrame("ROTARY", 0.4318, 0.0, 0.14288, 0.0) )
    self.psm1.suj_origin_to_suj_tip.append( DHFrame("ROTARY", 0.4318, 0.0, -0.1302, PI_2) )
    self.psm1.suj_origin_to_suj_tip.append( DHFrame("ROTARY", 0.0, PI_2, 0.4089, 0.0) )
    self.psm1.suj_origin_to_suj_tip.append( DHFrame("ROTARY", 0.0, -PI_2, -0.1029, -PI_2) )
    
    self.psm1.suj_tip_to_psm_origin.append( GeneralFrame( 0.478, 0.0, 0.1524, 0.0, 1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0 ) )
    
    PSM1_lenRCC = 0.4318
    PSM1_ToolLen = 0.4159
    PSM1_PitchToYaw = 0.009
    PSM1_YawToCtrlPnt = 0.0
  
    self.psm1.psm_origin_to_psm_tip.append( DHFrame("ROTARY", 0.0, PI_2, 0.0, PI_2) )
    self.psm1.psm_origin_to_psm_tip.append( DHFrame("ROTARY", 0.0, -PI_2, 0.0, -PI_2) )
    self.psm1.psm_origin_to_psm_tip.append( DHFrame("PRISMATIC", 0.0, PI_2, -PSM1_lenRCC, 0.0) )
    self.psm1.psm_origin_to_psm_tip.append( DHFrame("ROTARY", 0.0, 0.0, PSM1_ToolLen, 0.0) )
    self.psm1.psm_origin_to_psm_tip.append( DHFrame("ROTARY", 0.0, -PI_2, 0.0, -PI_2) )
    self.psm1.psm_origin_to_psm_tip.append( DHFrame("ROTARY", PSM1_PitchToYaw, -PI_2, 0.0, -PI_2 ) )
    self.psm1.psm_origin_to_psm_tip.append( DHFrame("FIXED", 0.0, -PI_2, PSM1_YawToCtrlPnt, 0.0) )
    
  def create_psm2(self):
  
    self.psm2 = DaVinciClassicArm()
    self.psm2.world_to_suj_origin.append( GeneralFrame(0.1016, -0.1016, 0.43, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0))
    
    self.psm2.suj_origin_to_suj_tip.append( DHFrame("PRISMATIC", 0.08979, 0.0, 0.0, 0.0) )
    self.psm2.suj_origin_to_suj_tip.append( DHFrame("ROTARY", 0.0, 0.0, 0.4166, 0.0) )
    self.psm2.suj_origin_to_suj_tip.append( DHFrame("ROTARY", 0.4318, 0.0, 0.14288, 0.0) )
    self.psm2.suj_origin_to_suj_tip.append( DHFrame("ROTARY", 0.4318, 0.0, -0.1302, PI_2) )
    self.psm2.suj_origin_to_suj_tip.append( DHFrame("ROTARY", 0.0, PI_2, 0.4089, 0.0) )
    self.psm2.suj_origin_to_suj_tip.append( DHFrame("ROTARY", 0.0, -PI_2, -0.1029, -PI_2) )
    
    self.psm2.suj_tip_to_psm_origin.append( GeneralFrame( 0.478, 0.0, 0.1524, 0.0, 1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0 ) )
    
    PSM2_lenRCC = 0.4318
    PSM2_ToolLen = 0.4159
    PSM2_PitchToYaw = 0.009
    PSM2_YawToCtrlPnt = 0.0
  
    self.psm2.psm_origin_to_psm_tip.append( DHFrame("ROTARY", 0.0, PI_2, 0.0, PI_2) )
    self.psm2.psm_origin_to_psm_tip.append( DHFrame("ROTARY", 0.0, -PI_2, 0.0, -PI_2) )
    self.psm2.psm_origin_to_psm_tip.append( DHFrame("PRISMATIC", 0.0, PI_2, -PSM2_lenRCC, 0.0) )
    self.psm2.psm_origin_to_psm_tip.append( DHFrame("ROTARY", 0.0, 0.0, PSM2_ToolLen, 0.0) )
    self.psm2.psm_origin_to_psm_tip.append( DHFrame("ROTARY", 0.0, -PI_2, 0.0, -PI_2) )
    self.psm2.psm_origin_to_psm_tip.append( DHFrame("ROTARY", PSM2_PitchToYaw, -PI_2, 0.0, -PI_2 ) )
    self.psm2.psm_origin_to_psm_tip.append( DHFrame("FIXED", 0.0, -PI_2, PSM2_YawToCtrlPnt, 0.0) )
    
  def create_ecm(self):
  
    self.ecm = DaVinciClassicArm()
    self.ecm.world_to_suj_origin.append( GeneralFrame(0.0, 0.0, 0.43, 0.0, -1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0))
    
    self.ecm.suj_origin_to_suj_tip.append( DHFrame("PRISMATIC", 0.08979, 0.0, 0.0, 0.0) )
    self.ecm.suj_origin_to_suj_tip.append( DHFrame("ROTARY", 0.0, 0.0, 0.4166, 0.0) )
    self.ecm.suj_origin_to_suj_tip.append( DHFrame("ROTARY", 0.4318, 0.0, 0.14288, 0.0) )
    self.ecm.suj_origin_to_suj_tip.append( DHFrame("ROTARY", 0.4318, 0.0, -0.34588, PI_2) )
    self.ecm.suj_origin_to_suj_tip.append( DHFrame("FIXED", 0.0, -PI_4, 0.0, PI_2) )
    self.ecm.suj_origin_to_suj_tip.append( DHFrame("FIXED", -0.06641, 0.0, 0.0, 0.0) )
    
    self.ecm.suj_tip_to_psm_origin.append( GeneralFrame( 0.6126, 0.0, 0.1016, 0.0, 1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0 ) )
    
    ECM1_lenRCC = 0.3822
    ECM1_ScopeLen = 0.3828
  
    self.ecm.psm_origin_to_psm_tip.append( DHFrame("ROTARY", 0.0, PI_2, 0.0, PI_2) )
    self.ecm.psm_origin_to_psm_tip.append( DHFrame("ROTARY", 0.0, -PI_2, 0.0, -PI_2) )
    self.ecm.psm_origin_to_psm_tip.append( DHFrame("PRISMATIC", 0.0, PI_2, -ECM1_lenRCC, 0.0) )
    self.ecm.psm_origin_to_psm_tip.append( DHFrame("ROTARY", 0.0, 0.0, ECM1_ScopeLen, 0.0) )
    self.ecm.psm_origin_to_psm_tip.append( DHFrame("FIXED", 0.0, -PI_2, 0.0, -PI_2) )
    self.ecm.psm_origin_to_psm_tip.append( DHFrame("FIXED", 0.0, -PI_2, 0.0, -PI_2 ) )
    self.ecm.psm_origin_to_psm_tip.append( DHFrame("FIXED", 0.0, -PI_2, 0.0, 0.0) )
    
  def extendChain(self, frame, A, delta = None):
  
    if isinstance(frame, GeneralFrame):
      
      A = mult_matrix(frame.as_4x4(), A)
    
    elif isinstance(frame,DHFrame):
    
      DH = np.zeros(shape=(4,4), dtype=np.float32)
    
      if frame.joint_type == "FIXED":
        self.glhDenavitHartenberg( frame.a * DHFrame.SCALE, frame.alpha, frame.d * DHFrame.SCALE, frame.theta, DH)
      elif frame.joint_type == "ROTARY":
        self.glhDenavitHartenberg( frame.a * DHFrame.SCALE, frame.alpha, frame.d * DHFrame.SCALE, frame.theta + delta, DH)
      elif frame.joint_type == "PRISMATIC":
        self.glhDenavitHartenberg( frame.a * DHFrame.SCALE, frame.alpha, (frame.d + delta) * DHFrame.SCALE, frame.theta, DH)
    
      A = mult_matrix(DH, A)   
    
    return A  
 
  def glhDenavitHartenberg(self, a, alpha, d, theta, matrix):
   
    sa = math.sin(alpha)
    ca = math.cos(alpha)
    st = math.sin(theta)
    ct = math.cos(theta)
        
    matrix[0,0] = ct
    matrix[1,0] = ca * st
    matrix[2,0] = sa * st
    matrix[3,0] = 0
    matrix[0,1] = -st
    matrix[1,1] = ca * ct
    matrix[2,1] = sa * ct
    matrix[3.1] = 0.0
    matrix[0,2] = 0.0
    matrix[1,2] = -sa
    matrix[2,2] = ca
    matrix[3,2] = 0.0
    matrix[0,3] = a
    matrix[1,3] = -sa * d
    matrix[2,3] = ca * d
    matrix[3,3] = 1.0

  def get_kinematic_chain_psm(self, psm, suj_data, j_data):

    import cv2
    A = np.eye(4, dtype=np.float32)
    A = self.extendChain(psm.world_to_suj_origin[0], A)
    chain = [copy.deepcopy(A)]

    for su_joint, su_joint_data in zip(psm.suj_origin_to_suj_tip, suj_data):
      A = self.extendChain(su_joint, A, su_joint_data)
      chain.append(copy.deepcopy(A))

    A = self.extendChain(psm.suj_tip_to_psm_origin[0], A)
    chain.append(copy.deepcopy(A))

    for i in range(len(psm.psm_origin_to_psm_tip)-1):

      A = self.extendChain(psm.psm_origin_to_psm_tip[i], A, j_data[i])
      chain.append(copy.deepcopy(A))
      if i == 3:
        roll = copy.deepcopy(A)
      elif i == 4:
        wrist_pitch = copy.deepcopy(A)
      elif i == 5:
        wrist_yaw = copy.deepcopy(A)

    A = self.extendChain(psm.psm_origin_to_psm_tip[6], A, 0)
    chain.append(copy.deepcopy(A))

    return chain

  def buildKinematicChainPSM(self, psm, suj_data, j_data):
    
    import cv2
    A = np.eye(4, dtype=np.float32)
    
    A = self.extendChain(psm.world_to_suj_origin[0], A)
    
    for su_joint, su_joint_data in zip(psm.suj_origin_to_suj_tip, suj_data):
      A = self.extendChain(su_joint, A, su_joint_data)
  
    A = self.extendChain(psm.suj_tip_to_psm_origin[0], A)
    
    for i in range(len(psm.psm_origin_to_psm_tip)-1):
    
      A = self.extendChain(psm.psm_origin_to_psm_tip[i], A, j_data[i])
      if i == 3:
        roll = copy.deepcopy(A)
      elif i == 4:
        wrist_pitch = copy.deepcopy(A)
      elif i == 5:
        wrist_yaw = copy.deepcopy(A)
        
    A = self.extendChain(psm.psm_origin_to_psm_tip[6], A, 0)

    grip_1 = copy.deepcopy(A)
    grip_2 = copy.deepcopy(A)

    clasper_angle = j_data[6]
    
    clasper_rotation_ = cv2.Rodrigues( 0.5 * clasper_angle * np.asarray( [ 0,1,0], dtype=np.float32 ))[0]
    clasper_rotation = np.eye(4, dtype=np.float32)
    clasper_rotation[0:3,0:3] = clasper_rotation_
    
    grip_1 = mult_matrix(clasper_rotation, grip_1)
    
    clasper_rotation_ = cv2.Rodrigues( 0.5 * -clasper_angle * np.asarray( [ 0,1,0], dtype=np.float32 ))[0]
    clasper_rotation = np.eye(4, dtype=np.float32)
    clasper_rotation[0:3,0:3] = clasper_rotation_
    
    grip_2 = mult_matrix(clasper_rotation, grip_2)
    
    return (roll, wrist_pitch, grip_1, grip_2)
    
  def buildKinematicChainECM(self, suj_data, j_data):
  
    A = np.eye(4, dtype=np.float32)
    
    A = self.extendChain(self.ecm.world_to_suj_origin[0], A)
        
    for su_joint, su_joint_data in zip(self.ecm.suj_origin_to_suj_tip, suj_data):
      
      A = self.extendChain(su_joint, A, su_joint_data)     
    
    A = self.extendChain(self.ecm.suj_tip_to_psm_origin[0], A)
    
    
    for joint, joint_data in zip(self.ecm.psm_origin_to_psm_tip, j_data + [0,0,0]):
      A = self.extendChain(joint, A, joint_data)
      
    return A

  def create_mtm(self):

    l_arm = 0.2794
    l_forearm1 = 0.3948
    l_forearm2 = 0.0597
    h = 0.1506
    l4 = 0 # unsure if this should be zero.

    mtm = DaVinciMTM()
    mtm.mtm_base_to_mtm_tip.append( DHFrame("ROTARY", 0, 0 , 0, PI_2 ))  # outer yaw
    mtm.mtm_base_to_mtm_tip.append( DHFrame("ROTARY", 0, 0 , 0, -PI_2 )) # outer pitch 1
    mtm.mtm_base_to_mtm_tip.append( DHFrame("ROTARY", -l_arm, 0 , 0, 0 )) # outer pitch 2
    mtm.mtm_base_to_mtm_tip.append( DHFrame("FIXED", -l_forearm1, 0 , 0, 0 )) # forearm
    mtm.mtm_base_to_mtm_tip.append( DHFrame("ROTARY", -l_forearm2, PI_2 , h, 0 )) # setup joint
    mtm.mtm_base_to_mtm_tip.append( DHFrame("ROTARY", 0, -PI_2 , 0, 0 )) # wrist pitch
    mtm.mtm_base_to_mtm_tip.append( DHFrame("ROTARY", 0, PI_2 , 0, PI_2 )) # wrist yaw
    mtm.mtm_base_to_mtm_tip.append( DHFrame("ROTARY", 0, PI_2 , l4, 0 )) # wrist roll
    return mtm

  def get_kinematic_chain_mtm(self, mtm, mtm_data):

    A = np.eye(4, dtype=np.float32)
    chain = []

    A = self.extendChain(mtm.mtm_base_to_mtm_tip[0], A, delta=mtm_data[0])
    chain.append(copy.deepcopy(A))
    A = self.extendChain(mtm.mtm_base_to_mtm_tip[1], A, delta=mtm_data[1])
    chain.append(copy.deepcopy(A))
    A = self.extendChain(mtm.mtm_base_to_mtm_tip[2], A, delta=mtm_data[2]-mtm_data[1])
    chain.append(copy.deepcopy(A))
    A = self.extendChain(mtm.mtm_base_to_mtm_tip[3], A) # fixed joint
    chain.append(copy.deepcopy(A))
    A = self.extendChain(mtm.mtm_base_to_mtm_tip[4], A, delta=mtm_data[3])
    chain.append(copy.deepcopy(A))
    A = self.extendChain(mtm.mtm_base_to_mtm_tip[5], A, delta=mtm_data[4])
    chain.append(copy.deepcopy(A))
    A = self.extendChain(mtm.mtm_base_to_mtm_tip[6], A, delta=mtm_data[5])
    chain.append(copy.deepcopy(A))
    A = self.extendChain(mtm.mtm_base_to_mtm_tip[7], A, delta=mtm_data[6])
    chain.append(copy.deepcopy(A))
    return chain



  def plot_transforms(self, subplot, arm_transforms):

    for transform in arm_transforms:

      axis_size = 50

      start = np.dot(transform, np.asarray([-axis_size, 0, 0, 1]))
      end = np.dot(transform,np.asarray([axis_size, 0, 0, 1]))

      top = np.dot(transform,np.asarray([0, axis_size, 0, 1]))
      bottom = np.dot(transform,np.asarray([0, -axis_size , 0, 1]))

      left = np.dot(transform, np.asarray([0, 0, axis_size, 1]))
      right = np.dot(transform, np.asarray([0, 0, -axis_size, 1]))

      #sys.exit(0)

      subplot.plot(xs = [start[0],transform[0,3], end[0], transform[0,3], left[0], transform[0,3], right[0], transform[0,3], bottom[0], transform[0,3], top[0]],
                   ys = [start[1],transform[1,3], end[1], transform[1,3], left[1], transform[1,3], right[1], transform[1,3], bottom[1], transform[1,3], top[1]],
                   zs = [start[2],transform[2,3], end[2], transform[2,3], left[2], transform[2,3], right[2], transform[2,3], bottom[2], transform[2,3], top[2]]
                   )

      #break

  def grab_new_values(self, i):

    #grab the values from ros

    mtml_data = np.zeros(shape=(8,), dtype=np.float32)
    mtmr_data = np.zeros(shape=(8,), dtype=np.float32)
    psm1_j_data = np.zeros(shape=(7,), dtype=np.float32)
    psm2_j_data = np.zeros(shape=(7,), dtype=np.float32)
    psm1_suj_data = np.zeros(shape=(6,), dtype=np.float32)
    psm2_suj_data = np.zeros(shape=(6,), dtype=np.float32)

    mtml_chain = self.get_kinematic_chain_mtm(self.mtml, mtml_data)
    mtmr_chain = self.get_kinematic_chain_mtm(self.mtmr, mtmr_data)

    psm1_chain = self.get_kinematic_chain_psm(self.psm1, psm1_suj_data, psm1_j_data)
    psm2_chain = self.get_kinematic_chain_psm(self.psm2, psm2_suj_data, psm2_j_data)

    self.plot_transforms(self.mtml_subplot, mtml_chain)
    self.plot_transforms(self.mtmr_subplot, mtmr_chain)
    self.plot_transforms(self.psm1_subplot, psm1_chain)
    self.plot_transforms(self.psm2_subplot, psm2_chain)

  def set_plot_limits(self, subplot):

    subplot.set_xlim3d( -1000, 1000 )
    subplot.set_ylim3d( -1000, 1000 )
    subplot.set_zlim3d( -1000, 1000 )

  def viz_robot(self):

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D # needed or the projection=3d will fail
    import matplotlib.animation as animation

    figure = plt.figure(figsize=(15,15),facecolor='white')

    self.mtml_subplot = plt.subplot2grid((2,2), (0,0), 1, 1, projection='3d')
    self.mtmr_subplot = plt.subplot2grid((2,2), (0,1), 1, 1, projection='3d')
    self.psm1_subplot = plt.subplot2grid((2,2), (1,0), 1, 1, projection='3d')
    self.psm2_subplot = plt.subplot2grid((2,2), (1,1), 1, 1, projection='3d')

    self.set_plot_limits(self.mtml_subplot)
    self.set_plot_limits(self.mtmr_subplot)
    self.set_plot_limits(self.psm1_subplot)
    self.set_plot_limits(self.psm2_subplot)

    ani = animation.FuncAnimation(figure, self.grab_new_values, frames = 4000)
    plt.show()
    #ani.save('./poseplotter/output/vid2.avi',fps=10,clear_temp=False)


if __name__ == '__main__':

  robot = DaVinciClassicRobot()
  
  import argparse
  import sys
  
  parser = argparse.ArgumentParser(description='Generate coordinate frames using da Vinci kinematics')
  
  parser.add_argument('--ecm-suj-file', type=str, help='The file containing the ECM set up joint values.', required=True)
  parser.add_argument('--ecm-j-file', type=str, help='The file containing the ECM joint values.', required=True)
  
  parser.add_argument('--psm1-suj-file', type=str, help='The file containing the PSM 1 SUJ values.')
  parser.add_argument('--psm1-j-file', type=str, help='The file containing the PSM 1 joint values.')
  
  parser.add_argument('--psm2-suj-file', type=str, help='The file containing the PSM 2 SUJ values.')
  parser.add_argument('--psm2-j-file', type=str, help='The file containing the PSM 2 joint values.')

  args = parser.parse_args()
  
  ecm_suj = open(args.ecm_suj_file, 'r').readlines()
  ecm_j = open(args.ecm_j_file, 'r').readlines()
  
  if args.psm1_suj_file and args.psm1_j_file:
    psm1_suj = open(args.psm1_suj_file, 'r').readlines()
    psm1_j = open(args.psm1_j_file, 'r').readlines()
  
  if args.psm2_suj_file and args.psm2_j_file:
    psm2_suj = open(args.psm2_suj_file, 'r').readlines()
    psm2_j = open(args.psm2_j_file, 'r').readlines()

  np.set_printoptions(precision=6)  
  np.set_printoptions(suppress=True) 

  def clean_line(line):
    
    try:
      vals = line.strip("\n").split(" ")
    except:
      print line
      s  = dd
    vals = [v for v in vals if v != ""]
    return map(float, vals)

  for i in range(len(ecm_suj)):
      
    A = robot.buildKinematicChainECM(clean_line(ecm_suj[i]), clean_line(ecm_j[i]))
    
    print "\nECM Frame {0} = \n".format(i)
    print A
    
    num_lines_printed = 9
    
    try:
    
      (psm1_roll, psm1_wrist_pitch, psm1_grip_1, psm1_grip_2) = robot.buildKinematicChainPSM(robot.psm1, clean_line(psm1_suj[i]), clean_line(psm1_j[i]))
 
      print "\nPSM 1 Roll Frame {0} = \n".format(i)
      print psm1_roll
 
      num_lines_printed += 7
 
    except NameError:
    
      pass
        
    try:
    
      (psm2_roll, psm2_wrist_pitch, psm2_grip_1, psm2_grip_2) = robot.buildKinematicChainPSM(robot.psm2, clean_line(psm2_suj[i]), clean_line(psm2_j[i]))
    
      print "\nPSM 2 Roll Frame {0} = \n".format(i)
      print psm2_roll
     
      num_lines_printed += 7
     
    except NameError:
    
      pass
    
    question = "\nUse enter to load the next line and 'q' to quit"
    print question,
    input = raw_input()
    if input == 'q':
      break
    
    sys.stdout.write("\033[F"*num_lines_printed)
  
  
  
  
  
  
  