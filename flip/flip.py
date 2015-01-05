import cv2

def flip_video(in_videofile,out_videofile):

    v = cv2.VideoCapture(in_videofile)

    i = v.read()

    if i[0] == False:
        print "Error, could not open video file!"
        return

    size = i[1].shape

    w = cv2.VideoWriter(out_videofile, cv2.VideoWriter_fourcc('D','I','B',' '), 25, (size[1],size[0]))

    while i[0]:

        w.write(flip(i[1]))

        i = v.read()

def flip(frame):

  return cv2.flip(frame,0)
