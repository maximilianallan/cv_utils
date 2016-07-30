import cv2
import numpy as np

import os
p = os.path.realpath(__file__)
p = os.path.dirname(p) + "/../"
import sys
sys.path.append(p)
from recolor import ColorSpace

import gc

all_features = ["red","green","blue","hue","sat","value","L","a","b","o1","o2","gabor"]
features = ["red","a","o1", "gabor"]
#features = ["hue","sat","o1","o2"]

def get_index(feature):
    return features.index(feature)

def build_filters():
    filters = []
    ksize = 31
    for theta in np.arange(0, np.pi, np.pi / 16):
        kern = cv2.getGaborKernel((ksize, ksize), 4.0, theta, 10.0, 0.5, 0, ktype=cv2.CV_32F)
        kern /= 1.5*kern.sum()
        filters.append(kern)
    return filters

def process(img, filters):
    accum = np.zeros_like(img)
    for kern in filters:
        fimg = cv2.filter2D(img, cv2.CV_32FC3, kern)
        np.maximum(accum, fimg, accum)
    return accum


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

class RandomForest(Model):

  def __init__(self):
    super(RandomForest, self).__init__()
    self.model = cv2.RTrees()
    self.name = "RF"
    
  def setup_params(self):
    self.params = dict(term_crit=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER , 5 , 0.001) )
  
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

        self.image_paths = image_paths
        self.mask_paths = mask_paths

        self.num_examples = 0
        self.num_labels = num_labels

        for im_path, mask_path in zip(self.image_paths, self.mask_paths):
            im = cv2.imread(im_path)
            mask = cv2.imread(mask_path,0)
            if im is None or mask is None:
                continue

            self.num_examples += im.shape[0]*im.shape[1]
            del im
            del mask
            gc.collect()

    #  if im is None or mask is None:
    #    pass
    #  else:
    #   self.images.append(im)
    #   self.masks.append(mask)


    #tmp_images = [cv2.imread(im_path) for im_path in image_paths]
    #tmp_masks = [cv2.imread(mask_path,0) for mask_path in mask_paths]
    
    #self.images = []
    #self.masks = []
    
    #for im, mask in zip(tmp_images, tmp_masks):
    #  if im is None or mask is None:
    #    pass
    #  else:
    #    self.images.append(im)
    #    self.masks.append(mask)

    #if len(self.images) != len(self.masks):
    #  raise Exception("Error, number of images files ({0}) does not match number of mask files ({1})! Exiting...\n".format(len(self.images), len(self.masks)))
    #if len(self.images) == 0:
    #  raise Exception("Error, no files found! Exiting...\n")
    
    #self.num_examples = sum([im.shape[0]*im.shape[1] for im in self.images])
    #self.num_labels = num_labels
    
    def convert_training(self):

        self.num_dims = len(features)

        import time

        print("Allocating {0} bytes of training data\n".format(self.num_examples*4*self.num_dims))
        training_data = np.zeros(shape=(self.num_examples,self.num_dims),dtype=np.float32)
   


        for n,image_path in enumerate(self.image_paths):

            image = cv2.imread(image_path)
            resolution = image.shape[0] * image.shape[1]
      
            start_index = n * resolution
            end_index = ((n+1) * resolution)

            """
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
                o1 = cs.get_o1()
                o2 = cs.get_o2()
                training_data[start_index:end_index,0] = hue.reshape((resolution,)).astype(np.float32, casting='safe')
                training_data[start_index:end_index,1] = sat.reshape((resolution,)).astype(np.float32, casting='safe')
                training_data[start_index:end_index,2] = o1.reshape((resolution,)).astype(np.float32, casting='safe')
                training_data[start_index:end_index,3] = o2.reshape((resolution,)).astype(np.float32, casting='safe')

            if self.num_dims == 7:
                red = image[:,:,0]
                green = image[:,:,1]
                blue = image[:,:,2]
                training_data[start_index:end_index,4] = red.reshape((resolution,)).astype(np.float32, casting='safe')
                training_data[start_index:end_index,5] = green.reshape((resolution,)).astype(np.float32, casting='safe')
                training_data[start_index:end_index,6] = blue.reshape((resolution,)).astype(np.float32, casting='safe')

            #filters = build_filters()
            #filters = np.asarray(filters)
            #image_gray = cv2.imread(image_path,0)
            #gabor_vals = process(image_gray, filters)
            #training_data[start_index:end_index,self.num_dims] = gabor_vals.reshape((resolution,)).astype(np.float32, casting='safe')
        """

            cs = ColorSpace(image=image)
            red = cs.get_red()
            green = cs.get_green()
            blue = cs.get_blue()
            hue = cs.get_hue()
            sat = cs.get_sat()
            value = cs.get_value()
            o1 = cs.get_o1()
            o2 = cs.get_o2()
            gabor = cs.get_gabor()
            l = cs.get_cielab_l()
            a = cs.get_cielab_a()
            b = cs.get_cielab_b()

            if "red" in features:
                print "adding red at " + str(get_index("red"))            
                training_data[start_index:end_index,get_index("red")] = red.reshape((resolution,))

            if "green" in features:
                print "adding green at " + str(get_index("green"))            
                training_data[start_index:end_index,get_index("green")] = green.reshape((resolution,))

            if "blue" in features:
                print "adding blue at " + str(get_index("blue"))            
                training_data[start_index:end_index,get_index("blue")] = blue.reshape((resolution,))

            if "hue" in features:
                print "adding hue at " + str(get_index("hue"))
                training_data[start_index:end_index,get_index("hue")] = hue.reshape((resolution,))

            if "sat" in features:
                print "adding sat at " + str(get_index("sat"))
                training_data[start_index:end_index,get_index("sat")] = sat.reshape((resolution,))

            if "value" in features:
                print "adding value at " + str(get_index("value"))
                training_data[start_index:end_index,get_index("value")] = value.reshape((resolution,))

            if "L" in features:
                print "adding L at " + str(get_index("L"))            
                training_data[start_index:end_index,get_index("L")] = l.reshape((resolution,))

            if "a" in features:
                print "adding a at " + str(get_index("a"))            
                training_data[start_index:end_index,get_index("a")] = a.reshape((resolution,))

            if "b" in features:
                print "adding b at " + str(get_index("b"))            
                training_data[start_index:end_index,get_index("b")] = b.reshape((resolution,))

            if "o1" in features:
                print "adding o1 at " + str(get_index("o1"))
                training_data[start_index:end_index,get_index("o1")] = o1.reshape((resolution,))

            if "o2" in features:
                print "adding o2 at " + str(get_index("o2"))
                training_data[start_index:end_index,get_index("o2")] = o2.reshape((resolution,))

            if "gabor" in features:
                print "adding gabor at " + str(get_index("gabor"))            
                training_data[start_index:end_index,get_index("gabor")] = gabor.reshape((resolution,))


        return training_data

    def convert_labels(self):
  
        if self.num_labels == 2:
     
            return self.convert_binary_labels()
    
        else:
    
            return self.convert_multiclass_labels()

    def convert_binary_labels(self):
  
        masks = np.zeros(shape=(self.num_examples,),dtype=np.int32)
  
        for n,mask_path in enumerate(self.mask_paths):

            mask = cv2.imread(mask_path,0)
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
        for mask_path in self.mask_paths:
            mask = cv2.imread(mask_path,0)
            unique_vals.update(mask.reshape((mask.shape[0]*mask.shape[1],)).astype(np.int32, casting='safe').tolist())
      
        labels = list(unique_vals)
        labels.sort()
 
        if len(labels) != self.num_labels:
            raise Exception("Error, the number of unique values: {0} does not equal the number of labels: {1}\nFound values are: {2}\n".format(len(labels), self.num_labels, labels))
    

        #load the mask values (they are not set to label values just now, just to pixel values)
        for n,mask_path in enumerate(self.mask_paths):

            mask = cv2.imread(mask_path,0)

            resolution = mask.shape[0] * mask.shape[1]
            start_index = n * resolution
            end_index = ((n+1) * resolution)

            masks[start_index:end_index] = mask.reshape((resolution,)).astype(np.int32, casting='safe')
    
    
        for i in range(self.num_examples):

            masks[i] = np.int32(labels.index(masks[i]))

        return masks

    def extract_positives(self, training_data, labels):

        num_positives = 0
        for i in range(self.num_examples):
            if labels[i] > 0:
                num_positives += 1

        new_training_data = np.zeros(shape=(num_positives,self.num_dims) , dtype=np.float32)
        new_labels = np.zeros(shape=(num_positives,),dtype=np.int32)

        c = 0
        for i in range(self.num_examples):
            if labels[i] > 0:
                new_training_data[c,:] = training_data[i,:]
                new_labels[c] = labels[i]
                c += 1

        return new_training_data, new_labels

    def rebalance_classes_2class(self, training_data, labels):
    
        positive_indexes = [ i for i in range(self.num_examples) if labels[i] > 0]
        negative_indexes = list(set(range(self.num_examples)) - set(positive_indexes))
        
        from random import shuffle
        
        shuffle(positive_indexes)
        shuffle(negative_indexes)
        
        
        if len(positive_indexes) < len(negative_indexes):
            
            partial_negative_indexes = negative_indexes[:len(positive_indexes)]
            negative_indexes = partial_negative_indexes 
            
        else:            
        
            partial_positive_indexes = positive_indexes[:len(negative_indexes)]
            positive_indexes = partial_positive_indexes 
            
        new_training_data = training_data[positive_indexes + negative_indexes,:]
        new_labels = labels[positive_indexes + negative_indexes]
        return new_training_data, new_labels
        
    def rebalance_classes_multiclass(self, training_data, labels):
    
        all_indexes = set(labels)
        index_vals = {}
        from random import shuffle
        
        for p in all_indexes:
            index_vals[p] = [ i for i in range(self.num_examples) if labels[i] == p]
            shuffle(index_vals[p])
        
        len_shortest = min([len(index_vals[l]) for l in index_vals])
         
        
        for p in index_vals:
          
            index_vals[p] = index_vals[p][:len_shortest]
            
        all_indexes = []
        for p in index_vals:
          
            all_indexes += index_vals[p] 
            
        new_training_data = training_data[all_indexes,:]
        new_labels = labels[all_indexes]
        return new_training_data, new_labels    
        
    def train(self, save_path = None):

        print("")
        print("Loading training data..."),
        self.training_data = self.convert_training()
        print("done.")
        print("Loading responses..."),
        self.labels = self.convert_labels()
        print("done.")

        self.training_data, self.labels = self.rebalance_classes_multiclass(self.training_data, self.labels)
        #self.training_data, self.labels = self.extract_positives(self.training_data, self.labels)

        self.model.setup_params()
        print("Training..."),
        self.model.model.train(self.training_data, 1, self.labels, params=self.model.params)
        print("done.")
        if save_path is not None:
            self.model.model.save(save_path)
        else:  
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

        #try:
        #    self.background_sub
        #except AttributeError:
        #    self.background_sub = cv2.BackgroundSubtractorMOG()
        #    cv2.namedWindow("test")


        #fgmask = self.background_sub.apply(image, learningRate=0.001)
        #cv2.imshow("test", fgmask)
        #k = cv2.waitKey(10)

        #if k & 255 == ord("q"):
        #    cv2.destroyAllWindows()
        #    sys.exit(0)

        #return

        predictions = np.zeros(shape=(image.shape[0],image.shape[1],3),dtype=np.uint8)

        cs = ColorSpace(image=image)
        red = cs.get_red()
        green = cs.get_green()
        blue = cs.get_blue()
        hue = cs.get_hue()
        sat = cs.get_sat()
        value = cs.get_value()
        o1 = cs.get_o1()
        o2 = cs.get_o2()
        gabor = cs.get_gabor()
        l = cs.get_cielab_l()
        a = cs.get_cielab_a()
        b = cs.get_cielab_b()

        #filters = build_filters()
        #filters = np.asarray(filters)
        #image_gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
        #gabor_vals = process(image_gray, filters)

        resolution = image.shape[0]*image.shape[1]
        eval_data = np.zeros(shape=(resolution, self.num_dims), dtype=np.float32)

        if "red" in features:
            eval_data[:,get_index("red")] = red.reshape((resolution,))

        if "green" in features:
            eval_data[:,get_index("green")] = green.reshape((resolution,))

        if "blue" in features:
            eval_data[:,get_index("blue")] = blue.reshape((resolution,))

        if "hue" in features:
            eval_data[:,get_index("hue")] = hue.reshape((resolution,))

        if "sat" in features:
            eval_data[:,get_index("sat")] = sat.reshape((resolution,))

        if "value" in features:
            eval_data[:,get_index("value")] = value.reshape((resolution,))

        if "L" in features:
            eval_data[:,get_index("L")] = l.reshape((resolution,))

        if "a" in features:
            eval_data[:,get_index("a")] = a.reshape((resolution,))

        if "b" in features:
            eval_data[:,get_index("b")] = b.reshape((resolution,))

        if "o1" in features:
            eval_data[:,get_index("o1")] = o1.reshape((resolution,))

        if "o2" in features:
            eval_data[:,get_index("o2")] = o2.reshape((resolution,))

        if "gabor" in features:
            eval_data[:,get_index("gabor")] = gabor.reshape((resolution,))

        for r in range(image.shape[0]):
            for c in range(image.shape[1]):

                idx = r * image.shape[1] + c
                data = eval_data[idx,:]

                """
                data = np.zeros(shape=(self.num_dims,),dtype=np.float32)

                if "red" in features >= 0:
                    data[get_index("red")] = red[r,c]

                if "green" in features >= 0:
                    data[get_index("green")] = green[r,c]

                if "blue" in features >= 0:
                    data[get_index("blue")] = blue[r,c]

                if "hue" in features >= 0:
                    data[get_index("hue")] = hue[r,c]

                if "sat" in features >= 0:
                    data[get_index("sat")] = sat[r,c]

                if "value" in features >= 0:
                    data[get_index("value")] = value[r,c]

                if "L" in features >= 0:
                    data[get_index("L")] = l[r,c]

                if "a" in features >= 0:
                    data[get_index("a")] = a[r,c]

                if "b" in features >= 0:
                    data[get_index("b")] = b[r,c]

                if "o1" in features >= 0:
                    data[get_index("o1")] = o1[r,c]

                if "o2" in features >= 0:
                    data[get_index("o2")] = o2[r,c]

                if "gabor" in features >= 0:
                    data[get_index("gabor")] = gabor[r,c]


                #if fgmask[r,c] == 0:
                #    predictions[r,c] = [0,0,0]
                """
                """
                if self.num_dims == 3:
                    data[0] = float(red[r,c])
                    data[1] = float(green[r,c])
                    data[2] = float(blue[r,c])

                else:

                    data[0] = float(hue[r,c])
                    data[1] = float(sat[r,c])
                    data[2] = float(o1[r,c])
                    data[3] = float(o2[r,c])

                if self.num_dims == 7:
                    data[4] = float(red[r,c])
                    data[5] = float(green[r,c])
                    data[6] = float(blue[r,c])

                """
                #data[self.num_dims] = float(gabor_vals[r,c])

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
