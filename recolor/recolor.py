from cv2 import imread, COLORMAP_HSV, COLOR_BGR2HSV, imwrite, applyColorMap
import cv2
import argparse
import numpy as np

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
        fimg = cv2.filter2D(img, cv2.CV_32F, kern)
        np.maximum(accum, fimg, accum)
    return accum


class ColorSpace:

    def __init__(self,image_path=None,image=None, process_as_uint8 = False):

        if image_path is not None:
            self.image = imread(image_path,1)
        elif image is not None:
            self.image = image
        if not process_as_uint8:
          self.image = self.image.astype(np.float32)
          self.image *= 1.0/255
        
        
          
        try:    
            (self.height,self.width,self.chans) = self.image.shape
        except:
            (self.height,self.width) = self.image.shape
            self.chans = 1

    def process(self,target_colorspace, apply_colormap):
        
        if target_colorspace == "hue":
            i = self.get_hue()
        elif target_colorspace == "sat":
            i = self.get_sat()
        elif target_colorspace == "val":
            i = self.get_value()
        elif target_colorspace == "o1":
            i = self.get_o1()
        elif target_colorspace == "o2":
            i = self.get_o2()
        elif target_colorspace == "L":
            i = self.get_cielab_l()
        elif target_colorspace == "a":
            i = self.get_cielab_a()
        elif target_colorspace == "b":
            i = self.get_cielab_b()
        elif target_colorspace == "red":
            i = self.get_red()
        elif target_colorspace == "green":
            i = self.get_green()
        elif target_colorspace == "blue":
            i = self.get_blue()
        elif target_colorspace == "gabor":
            i = self.get_gabor()
        elif target_colorspace == "gray":
            i = self.get_gray()
        elif target_colorspace == "all":
            i = np.ndarray(shape=(self.image.shape[0],self.image.shape[1],4), dtype=np.float32)
            i[:,:,0] = self.get_hue()
            i[:,:,1] = self.get_sat()
            i[:,:,2] = self.get_o1()
            i[:,:,3] = self.get_o2()
        else:
            raise Exception("Error, unsupported color space specified")

        if apply_colormap == False:
          return i
        else:
          return cv2.applyColorMap(i,cv2.COLORMAP_JET)

    def get_gray(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        if self.image.dtype == np.float32:
          return gray.astype(np.float32)
        else:
          return cv2.normalize(gray, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX).astype(np.uint8)
          
    def get_red(self):
        return self.image[:,:,2]

    def get_green(self):
        return self.image[:,:,1]

    def get_blue(self):
        return self.image[:,:,0]

    def get_hue(self):
        
        hsv = cv2.cvtColor(self.image,COLOR_BGR2HSV)
        if self.image.dtype == np.float32:
          return hsv[:,:,0].astype(np.float32)
        else:
          return cv2.normalize(hsv[:,:,0], alpha=0, beta=255, norm_type=cv2.NORM_MINMAX).astype(np.uint8)#hsv[:,:,0]

    def get_sat(self):
    
        hsv = cv2.cvtColor(self.image,COLOR_BGR2HSV)
        if self.image.dtype == np.float32:
          return hsv[:,:,1].astype(np.float32)
        else:
          return hsv[:,:,1]


    def get_value(self):

        hsv = cv2.cvtColor(self.image,COLOR_BGR2HSV)
        if self.image.dtype == np.float32:
          return hsv[:,:,2].astype(np.float32)
        else:
          return hsv[:,:,2]

    def get_o1(self):

        o1 = np.array( map(self.bgr2o1, np.reshape(self.image,(self.width*self.height,self.chans))),dtype=np.float32)#
        o1 = np.reshape(o1,(self.height,self.width))
        if self.image.dtype == np.float32:
          return o1
        else:
          """
          from sklearn.preprocessing import MinMaxScaler
          m = MinMaxScaler(feature_range=(0,255))
          m.fit(o1)
          return m.transform(o1).astype(np.uint8)
          """
          return cv2.normalize(o1, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX).astype(np.uint8)           
          
          
        #return np.reshape(o2,(self.height,self.width)).astype(np.uint8,copy=False) - THIS IS BAD AS THE VALUES CANNOT MAP To 0-255
        
    def get_o2(self):
        
        o2 = np.array(map(self.bgr2o2,np.reshape(self.image,(self.width*self.height,self.chans))),dtype=np.float32)
        o2 = np.reshape(o2,(self.height,self.width))#.astype(np.uint8,copy=False)
        if self.image.dtype == np.float32:
          return o2
        else:
          """from sklearn.preprocessing import MinMaxScaler
          m = MinMaxScaler(feature_range=(0,255))
          m.fit(o2)
          return m.transform(o2).astype(np.uint8)
          """
          return cv2.normalize(o2, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX).astype(np.uint8)           
          
    def bgr2o1(self,x):

        #try:            
        return 0.5*(float(x[2])-float(x[1]))
        #except:
        #return 0

    def bgr2o2(self,x):


        return (0.5*float(x[0])) - 0.25*(float(x[2])+float(x[1]))
        #except:
        #    return 0


    def get_gabor(self):
        
          
        filters = build_filters()         
        filters = np.asarray(filters)
        im = self.image
        if self.image.dtype != np.float32:
          im = im.astype(np.float32)
          im = im * 1.0/255
        image_gray = cv2.cvtColor(im, cv2.cv.CV_BGR2GRAY)
        gabor_vals = process(image_gray, filters)
        if self.image.dtype == np.float32:
          return gabor_vals.astype(np.float32, casting='safe')
        else:
           #from sklearn.preprocessing import MinMaxScaler
           #m = MinMaxScaler(feature_range=(0,255))
           #m.fit(gabor_vals)
           #return m.transform(gabor_vals).astype(np.uint8)
           #(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gabor_vals)
           return cv2.normalize(gabor_vals, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX).astype(np.uint8)           
          
  
    def get_cielab_l(self):

        cie = cv2.cvtColor(self.image,cv2.cv.CV_BGR2Lab)
        if self.image.dtype == np.float32:
          return cie[:,:,0].astype(np.float32)
        else:
          return cie[:,:,0]

    def get_cielab_a(self):

        cie = cv2.cvtColor(self.image,cv2.cv.CV_BGR2Lab)
        if self.image.dtype == np.float32:
          return cie[:,:,1].astype(np.float32)
        else:
          return cv2.normalize(cie[:,:,1], alpha=0, beta=255, norm_type=cv2.NORM_MINMAX).astype(np.uint8)

    def get_cielab_b(self):

        cie = cv2.cvtColor(self.image,cv2.cv.CV_BGR2Lab)
        if self.image.dtype == np.float32:
          return cie[:,:,2].astype(np.float32)
        else:
          return cv2.normalize(cie[:,:,2], alpha=0, beta=255, norm_type=cv2.NORM_MINMAX).astype(np.uint8)

if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument("image_path")
    parser.add_argument("colorspace")
    args = parser.parse_args()

    image_path = args.image_path
    colorspace = args.colorspace
    
    csp = ColorSpace(image_path)
    i = csp.process(colorspace)
 
    hm = applyColorMap(i,cv2.COLORMAP_JET)
    imwrite(colorspace+".png",hm)
    
