from recolor import ColorSpace
import argparse
import cv2
import numpy as np
if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", type=str, required=True)
    parser.add_argument("--colorspace", type=str, required=True)
    parser.add_argument('--uint8', action="store_true", help='Use uint8 representations.', default=False)
    parser.add_argument('--jet', action="store_true", help='Use jet colorspace representations.', default=False)
    
    args = parser.parse_args()

    image_path = args.image_path
    colorspace = args.colorspace
    
    csp = ColorSpace(image_path, None, args.uint8)
    i = csp.process(colorspace, False)

    if args.jet:
      i = cv2.applyColorMap(i,cv2.COLORMAP_JET)
    #i = 255 * i.astype(np.uint8)
   
    cv2.imwrite(colorspace+".png",i)