import cv2
import numpy as np
import os
p = os.path.realpath(__file__)
p = os.path.dirname(p) + "/../"
import sys
sys.path.append(p)
from recolor import ColorSpace

class Model(object):

  def __init__(self):
    self.model = None

  def setup_params(self):
    raise NotImplementedError("")
    
  def train(self, *args,**kwargs):
    self.model.train(args,kwargs)
    
  def save(self, *args, **kwargs):
    self.model.save(args,kwargs)
  
  def load(self, *args,**kwargs):
    self.model.load(args[0])
    print self.model
    
class RandomForest(Model):

  def __init__(self):
    super(RandomForest, self).__init__()
    self.model = cv2.RTrees()
    self.name = "RF"
    
  def setup_params(self):
    self.params = dict(term_crit=(cv2.TERM_CRITERIA_MAX_ITER,1,1) )
  
class BoostedClassifier(Model):
  def __init__(self):
    super(BoostedClassifier, self).__init__()
    self.model = cv2.Boost()
    self.name = "Boost"
    
  def setup_params(self):
    self.params = dict(max_depth=5)

class SVM(Model):
  def __init__(self):
    super(SVM,self).__init__()
    self.model = cv2.SVM()
    self.name = "SVM"
    
  def setup_params(self):
    self.params = dict( kernel_type = cv2.SVM_LINEAR, vm_type = cv2.SVM_C_SVC, C = 1 )
   
  def train(self, training_data, data_storage_type, labels, params):
    self.model.train(training_data, labels, params)
   
class Trainer(object):

  def __init__(self,  classifier_type, num_dims):

    self.num_dims = num_dims
    self.num_labels = 2
    
    if classifier_type == "rf":
      self.model = RandomForest()
    elif classifier_type == "svm":
      self.model = SVM()
    elif classifier_type == "boost":
      self.model = BoostedClassifier()
    else:
      raise Exception("Error, unrecognised classifier")

  def setup_training(self, image_paths, mask_paths, num_labels = 2):

    tmp_images = [cv2.imread(im_path) for im_path in image_paths] 
    tmp_masks = [cv2.imread(mask_path,0) for mask_path in mask_paths]
    
    self.images = []
    self.masks = []
    
    for im, mask in zip(tmp_images, tmp_masks):
      if im is None or mask is None:
        pass
      else:
        self.images.append(im)
        self.masks.append(mask)

    if len(self.images) != len(self.masks):
      raise Exception("Error, number of images files ({0}) does not match number of mask files ({1})! Exiting...\n".format(len(self.images), len(self.masks)))
    if len(self.images) == 0:
      raise Exception("Error, no files found! Exiting...\n")
    
    self.num_examples = sum([im.shape[0]*im.shape[1] for im in self.images])
    self.num_labels = num_labels
    
  def convert_training(self):

    training_data = np.zeros(shape=(self.num_examples,self.num_dims),dtype=np.float32)
   
    for n,image in enumerate(self.images):
   
      resolution = image.shape[0] * image.shape[1]
   
      start_index = n * resolution
      end_index = ((n+1) * resolution)
   
      if self.num_dims == 3:
        red = image[:,:,0]
        green = image[:,:,1]
        blue = image[:,:,2]
        training_data[start_index:end_index,0] = red.reshape((resolution,)).astype(np.float32, casting='safe')
        training_data[start_index:end_index,1] = green.reshape((resolution,)).astype(np.float32, casting='safe')
        training_data[start_index:end_index,2] = blue.reshape((resolution,)).astype(np.float32, casting='safe')
        
      else:
        cs = ColorSpace(image=image)
        hue = cs.get_hue()
        sat = cs.get_sat()
        o2 = cs.get_o2()
        o3 = cs.get_o3()
        
        if self.num_dims == 7:
          red = image[:,:,0]
          green = image[:,:,1]
          blue = image[:,:,2]
              
        training_data[start_index:end_index,0] = hue.reshape((resolution,)).astype(np.float32, casting='safe')
        training_data[start_index:end_index,1] = sat.reshape((resolution,)).astype(np.float32, casting='safe')
        training_data[start_index:end_index,2] = o2.reshape((resolution,)).astype(np.float32, casting='safe')
        training_data[start_index:end_index,3] = o3.reshape((resolution,)).astype(np.float32, casting='safe')
        
        if self.num_dims == 7:
          training_data[start_index:end_index,4] = red.reshape((resolution,)).astype(np.float32, casting='safe')
          training_data[start_index:end_index,5] = green.reshape((resolution,)).astype(np.float32, casting='safe')
          training_data[start_index:end_index,6] = blue.reshape((resolution,)).astype(np.float32, casting='safe')
        
    return training_data

  def convert_labels(self):
  
    if self.num_labels == 2:
     
      return self.convert_binary_labels()
    
    else:
    
      return self.convert_multiclass_labels()

  def convert_binary_labels(self):
  
    masks = np.zeros(shape=(self.num_examples,),dtype=np.int32)
  
    for n,mask in enumerate(self.masks):
    
      resolution = mask.shape[0] * mask.shape[1]
      start_index = n * resolution
      end_index = ((n+1) * resolution)
    
      masks[start_index:end_index] = mask.reshape((resolution,)).astype(np.int32, casting='safe')
    
    masks = masks/255
    return masks
    
  def convert_multiclass_labels(self):
  
    masks = np.zeros(shape=(self.num_examples,),dtype=np.int32)
  
    #find labels in ALL images
    
    unique_vals = set()
    for mask in self.masks:
      
      unique_vals.update(mask.reshape((mask.shape[0]*mask.shape[1],)).astype(np.int32, casting='safe').tolist())
      
    labels = list(unique_vals)
    labels.sort()
 
    if len(labels) != self.num_labels:
      raise Exception("Error, the number of unique values: {0} does not equal the number of labels: {1}\n".format(len(labels), self.num_labels))
    
   
    #load the mask values (they are not set to label values just now, just to pixel values)
    for n,mask in enumerate(self.masks):
    
      resolution = mask.shape[0] * mask.shape[1]
      start_index = n * resolution
      end_index = ((n+1) * resolution)
      
      masks[start_index:end_index] = mask.reshape((resolution,)).astype(np.int32, casting='safe')
    
    
    for i in range(self.num_examples):
      
      masks[i] = np.int32(labels.index(masks[i]))
          
    return masks    
  
  def train(self):
  
    print("")
    print("Loading training data..."),
    self.training_data = self.convert_training()
    print("done.")
    print("Loading responses..."),
    self.labels = self.convert_labels()
    print("done.")
   
    self.model.setup_params()
    print("Training..."),
    self.model.model.train(self.training_data, 1, self.labels, params=self.model.params)
    print("done.")
    self.model.model.save(self.model.name + "_{0}.xml".format(self.num_labels))

  def find_unique_vals(self, mask):
  
    vals = []
    height = mask.shape[0]
    width = mask.shape[1]
    for r in range(height):
      for c in range(width):
        vals.append(mask[r,c])
    
    vals = set(vals)
    return vals
    
  def predict(self, image):

    predictions = np.zeros(shape=(image.shape[0],image.shape[1],3),dtype=np.uint8)

    cs = ColorSpace(image=image)
    hue = cs.get_hue()
    sat = cs.get_sat()
    o2 = cs.get_o2()
    o3 = cs.get_o3()
    
    if self.num_dims:
      red = image[:,:,0]
      green = image[:,:,1]
      blue = image[:,:,2]

    for r in range(image.shape[0]):
      for c in range(image.shape[1]):
        data = np.zeros(shape=(self.num_dims,),dtype=np.float32)
        
        if self.num_dims == 3:
          data[0] = float(red[r,c])
          data[1] = float(green[r,c])
          data[2] = float(blue[r,c])
        
        else:
          
          data[0] = float(hue[r,c])
          data[1] = float(sat[r,c])
          data[2] = float(o2[r,c])
          data[3] = float(o3[r,c])
          
          if self.num_dims == 7:
            data[4] = float(red[r,c])
            data[5] = float(green[r,c])
            data[6] = float(blue[r,c])
                  
        pred = self.model.model.predict( data )
        if pred == 0:
          predictions[r,c] = [0,0,0]
        elif pred == 1:
          predictions[r,c] = [255,0,0]
        elif pred == 2:
          predictions[r,c] = [0,255,0]
        elif pred == 3:
          predictions[r,c] = [0,0,255]
        else:
          raise Exception("Error, need more colors: {0} for data: {1} at pixel ({2},{3})".format(pred, data,r, c))
        #predictions[r,c] = 255 * self.rf.predict( data  )
    
    return predictions
