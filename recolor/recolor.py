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
        fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
        np.maximum(accum, fimg, accum)
    return accum


class ColorSpace:

    def __init__(self,image_path=None,image=None):

        if image_path is not None:
            self.image = imread(image_path,1)
        elif image is not None:
            self.image = image
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
        elif target_colorspace == "o1":
            i = self.get_o1()
        elif target_colorspace == "o2":
            i = self.get_o2()
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
          return cv2.applyColorMap(i,COLORMAP_HSV)
            
    def get_hue(self):
        
        hsv = cv2.cvtColor(self.image,COLOR_BGR2HSV)
        return hsv[:,:,0].astype(np.float32)

    def get_sat(self):

        hsv = cv2.cvtColor(self.image,COLOR_BGR2HSV)
        return hsv[:,:,1].astype(np.float32)


    def get_value(self):

        hsv = cv2.cvtColor(self.image,COLOR_BGR2HSV)
        return hsv[:,:,2].astype(np.float32)


    def get_o1(self):

        o1 = np.array( map(self.bgr2o1, np.reshape(self.image,(self.width*self.height,self.chans))),dtype=np.float32)#
        return np.reshape(o1,(self.height,self.width))
        #return np.reshape(o2,(self.height,self.width)).astype(np.uint8,copy=False) - THIS IS BAD AS THE VALUES CANNOT MAP To 0-255
        
    def get_o2(self):
        
        o2 = np.array(map(self.bgr2o2,np.reshape(self.image,(self.width*self.height,self.chans))),dtype=np.float32)
        return np.reshape(o2,(self.height,self.width))#.astype(np.uint8,copy=False)
        
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
        image_gray = cv2.cvtColor(self.image, cv2.cv.CV_BGR2GRAY)
        gabor_vals = process(image_gray, filters)
        return gabor_vals.astype(np.float32, casting='safe')

if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument("image_path")
    parser.add_argument("colorspace")
    args = parser.parse_args()

    image_path = args.image_path
    colorspace = args.colorspace
    
    csp = ColorSpace(image_path)
    i = csp.process(colorspace)
 
    hm = applyColorMap(i,cv2.COLORMAP_HSV)
    imwrite(colorspace+".png",hm)
    
