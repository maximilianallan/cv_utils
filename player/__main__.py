from player import VideoPlayer, combine_images, compare_images
import argparse
import cv2

if __name__ == '__main__':

  
  parser = argparse.ArgumentParser(description='Simple video player for finding the pose of an object in the video at a particular frame using visual inspection.')

  parser.add_argument('-v', '--video-file', type=str, help='The video file to be played.', required=True)
  parser.add_argument('-p', '--pose-file', type=str, help='The pose file to be processed alongside the video file.', required=True)
  parser.add_argument('-i', '--image-file', type=str, help='The image file to display alongside the video frame to match', required=True)
  parser.add_argument('-a', '--auto', action='store_true')

  args = parser.parse_args()

  bpf = VideoPlayer(args.video_file, args.pose_file, args.image_file)

  if args.auto:

    min_diff = 99999999
    best_image = None
    best_pose = None

    while True:
      if not bpf.load_new():
        break
      diff = compare_images(bpf.get_current_frame(), bpf.image)
      if diff < min_diff:
        min_diff = diff
        best_image = bpf.get_current_frame()
        best_pose = bpf.get_current_pose()

    if best_image is not None:
      print("Found match with average distance: {0}!".format(min_diff))
      cv2.namedWindow("Match")
      cv2.imshow("Match", combine_images(best_image, bpf.image))
      print best_pose
      cv2.waitKey(-1)



  else:

    cv2.namedWindow("output")

    play = True

    count = 0

    while True:

      if play == True:

        if bpf.index + 1 == len(bpf.frames):

          if not bpf.load_new():
            break

        else:
          bpf.index += 1


      cv2.imshow("output", combine_images(bpf.get_current_frame(), bpf.image))

      key = cv2.waitKey(8)

      if key & 255 == ord(' '):
        play = not play


      if key == 2424832:
        play = False
        bpf.rewind()

      if key == 2555904:
        play = False
        if not bpf.forward():
          break


      if key & 255 == ord('m'):
        play = False
        print bpf.get_current_pose()

      if key & 255 == ord('q'):
        play = False
        cv2.destroyAllWindows()
        break