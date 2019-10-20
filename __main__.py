#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __main__.py
# https://github.com/w13b3/SSIM-py

import sys
import logging
import argparse


__version__ = '1.0.0'


description = """
This is the --help information
------------------------------
Compares two given images and returns a score between 0 and 1.
The score is calculated with Structural Similarity (SSIM) index method.
 
Best result is given if both images are the same height and width.
Converts the images to B/W if given images doesn't have the same channels.
"""


def parse_args():
    parser = argparse.ArgumentParser(usage='use "%(prog)s --help" for more information',
                                     description=description,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('image1', type=str,
                        help='path to image one')
    parser.add_argument('image2', type=str,
                        help='path to image two')
    parser.add_argument('-g', '--gray', action='store_true',
                        help='convert images to gray before comparison')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', action='store_true',
                       help='show initial arguments and logging')
    group.add_argument('-q', '--quiet', action='store_true',
                       help='show nothing, not even the score of the comparison')
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    # get arguments
    arguments = parse_args()

    if arguments.verbose:  # enable to show logging if -v or --verbose
        sys.stdout.write('Python: %s\n' % sys.version)

        for key, val in vars(arguments).items():
            sys.stdout.write('%s: %s\n' % (key, val))

        # stream to sys.stdout so piping is enabled, example:
        # python SSIM-py.zip --verbose path/to/image1 path/to/image2 > SSIM-py.log
        # stdout = logging.StreamHandler(stream=sys.stdout)
        stdout = logging.StreamHandler()
        logging.basicConfig(level=logging.DEBUG, handlers=(stdout,))
        logging.getLogger("__main__").setLevel(logging.DEBUG)
        logging.captureWarnings(True)

    # import SSIM-py packages here so verbosity/logging can be activated
    from image.ssim import structural_similarity
    from image.processing import image_to_array, crop_to_smallest

    logging.debug(f'main version: {__version__}')

    # compare images
    img1_arr = image_to_array(arguments.image1, output_gray=arguments.gray)
    img2_arr = image_to_array(arguments.image2, output_gray=arguments.gray)

    # if both image dimensions compare the images to Black/White.
    # happens when Black/White and RedGreenBlue images are compared.
    if img1_arr.ndim != img2_arr.ndim:
        sys.stdout.write('WARNING: images given have different dimensions\n')
        sys.stdout.write('\tConverting given images to Black/White before comparison\n')
        img1_arr = image_to_array(arguments.image1, output_gray=True)
        img2_arr = image_to_array(arguments.image2, output_gray=True)

    img1_crop, img2_crop = crop_to_smallest(img1_arr, img2_arr)
    ssim_score, ssim_map = structural_similarity(img1_crop, img2_crop)

    # show result if not -q or --quiet
    if not arguments.quiet:
        score = 'Score: ' if arguments.verbose else ''
        newline = '\n' if arguments.verbose else ''
        sys.stdout.write('%s%s%s' % (score, float(ssim_score), newline))
