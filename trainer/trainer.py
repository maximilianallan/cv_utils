import cv2
import numpy as np
import sys
sys.path.append("z:\cv_utils")
from recolor import ColorSpace
from sklearn.ensemble import RandomForestClassifier
import pickle

class Trainer(object):

  def __init__(self, image_path, mask_path, num_labels = 2):

    self.image = cv2.imread(image_path)
    self.mask = cv2.imread(mask_path,0)

    self.num_examples = self.image.shape[0]*self.image.shape[1]
    self.num_dims = 4
    self.num_labels = num_labels
    
  def convert_training(self):

    cs = ColorSpace(image=self.image)
    hue = cs.get_hue()
    sat = cs.get_sat()
    o2 = cs.get_o2()
    o3 = cs.get_o3()

    training_data = np.zeros(shape=(self.num_examples,self.num_dims),dtype=np.float32)
    training_data[:,0] = hue.reshape((self.num_examples,)).astype(np.float32)
    training_data[:,1] = sat.reshape((self.num_examples,)).astype(np.float32)
    training_data[:,2] = o2.reshape((self.num_examples,)).astype(np.float32)
    training_data[:,3] = o3.reshape((self.num_examples,)).astype(np.float32)
    return training_data

  def convert_labels(self):

    if self.num_labels == 2:
    
      a = self.mask.reshape((self.num_examples,)).astype(np.int32)
      a = a/255
      return a
    
    else:
    
      unique_vals = self.find_unique_vals(self.mask)

      if len(unique_vals) != self.num_labels:
        raise Exception("Error, the number of unique values: {0} does not equal the number of labels: {1}\n".format(len(unique_vals), self.num_labels))
      
      labels = list(unique_vals)
      labels.sort()
      a = self.mask.reshape((self.num_examples,)).astype(np.int32)
      for i in range(self.num_examples):
        a[i] = labels.index(a[i])
        
      for i in range(self.num_examples):
        v = a[i]
        if v != 0 and v != 1 and v != 2:
          raise Exception("Err v = {0}".format(v))
      
      return a
      
      
  def train(self):

    self.training_data = self.convert_training()
    self.labels = self.convert_labels()

    self.rf = cv2.RTrees()
    
    self.rf.train(self.training_data, 1, self.labels)

    self.rf.save("rf_{0}class.xml".format(self.num_labels))

  
  def find_unique_vals(self, mask):
  
    vals = []
    height = mask.shape[0]
    width = mask.shape[1]
    for r in range(height):
      for c in range(width):
        vals.append(mask[r,c])
    
    vals = set(vals)
    return vals
    
  def predict(self,image):

    if self.rf == None:
      self.rf.load("rf_{0}class.xml".format(self.num_labels))

    predictions = np.zeros(shape=(image.shape[0],image.shape[1],3),dtype=np.uint8)

    cs = ColorSpace(image=self.image)
    hue = cs.get_hue()
    sat = cs.get_sat()
    o2 = cs.get_o2()
    o3 = cs.get_o3()

    for r in range(image.shape[0]):
      for c in range(image.shape[1]):
        data = np.zeros(shape=(self.num_dims,),dtype=np.float32)
        data[0] = float(hue[r,c])
        data[1] = float(sat[r,c])
        data[2] = float(o2[r,c])
        data[3] = float(o3[r,c])
        pred = self.rf.predict( data )
        if pred == 0:
          predictions[r,c] = [0,0,0]
        elif pred == 1:
          predictions[r,c] = [255,0,0]
        elif pred == 2:
          predictions[r,c] = [0,255,0]
        elif pred == 3:
          predictions[r,c] = [0,0,255]
        else:
          raise Exception("Error, need more colors")
        #predictions[r,c] = 255 * self.rf.predict( data  )

    cv2.imwrite("prediction.png",predictions)
