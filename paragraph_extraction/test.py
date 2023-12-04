# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 22:23:17 2023

@author: mazym
"""

import cv2
from matplotlib import pyplot as pt
import numpy as np

# Read the first image 
first_img = cv2.imread('005.png', 0)
sample_img = cv2.imread('paragraph 1 sample.png', 0)
[nrow, ncol] = first_img.shape


GaussianFilter= cv2.GaussianBlur(first_img, (7,7), 0, cv2.BORDER_DEFAULT)
hist = cv2.calcHist([GaussianFilter], [0], None, [256], [0,256])
_, binarizedImage = cv2.threshold(GaussianFilter, 200, 255, cv2.THRESH_BINARY)

#white is 0, black is 1 
binarizedImage[binarizedImage == 0] = 1
binarizedImage[binarizedImage == 255] = 0


#Removing table spanning all columns
def remove_table_1col(ncol):
    table_row = []
    horizontal_projection1 = np.sum(
        binarizedImage, axis=1)
    for row in range (horizontal_projection1.shape[0]):
        if horizontal_projection1[row] > 0.8 * ncol:
            table_row.append(row)
    binarizedImage[table_row[0] : table_row[-1], :] = 0

remove_table_1col(ncol) 

