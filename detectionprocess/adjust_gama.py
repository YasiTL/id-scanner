# import the necessary packages
from __future__ import print_function
import numpy as np
import argparse
import cv2
import os

img_counter = 0
path = 'images'


def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)


for file in os.listdir(path):
    filename = os.fsdecode(file)
    if filename.endswith(".png") and img_counter < 20:
        image_file = os.path.join(path, filename)
        original = cv2.imread(image_file)
        adjusted = adjust_gamma(original, 1.5)
        img_name = "images/opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, adjusted)
        print("{} written!".format(img_name))
        img_counter += 1
