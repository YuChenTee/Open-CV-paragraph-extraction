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


def vertical_projection():
    vertical_projection = np.sum(binarizedImage, axis=0);
    state = False
    count = 0
    first_pixel = []
    for column in range (vertical_projection.shape[0]):
        if state == False:
            if vertical_projection[column] >= 1:
                state = True
                count = count + 1 
                first_pixel.append(column)   
                
        if state == True:
            if vertical_projection[column] == 0:
                state = False
                first_pixel.append(column)
    return first_pixel             
    

def horizontal_projection_1col(interchange_pixel):
    horizontal_projection = np.sum(
        binarizedImage[ : ,interchange_pixel[0] : interchange_pixel[1]], axis=1);   
    state = False
    count = 0
    first_pixel = []
    row_pixel = []
    row_pixel_index = []
    
    for column in range (horizontal_projection.shape[0]):
        if state == False:
            if horizontal_projection[column] >= 1:
                state = True
                count = count + 1 
                first_pixel.append(column)
                
        if state == True:
            if horizontal_projection[column] == 0:
                state = False
                first_pixel.append(column)
                
    #append the starting point into the row pixel
    row_pixel.append(first_pixel[0])
    difference = []
    for x in range(len(first_pixel) - 1):
        difference.append(first_pixel[x + 1] - first_pixel[x] )
    for y in range(len(difference)):
        if difference[y] > 30 * 1.5:
            row_pixel_index.append(y)
            row_pixel_index.append(y + 1)
    for z in range(len(row_pixel_index)):
        row_pixel.append(first_pixel[row_pixel_index[z]])
    #append the ending point into the row pixel
    row_pixel.append(first_pixel[-1] + 1)
    return row_pixel

def horizontal_projection_2col(interchange_pixel, col):
    horizontal_projection_col1 = np.sum(
        binarizedImage[ : ,interchange_pixel[0] : interchange_pixel[1]], axis=1);
    horizontal_projection_col2 = np.sum(
        binarizedImage[ : ,interchange_pixel[2] : interchange_pixel[3]], axis=1); 
    state = False
    count = 0
    first_pixel = []
    row_pixel = []
    row_pixel_index = []
    
    if col == 1:
        for column in range (horizontal_projection_col1.shape[0]):
            if state == False:
                if horizontal_projection_col1[column] >= 1:
                    state = True
                    count = count + 1 
                    first_pixel.append(column)
                    
            if state == True:
                if horizontal_projection_col1[column] == 0:
                    state = False
                    first_pixel.append(column)
                    
        #append the starting point into the row pixel
        row_pixel.append(first_pixel[0])
        difference = []
        for x in range(len(first_pixel) - 1):
            difference.append(first_pixel[x + 1] - first_pixel[x] )
        for y in range(len(difference)):
            if difference[y] > 30 * 1.5:
                row_pixel_index.append(y)
                row_pixel_index.append(y + 1)
        for z in range(len(row_pixel_index)):
            row_pixel.append(first_pixel[row_pixel_index[z]])
        #append the ending point into the row pixel
        row_pixel.append(first_pixel[-1] + 1)
 
    if col == 2:
        for column in range (horizontal_projection_col2.shape[0]):
            if state == False:
                if horizontal_projection_col2[column] >= 1:
                    state = True
                    count = count + 1 
                    first_pixel.append(column)
                    
            if state == True:
                if horizontal_projection_col2[column] == 0:
                    state = False
                    first_pixel.append(column)
                    
        #append the starting point into the row pixel
        row_pixel.append(first_pixel[0])
        difference = []
        for x in range(len(first_pixel) - 1):
            difference.append(first_pixel[x + 1] - first_pixel[x] )
        for y in range(len(difference)):
            if difference[y] > 30 * 1.5:
                row_pixel_index.append(y)
                row_pixel_index.append(y + 1)
        for z in range(len(row_pixel_index)):
            row_pixel.append(first_pixel[row_pixel_index[z]])
        #append the ending point into the row pixel
        row_pixel.append(first_pixel[-1] + 1)
    return row_pixel


def paragraph_1(row_pixel,n):
        return first_img[row_pixel[n] * 2 - 2 : row_pixel[n] * 2 - 1]
    
def paragraph(row_pixel,col_pixel,col, n):
        if col == 1:
            return first_img[row_pixel[n] * 2 - 2 : row_pixel[n] * 2 - 1, 
                             col_pixel[0] : col_pixel[2] ]
        if col == 2:
            return first_img[row_pixel[n] * 2 - 2 : row_pixel[n] * 2 - 1, 
                             col_pixel[2] : col_pixel[4] ]




## Main Code ##

# Read the first image 
first_img = cv2.imread('001.png', 0)
sample_img = cv2.imread('paragraph 1 sample.png', 0)
[nrow, ncol] = first_img.shape


GaussianFilter= cv2.GaussianBlur(first_img, (7,7), 0, cv2.BORDER_DEFAULT)

hist = cv2.calcHist([GaussianFilter], [0], None, [256], [0,256])

_, binarizedImage = cv2.threshold(GaussianFilter, 200, 255, cv2.THRESH_BINARY)

#white is 0, black is 1 
binarizedImage[binarizedImage == 0] = 1
binarizedImage[binarizedImage == 255] = 0

remove_table_1col(ncol)
col_pixel = vertical_projection()
if len(col_pixel) == 2:
    row_pixel = horizontal_projection_1col(col_pixel)
    paragraph_snap = paragraph_1(row_pixel,1)
elif len(col_pixel) == 4:
    #Change the column wanted here
    row_pixel = horizontal_projection_2col(col_pixel, 1)
    paragraph_snap = paragraph(row_pixel, col_pixel,1, 2)


cv2.imshow('test', paragraph_snap)
cv2.waitKey()
cv2.destroyAllWindows()