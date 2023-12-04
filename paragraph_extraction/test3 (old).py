
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 14:20:02 2023

@author: mazym
"""

import cv2
from matplotlib import pyplot as pt
import numpy as np

#Removing table spanning all columns
def remove_table_1col(ncol):
    table_row = []
    horizontal_projection1 = np.sum(
        binarizedImage, axis=1)
    for row in range (horizontal_projection1.shape[0]):
        if horizontal_projection1[row] > 0.8 * ncol:
            table_row.append(row)
    if len(table_row) > 0:
        binarizedImage[table_row[0] : table_row[-1] + 1] = 0


def vertical_projection(binarizedImage):
    vertical_projection = np.sum(binarizedImage, axis=0)
    state = False
    first_pixel = []
    for column in range (vertical_projection.shape[0]):
        if state == False:
            if vertical_projection[column] >= 1:
                state = True
                first_pixel.append(column)   
                
        if state == True:
            if vertical_projection[column] == 0:
                state = False
                first_pixel.append(column)
    return first_pixel             
    

def horizontal_projection(binarizedImage, interchange_pixel, col):
    state = False
    first_pixel = []
    row_pixel = []
        
    # selected region = (2x-2, 2x-1)
    horizontal_projection_col = np.sum(binarizedImage[:, interchange_pixel[col * 2 - 2]: interchange_pixel[col * 2 - 1]], axis=1)
    for column in range(horizontal_projection_col.shape[0]):
        if state == False:
            if horizontal_projection_col[column] >= 1:
                state = True
                first_pixel.append(column)
                
        if state == True:
            if horizontal_projection_col[column] == 0:
                state = False
                first_pixel.append(column)
   
    # append the starting point into the row pixel
    row_pixel.append(first_pixel[0])
    difference = []
    for pixel_index in range(len(first_pixel) - 1):
        difference.append(first_pixel[pixel_index + 1] - first_pixel[pixel_index])
    for difference_index in range(len(difference)):
        if difference[difference_index] > 30 * 1.5 and difference[difference_index]< 100:
            row_pixel.append(first_pixel[difference_index])
            row_pixel.append(first_pixel[difference_index + 1])

    # append the ending point into the row pixel
    row_pixel.append(first_pixel[-1] + 1)
    
    return row_pixel

def horizontal_projection_image(binarizedImage, col):
    state = False
    first_pixel = []

    # selected region = (2x-2, 2x-1)
    horizontal_projection_col = np.sum(binarizedImage, axis=1)
    for column in range(horizontal_projection_col.shape[0]):
        if state == False:
            if horizontal_projection_col[column] >= 1:
                state = True
                first_pixel.append(column)
                
        if state == True:
            if horizontal_projection_col[column] == 0:
                state = False
                first_pixel.append(column)
    
    return first_pixel

def paragraph(row_pixel, col_pixel, col, n):
    #shift 10 to leave some borders
    paragraph_snap = first_img[row_pixel[n * 2 - 2]-10 : row_pixel[n * 2 - 1]+10, 
                         col_pixel[col*2-2]-10 : col_pixel[col*2-1]+10 ]
    paragraph_snap = ignore_images(paragraph_snap, n)
    return paragraph_snap
    

def ignore_images(paragraph_snap, current_paragraph):
    img = paragraph_snap
    GaussianFilter= cv2.GaussianBlur(img, (7,7), 0, cv2.BORDER_DEFAULT)
    _, img= cv2.threshold(GaussianFilter, 200, 255, cv2.THRESH_BINARY)
    img[img == 0] = 1
    img[img == 255] = 0
    
    row_pixel_paragraph = horizontal_projection_image(img, 1)
    #check if there is only one row in the paragraph
    if len(row_pixel_paragraph) <= 2: 
        current_paragraph+=1
        #recursion, check the next paragraph if it contains image
        return paragraph(row_pixel, col_pixel, chosen_col, current_paragraph)
    
    else:
        return paragraph_snap
    
## Main Code ##

# Read the first image 
first_img = cv2.imread('007.png', 1)
first_img = cv2.cvtColor(first_img, cv2.COLOR_BGR2GRAY)
[nrow, ncol] = first_img.shape

GaussianFilter= cv2.GaussianBlur(first_img, (7,7), 0, cv2.BORDER_DEFAULT)

hist = cv2.calcHist([GaussianFilter], [0], None, [256], [0,256])

_, binarizedImage = cv2.threshold(GaussianFilter, 200, 255, cv2.THRESH_BINARY)

#white is 0, black is 1 
binarizedImage[binarizedImage == 0] = 1
binarizedImage[binarizedImage == 255] = 0

remove_table_1col(ncol)
col_pixel = vertical_projection(binarizedImage)

#Change the paragraph wanted here
chosen_paragraph = 4
#Change the column wanted here
chosen_col = 2

row_pixel = horizontal_projection(binarizedImage, col_pixel, chosen_col)
paragraph_snap= paragraph(row_pixel, col_pixel, chosen_col, chosen_paragraph)

cv2.imshow('test', paragraph_snap)
cv2.waitKey()
cv2.destroyAllWindows()