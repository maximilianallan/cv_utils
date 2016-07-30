__author__ = 'max'

from player import VideoPlayer
import argparse
import cv2

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Simple video player for which allows frame by frame viewing.')
	parser.add_argument('-v', '--video-file', type=str, help='The video file to be played.', required=True)
	args = parser.parse_args()

	bpf = VideoPlayer(args.video_file)

	cv2.namedWindow("output")

	play = False
	first = True

	count = 0

	while True:

		if play == True or first == True:
      
			first = False
      
			if bpf.index + 1 == len(bpf.frames):

				if not bpf.load_new():
					break


			else:
				bpf.index += 1


		cv2.imshow("output", bpf.get_current_frame())

		key = cv2.waitKey(8)

		if key & 255 == ord(' '):
			play = not play

		if key == 37 or key == 2424832:
			play = False
			bpf.rewind()

		if key == 39 or key == 2555904:
			play = False
			if not bpf.forward():
				break


		if key & 255 == ord('q'):
			play = False
			cv2.destroyAllWindows()
			break


