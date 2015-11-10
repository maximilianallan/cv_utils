__author__ = 'max'

import argparse
import cv2


def get_nearest(to_match, set_of_vals):

    return min(set_of_vals, key=lambda x:abs(x-to_match))


if __name__ == '__main__':


    parser = argparse.ArgumentParser(description='Clean up a bitmask.')

    parser.add_argument('-i', '--images', nargs='+', type=str, help='The list of bitmask files.', required=True)
    parser.add_argument('-v', '--vals', nargs='+', type=int, help='The set of values expected in the mask. Nearest neighbor is used to clean up.', required=True)
    parser.add_argument('-f', '--fix-channel', action='store_true', help='Fix any 3 channel images to 1 channel by dropping channel 2 and 3')
    args = parser.parse_args()

    for image in args.images:

        im = cv2.imread(image)

        if im is None:
            continue

        if not len(im.shape) == 2:
            if args.fix_channel:
                im = im[:,:,0]
            else:
                print("Error, image has 3 channels. Specify -f flag to clean these images\n")
                continue

        for r in range(im.shape[0]):
            for c in range(im.shape[1]):
                im[r,c] = get_nearest(im[r,c], args.vals)

        cv2.imwrite(image,im)
        print("Done image {0}".format(image))






