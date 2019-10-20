# SSIM-py
## Structural Similarity (SSIM) index, where the core dependency is [NumPy](https://numpy.org/)
##### To actually compare images with SSIM-py [Pillow](https://pypi.org/project/Pillow/) or [opencv-python](https://pypi.org/project/opencv-python/) is needed
---
### Preparation
###### Setting up your environment
1. Download the [SSIM-py.zip](https://github.com/w13b3/SSIM-py/blob/master/SSIM-py.zip)
2. Setup and activate a [virtual environment](https://docs.python.org/3/library/venv.html) (optional)
3. Extract the requirements.txt from the downloaded SSIM-py.zip
4. Open a [command-line interface](https://en.wikipedia.org/wiki/Command-line_interface)
5. Enter the following command on the command-line `pip install -r requirements.txt`

Result: Pillow, opencv-python and numpy modules are installed in the environment.

###### Image comparison preparation
Have two similar images ready to compare.

**For the best result:** 

The module: opencv-python is preferred.

Make sure both images are the same size and have the same amount of [color channels](https://en.wikipedia.org/wiki/Channel_(digital_image))

---
### Usage
1. Open a [command-line interface](https://en.wikipedia.org/wiki/Command-line_interface)
2. Read the help text by entering the following command `python SSIM-py.zip --help` (optional)
3. Enter the following command `python SSIM-py.zip path/to/image1 path/to/image2`

Result: Number between 1 and 0 shows up on the command-line.

###### What to do by failure
Run the command again but now with the `--verbose` argument.

Copy the log into an textfile.

Usefull command to do this with is: `python SSIM-py.zip --verbose path/to/image1 path/to/image2 > SSIM-py.log`

Create an issue with the SSIM-py.log and the images used.

---
### Test information
Created and tested on Ubuntu 18.04.3 LTS

With python 3.6.8 (default, Oct  7 2019, 12:59:55) [GCC 8.3.0]

Pillow: 6.2.0

numpy: 1.17.3

opencv_python: 4.1.1.26

Tested with the following image formats: .tif .png .ppm .pgm .jpg .bmp

CAUTION: Comparing the same images with different file formats with Pillow won't give expected results.

---
### References
Thanks mom, Thanks dad.

[1](https://github.com/obartra/ssim/blob/master/assets/ssim.pdf)
[2](https://en.wikipedia.org/wiki/Structural_similarity)
[3](https://scikit-image.org/docs/dev/auto_examples/transform/plot_ssim.html)
[4](https://blog.csdn.net/weixin_42096901/article/details/90172534)
[5](https://github.com/tensorflow/models/blob/master/research/compression/image_encoder/msssim.py)
[6](https://stackoverflow.com/users/7567938/allosteric)
[7](https://songhuiming.github.io/pages/2017/04/16/convolve-correlate-and-image-process-in-numpy/)
[8](https://github.com/nichannah/gaussian-filter/blob/master/gaussian_filter.py)
[9](https://homepages.cae.wisc.edu/~ece533/images/)
[10](https://www.petitcolas.net/watermarking/image_database/)
