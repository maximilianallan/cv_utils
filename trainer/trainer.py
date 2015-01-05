import cv2
import numpy as np
import sys
sys.path.append("z:\cv_utils")
from recolor import ColorSpace
from sklearn.ensemble import RandomForestClassifier
import pickle

class Trainer(object):

  def __init__(self, image_path, mask_path):

    self.image = cv2.imread(image_path)
    self.mask = cv2.imread(mask_path,0)

    self.num_examples = self.image.shape[0]*self.image.shape[1]
    self.num_dims = 4

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

    a = self.mask.reshape((self.num_examples,)).astype(np.int32)
    a = a/255
    return a

  def train(self):

    self.training_data = self.convert_training()
    self.labels = self.convert_labels()

    self.rf = cv2.RTrees()
    
    self.rf.train(self.training_data, 1, self.labels)

    self.rf.save("rf.xml")

  def predict(self,image):

    if self.rf == None:
      self.rf.load("rf.xml")

    predictions = np.zeros(shape=(image.shape[0],image.shape[1]),dtype=np.uint8)

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
        predictions[r,c] = 255 * self.rf.predict( data  )

    cv2.imwrite("prediction.png",predictions)
