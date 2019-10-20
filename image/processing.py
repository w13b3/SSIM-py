#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# processing.py
# https://github.com/w13b3/SSIM-py

import os
import logging
from contextlib import suppress

import numpy as np

cv2 = None  # try to import opencv-python
with suppress(ModuleNotFoundError):
    import cv2
    logging.debug(f'opencv-python version: {cv2.__version__}')

Image = None  # try to import Pillow
with suppress(ModuleNotFoundError):
    from PIL import Image, __version__
    logging.debug(f'Pillow version: {__version__}')

if not any((cv2, Image)):  # if neither opencv-python or Pillow are installed
    msg = 'Expected either cv2 (opencv-python) or PIL (Pillow) to be installed.'
    logging.error(msg=msg)
    raise ModuleNotFoundError(msg)


__version__ = '1.0.0'
logging.debug(f'processing version: {__version__}')
logging.debug(f'PIL.Image: {type(Image)}')  # check if modules are imported
logging.debug(f'cv2: {type(cv2)}')          # if not result: <class 'NoneType'>


def _cv2_array(image_path: str, output_gray: bool = False) -> (np.array, None):
    """ turn an image into an array with cv2 """
    logging.info(f'_cv2_array: Input image_path {image_path}')
    logging.info(f'_cv2_array: output_gray {output_gray}')
    array = None
    with suppress(cv2.error):
        array = cv2.imread(image_path, int(not bool(output_gray)))
    logging.debug(f'_cv2_array: output type {type(array)}')
    return array  # -> (np.array or None)


def _pil_array(image_path: str, output_gray: bool = False) -> (np.array, None):
    """ turn an image into an array with PIL.Image """
    logging.info(f'_pil_array: Input image_path {image_path}')
    logging.info(f'_pil_array: output_gray {output_gray}')
    array = None
    with suppress(FileNotFoundError):
        with open(image_path, 'rb') as readbytes:
            open_image = Image.open(readbytes)
            if bool(output_gray):
                # open_image.load()
                open_image = open_image.convert('L')
            array = np.asarray(open_image)
    logging.debug(f'_pil_array: output type {type(array)}')
    return array  # -> (np.array or None)


def image_to_array(image_path: str, output_gray: bool = False) -> np.ndarray:
    """
    Turns an image into an array with PIL or cv2.
    cv2 preferred over PIL.

    Parameters
    ----------
    image_path  str  path to the image.
    output_gray  bool  True returns a grayscale array.

    Raises
    ------
    FileNotFoundError  if the path to the image is not found.
    ValueError  if the conversion to array failed and None is returned.

    Returns
    -------
    image_array  numpy.ndarray  array with a value representation of the given image.
    """
    logging.info(f'image_to_array: Input image_path {image_path}')
    logging.info(f'image_to_array: output_gray {output_gray}')
    image = os.path.realpath(image_path)  # get the absolute path
    if not os.path.exists(image):
        msg = f'No such file or directory: {image_path}'
        logging.error(msg=msg)
        raise FileNotFoundError(msg)

    # cv2 preferred over PIL
    array_func = _cv2_array if cv2 is not None else _pil_array
    image_array = array_func(image, output_gray)
    if image_array is None:
        msg = f'Image could not be converted to array: {image_path}'
        logging.error(msg=msg)
        ValueError(msg)

    return image_array  # -> np.ndarray


def crop_to_smallest(array1: np.ndarray, array2: np.ndarray) -> (np.ndarray, np.ndarray):
    """
    Crops the given array's to the smallest height and width of both array's.
    if both images already have the same height and width, nothing will be cropped.

    Parameters
    ----------
    array1  numpy.ndarray  input array to crop
    array2  numpy.ndarray  input array to crop

    Raises
    ------
    ValueError  if given arrays doesn't have 2 or more dimensions

    Returns
    -------
    array1  numpy.ndarray  cropped to the smallest height and width
    array2  numpy.ndarray  cropped to the smallest height and width
    """
    if array1.ndim < 2 or array2.ndim < 2:
        msg = 'Expected given array\'s to have at least 2 dimensions'
        logging.error(msg=msg)
        raise ValueError(msg)

    size1_y, size1_x = array1.shape[:2]  # get y and x values of both arrays
    size2_y, size2_x = array2.shape[:2]
    logging.info(f'crop_to_smallest: array1 size_y {size1_y}, size_x {size1_x}')
    logging.info(f'crop_to_smallest: array2 size_y {size2_y}, size_x {size2_x}')

    size_y, size_x = min(size1_y, size2_y), min(size1_x, size2_x)  # get minimum x and y value
    array1, array2 = array1[0:size_y, 0:size_x], array2[0:size_y, 0:size_x]  # crop according minimum

    logging.debug(f'crop_to_smallest: cropped arrays to size_y {size_y}, size_x {size_x}')
    return array1, array2  # -> (np.ndarray, np.ndarray)


if __name__ == '__main__':
    print('start\n')

    import logging
    console = logging.StreamHandler()
    logging.basicConfig(level=logging.DEBUG, handlers=(console,))
    logging.getLogger('__main__').setLevel(logging.DEBUG)
    logging.captureWarnings(True)
