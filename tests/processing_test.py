#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# processing_test.py

import os
import logging
import unittest

import numpy as np

import image.processing as processing


class ProcessingTest(unittest.TestCase):

    image_path_list = []
    image_suffix = ('.bmp', '.dib', '.sr', '.ras', '.tiff',
                    '.tif', '.jpeg', '.jpg', '.pxm,', '.pnm',
                    '.jpe', '.png', '.pbm,', '.pgm,', '.ppm')
    script_dir = os.path.dirname(os.path.realpath(__file__))

    @classmethod
    def setUpClass(cls) -> None:
        logging.debug(f'processing version: {processing.__version__}')
        for root, dirs, files in os.walk(cls.script_dir):
            for file in files:
                if file.lower().endswith(cls.image_suffix):
                    image_path = os.path.join(root, file)
                    cls.image_path_list.append(image_path)

    def test_pil_array(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("PIL is not installed")

        for image_path in self.image_path_list:
            array = processing._pil_array(image_path, output_gray=False)
            self.assertIsInstance(array, np.ndarray, msg=f'{image_path}')

        for image_path in self.image_path_list:
            array = processing._pil_array(image_path, output_gray=True)
            self.assertIsInstance(array, np.ndarray)
            self.assertEqual(array.ndim, 2, msg=f'{image_path}')  # black and white has 2 dimensions

        expect_none = processing._pil_array('')  # none existing path returns None
        self.assertIsNone(expect_none)

    def test_cv2_array(self):
        try:
            import cv2
        except ImportError:
            self.skipTest("cv2 is not installed")

        for image_path in self.image_path_list:
            array = processing._cv2_array(image_path, output_gray=False)
            self.assertIsInstance(array, np.ndarray, msg=f'{image_path}')

        for image_path in self.image_path_list:
            array = processing._cv2_array(image_path, output_gray=True)
            self.assertIsInstance(array, np.ndarray)
            self.assertEqual(array.ndim, 2, msg=f'{image_path}')  # black and white has 2 dimensions

        expect_none = processing._cv2_array('')  # none existing path returns None
        self.assertIsNone(expect_none)

    def test_image_to_array(self):
        try:
            import cv2
        except ImportError:
            self.skipTest("cv2 is not installed")

        for image_path in self.image_path_list:
            array = processing.image_to_array(image_path, output_gray=False)
            self.assertIsInstance(array, np.ndarray)

        for image_path in self.image_path_list:
            array = processing.image_to_array(image_path, output_gray=True)
            self.assertIsInstance(array, np.ndarray)
            self.assertEqual(array.ndim, 2)  # black and white has 2 dimensions

        with self.assertRaises(FileNotFoundError):
            processing.image_to_array('this.is.a.test')

    def test_crop_to_smallest(self):
        image_path_list_1 = self.image_path_list
        image_path_list_2 = self.image_path_list.copy()
        first_image = image_path_list_2.pop(0)  # get first image
        image_path_list_2.append(first_image)  # place first image to the back of the list

        for image1_path, image2_path in zip(image_path_list_1, image_path_list_2):

            img_array1 = processing.image_to_array(image1_path, output_gray=True)
            img_array2 = processing.image_to_array(image2_path, output_gray=True)

            array1, array2 = processing.crop_to_smallest(img_array1, img_array2)
            self.assertEqual(array2.shape[:2], array1.shape[:2])


if __name__ == '__main__':
    print("start\n")

    import logging

    console = logging.StreamHandler()
    logging.basicConfig(level=logging.DEBUG, handlers=(console,))
    logging.getLogger("__main__").setLevel(logging.DEBUG)
    logging.captureWarnings(True)

    unittest.main()
