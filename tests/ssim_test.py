#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ssim_test.py

import os
import glob
import logging
import unittest
from contextlib import suppress

import numpy as np

import image.processing as processing
import image.ssim as ssim


class SsimTest(unittest.TestCase):
    image_path_list = []
    image_suffix = ('.bmp', '.dib', '.sr', '.ras', '.tiff',
                    '.tif', '.jpeg', '.jpg', '.pxm,', '.pnm',
                    '.jpe', '.png', '.pbm,', '.pgm,', '.ppm')
    script_dir = os.path.dirname(os.path.realpath(__file__))

    @classmethod
    def setUpClass(cls) -> None:
        logging.debug(f'ssim version: {ssim.__version__}')
        logging.debug(f'processing version: {processing.__version__}')
        for root, dirs, files in os.walk(cls.script_dir):
            for file in files:
                if file.lower().endswith(cls.image_suffix):
                    image_path = os.path.join(root, file)
                    cls.image_path_list.append(image_path)

    def setUp(self) -> None:
        cv2 = None  # try to import cv2
        with suppress(ModuleNotFoundError):
            import cv2

        Image = None  # try to import PIL.Image
        with suppress(ModuleNotFoundError):
            from PIL import Image

        if not any((cv2, Image)):
            msg = 'Expected either cv2 (opencv-python) or PIL (Pillow) to be installed.'
            self.skipTest(msg)

    def test_structural_similarity_same_images(self):
        # test if SSIM score is 1.0 if both images are the same
        for image_path in self.image_path_list:
            image_array = processing.image_to_array(image_path)
            ssim_score, ssim_map = ssim.structural_similarity(image_array, image_array)
            self.assertEqual(ssim_score, 1.0)
            self.assertIsInstance(ssim_map, np.ndarray)

    def test_structural_similarity_different_images(self):
        # test if SSIM score is less than 1.0 if both images are different
        image_path_list_1 = self.image_path_list
        image_path_list_2 = self.image_path_list.copy()
        first_image = image_path_list_2.pop(0)  # get first image
        image_path_list_2.append(first_image)  # place first image to the back of the list

        # reversed_image_path_list = reversed(self.image_path_list)
        for image1_path, image2_path in zip(image_path_list_1, image_path_list_2):
            image1_array = processing.image_to_array(image1_path)
            image2_array = processing.image_to_array(image2_path)

            # assert image dimensions are the same for test
            if not image1_array.ndim == image2_array.ndim:  # do not test array.shape !!!
                continue   # next iteration

            # Input arrays must have the same size
            image1_array, image2_array = processing.crop_to_smallest(image1_array, image2_array)
            ssim_score, ssim_map = ssim.structural_similarity(image1_array, image2_array)
            self.assertLess(ssim_score, 1.0)
            self.assertIsInstance(ssim_map, np.ndarray)

    def test_structural_similarity_same_images_different_format(self):
        # test if SSIM score is near 1.0 if both images are the same but has a different format
        for image_path in self.image_path_list:
            path, image_with_suffix = os.path.split(image_path)
            image_name, suffix = os.path.splitext(image_with_suffix)
            glob_path = os.path.join(path, f'{image_name}*')  # <path>/<dir>/<img-no-suffix>*
            img_list = glob.glob(glob_path, recursive=False)  # [<path>/<img-no-suffix>.png, <path>/<img-no-suffix>.bmp]

            # if length list is not greater of equal to two (2)
            if not len(img_list) >= 2:
                continue  # next iteration

            image1_path, image2_path = img_list[:2]
            image1_array = processing.image_to_array(image1_path)
            image2_array = processing.image_to_array(image2_path)

            # assert image dimensions are the same for test
            if not image1_array.shape == image2_array.shape:
                continue  # next iteration

            ssim_score, ssim_map = ssim.structural_similarity(image1_array, image2_array)
            msg = f'{image1_path} <~> {image2_path}'
            self.assertLessEqual(ssim_score, 1.0, msg=msg)
            # assertAlmostEqual Delta 0.3 arrays of equal images with different formats are different.
            self.assertAlmostEqual(ssim_score, 1.0, delta=0.3, msg=msg)


if __name__ == '__main__':
    print("start\n")

    import logging
    console = logging.StreamHandler()
    logging.basicConfig(level=logging.DEBUG, handlers=(console,))
    logging.getLogger("__main__").setLevel(logging.DEBUG)
    logging.captureWarnings(True)

    unittest.main()
