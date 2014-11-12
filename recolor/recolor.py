import cv2
import argparse
import numpy as np

class ColorSpace:

    def __init__(self,image_path=None,image=None):

        if image_path is not None:
            self.image = cv2.imread(image_path,1)
        elif image is not None:
            self.image = image
        try:    
            (self.height,self.width,self.chans) = self.image.shape
        except:
            (self.height,self.width) = self.image.shape
            self.chans = 1

    def process(self,target_colorspace):
        
        if target_colorspace == "hue":
            return cv2.applyColorMap(self.get_hue(),cv2.COLORMAP_HSV)
        elif target_colorspace == "sat":
            return cv2.applyColorMap(self.get_sat(),cv2.COLORMAP_HSV)
        elif target_colorspace == "o2":
            return cv2.applyColorMap(self.get_o2(),cv2.COLORMAP_HSV)
        elif target_colorspace == "o3":
            return cv2.applyColorMap(self.get_o3(),cv2.COLORMAP_HSV)
        else:
            raise Exception("Error, unsupported color space specified")

    def get_hue(self):
        
        hsv = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)
        return hsv[:,:,0]

    def get_sat(self):

        hsv = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)
        return hsv[:,:,1]   
    
    def get_o2(self):

        o2 = np.array( map(self.bgr2o2, np.reshape(self.image,(self.width*self.height,self.chans))),dtype=np.float32)#
        return np.reshape(o2,(self.height,self.width))
        #return np.reshape(o2,(self.height,self.width)).astype(np.uint8,copy=False) - THIS IS BAD AS THE VALUES CANNOT MAP To 0-255
        
    def get_o3(self):
        
        o3 = np.array(map(self.bgr2o3,np.reshape(self.image,(self.width*self.height,self.chans))),dtype=np.float32)
        return np.reshape(o3,(self.height,self.width))#.astype(np.uint8,copy=False)
        
    def bgr2o2(self,x):

        #try:            
        return 0.5*(float(x[2])-float(x[1]))
        #except:
        #return 0

    def bgr2o3(self,x):

        #try:
        return (0.5*float(x[0])) - 0.25*(float(x[2])+float(x[1]))
        #except:
        #    return 0


if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument("image_path")
    parser.add_argument("colorspace")
    args = parser.parse_args()

    image_path = args.image_path
    colorspace = args.colorspace
    
    csp = ColorSpace(image_path)
    i = csp.process(colorspace)
 
    hm = cv2.applyColorMap(i,cv2.COLORMAP_HSV)
    cv2.imwrite(colorspace+".png",hm)
    
