import cv2
import numpy as np

# Function to remove table spanning all columns
def remove_long_table(ncol):
    table_row = []
    horizontal_projection1 = np.sum(
        binarizedImage, axis=1)
    # If the value of horizontal projection of a row is larger than 80% of
    # the width of paper, it is identified as the table border
    for row in range (horizontal_projection1.shape[0]):
        if horizontal_projection1[row] > 0.8 * ncol:
            table_row.append(row)
    # Set the region between borders of the table to be white colour,
    # removing the table from the paper
    if len(table_row) > 0:
        binarizedImage[table_row[0] : table_row[-1] + 1] = 0

# Function to extract paragraph starting and ending pixel values vertically
def vertical_extraction(binarizedImage):
    vertical_projection = np.sum(binarizedImage, axis=0)
    state = False
    first_pixel = []
    
    for column in range (vertical_projection.shape[0]):
        # When state changes from false to true, it indicates the starting point 
        # of the paragraph, so add the pixel into the list
        if state == False:
            if vertical_projection[column] >= 1:
                state = True
                first_pixel.append(column)   
        # When state changes from true to false, it indicates the ending point  
        # of the paragraph, so add the pixel into the list         
        if state == True:
            if vertical_projection[column] == 0:
                state = False
                first_pixel.append(column)
    return first_pixel             
    
# Function to extract paragraph starting and ending pixel values horizontally
def horizontal_extraction(binarizedImage, interchange_pixel, col):
    state = False
    first_pixel = []
    row_pixel = []
        
    # Select region based on the col parameter, selected region = (2col-2, 2col-1) 
    horizontal_projection_col = np.sum(binarizedImage[:, 
                                interchange_pixel[col * 2 - 2]: 
                                interchange_pixel[col * 2 - 1]], axis=1)
   
    for column in range(horizontal_projection_col.shape[0]):
        # When state changes from false to true, it is the starting point of 
        # the paragraph/sentence, so add the pixel into the list
        if state == False:
            if horizontal_projection_col[column] >= 1:
                state = True
                first_pixel.append(column)
        # When state changes from true to false, it is the ending point of the 
        # paragraph/sentence, so add the pixel into the list           
        if state == True:
            if horizontal_projection_col[column] == 0:
                state = False
                first_pixel.append(column)
   
    # Append the starting point of the paragraph into the row_pixel
    row_pixel.append(first_pixel[0])
    
    difference = []
    
    # Calculate the differences between pixel value to differentiate between 
    # paragraphs and sentences. Gaps between paragraphs should be much larger 
    # than gaps between sentences
    for pixel_index in range(len(first_pixel) - 1):
        difference.append(first_pixel[pixel_index + 1] - first_pixel[pixel_index])
        
    for difference_index in range(len(difference)):
        # If difference is larger than the sentence gap threshold, it is considered as
        # starting and ending point of paragraph, append the value into row_pixel
        sentence_gap_size = 30
        gap_between_paragraph = 100
        if difference[difference_index] > sentence_gap_size * 1.5 and \
        difference[difference_index] < gap_between_paragraph:
            row_pixel.append(first_pixel[difference_index])
            row_pixel.append(first_pixel[difference_index + 1])

    # append the ending point of the paragraph into the row_pixel
    row_pixel.append(first_pixel[-1] + 1)
    
    return row_pixel

# Function to get the interchange pixel between white gap 
# and content (used to determine if its an image)
def horizontal_extraction_image(binarizedImage, col):
    state = False
    first_pixel = []

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

# Function to snapshot the paragraph based on the result from vertical and horizontal extraction
def paragraph(row_pixel, col_pixel, col, n):
    # shift 10 to leave some borders
    paragraph_snap = img[row_pixel[n * 2 - 2]-10 : row_pixel[n * 2 - 1]+10, 
                         col_pixel[col*2-2]-10 : col_pixel[col*2-1]+10 ]
    # Check if the paragraph is an image, if yes, do not return the paragraph
    if not detected_images(paragraph_snap, n):
        return paragraph_snap
    else:
        return "Image detected"

# Function to detect if a paragraph is an image 
def detected_images(paragraph_snap, current_paragraph):
    img = paragraph_snap
    GaussianFilter= cv2.GaussianBlur(img, (7,7), 0, cv2.BORDER_DEFAULT)
    _, img= cv2.threshold(GaussianFilter, 200, 255, cv2.THRESH_BINARY)
    img[img == 0] = 1
    img[img == 255] = 0
    
    # Get the horizontal paragraph starting and ending pixel values
    row_pixel_paragraph = horizontal_extraction_image(img, 1)
    
    # Check if there is only one row in the paragraph
    # If the number of values recorded is equals or lesser than 2, means there
    # are no gaps within the paragraph, means it is an image or table
    if len(row_pixel_paragraph) <= 2: 
        return True 
    else:
        return False
    
## Main Code ##

# Choose your image 
img_name = "008"
img_type = ".png"
img = cv2.imread(img_name+img_type, 1)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
[nrow, ncol] = img.shape

# Apply filter to reduce noise
GaussianFilter= cv2.GaussianBlur(img, (7,7), 0, cv2.BORDER_DEFAULT)
hist = cv2.calcHist([GaussianFilter], [0], None, [256], [0,256])
# Binarized the image
_, binarizedImage = cv2.threshold(GaussianFilter, 200, 255, cv2.THRESH_BINARY)

# White is 0, black is 1 
binarizedImage[binarizedImage == 0] = 1
binarizedImage[binarizedImage == 255] = 0

# Remove table spanning all columns
remove_long_table(ncol)

# Get vertical starting and ending points of paragraph
col_pixel = vertical_extraction(binarizedImage)

page_count = 1
num_of_col = len(col_pixel)//2

# Loop through every column in the paper
for cols in range(1, num_of_col+1):
    # Get horizontal starting and ending points of paragraph
    row_pixel = horizontal_extraction(binarizedImage, col_pixel, cols)
    num_of_row = len(row_pixel)//2
    for rows in range(1, num_of_row+1):
        # Snapshot the paragraph
        paragraph_snap = paragraph(row_pixel, col_pixel, cols, rows)     
        # If the paragraph is not identified as an image, output the image
        if not np.array_equal(paragraph_snap, "Image detected"):
            filename = img_name + "_paragraph_"+ str(page_count)+".png"
            cv2.imwrite(filename, paragraph_snap)
            page_count+=1