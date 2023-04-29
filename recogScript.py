'''
This script detects complete words by splitting the word into letters and then recognizing individual letters.
'''

import tensorflow as tf
import numpy as np
import cv2

# A dictionary to map labels to their corresponding characters.
# Label mapping is available in the dataset. File : emnist-byclass-mapping.txt
LabelDict = {
    0 : "0", 1 : "1", 2 : "2", 3 : "3", 4 : "4", 5 : "5", 6 : "6", 7 : "7", 8 : "8", 9 : "9",

    10 : "A", 11 : "B", 12 : "C", 13 : "D", 14 : "E", 15 : "F", 16 : "G", 17 : "H", 18 : "I", 19 : "J", 20 : "K", 21 : "L", 22 : "M",
    23 : "N", 24 : "O", 25 : "P", 26 : "Q", 27 : "R", 28 : "S", 29 : "T", 30 : "U", 31 : "V", 32 : "W", 33 : "X", 34 : "Y", 35 : "Z",

    36 : "a", 37 : "b", 38 : "c", 39 : "d", 40 : "e", 41 : "f", 42 : "g", 43 : "h", 44 : "i", 45 : "j", 46 : "k", 47 : "l", 48 : "m",
    49 : "n", 50 : "o", 51 : "p", 52 : "q", 53 : "r", 54 : "s", 55 : "t", 56 : "u", 57 : "v", 58 : "w", 59 : "x", 60 : "y", 61 : "z"
}

# Define model path and load it
unixTime = 1679036461
ModelPath = f"Models/{unixTime}/model.meow"

model = tf.keras.models.load_model(ModelPath)

# Alternative method to MSER
# Time comparison of various methods :
# MSER time : 0.046875s
# Alt time (opti) : 0.015625s
# alt time (unopti) : 1.859375s

def altMSER(img) :
    image = np.copy(img)

    h, w = image.shape
    img_size = h * w

    maxArea = int(img_size / 2)
    minArea = 10
    
    rects = []

    x = -1
    y = -1
    y_low = -1

    # Optimized approach
    image  = np.transpose(image)
    image = cv2.bitwise_not(image)
    h, w = image.shape

    rowCount = -1
    for rows in image :
        rowCount += 1
        if np.count_nonzero(rows) > 0 :
            t1 = np.nonzero(rows)[0][0]
            t2 = np.nonzero(rows)[0][-1]

            if y_low == -1 or t1 < y_low :
                y_low = t1

            if y == -1 or t2 > y :
                y = t2

            if x == -1 :
                x = rowCount
        else :
            if x != -1 and y != -1 :
                area = abs((rowCount - x) * (y_low - y))

                if area > minArea and area < maxArea :
                    box = (x, y, rowCount - x, y_low - y)
                    rects.append(box)

                x = -1
                y = -1
                y_low = -1

        if rowCount == h - 1 :
            if x != -1 and y != -1 :
                area = abs((rowCount - x) * (y_low - y))

                if area > minArea and area < maxArea :
                    box = (x, y, rowCount - x, y_low - y)
                    rects.append(box)

                x = -1
                y = -1
                y_low = -1

    # Unoptimized method
    # for i in range(w) :
    #     flag = True
    #     for j in range(h) :
    #         if image[j, i] == 0 :
    #             flag = False

    #             if x == -1 :
    #                 x = i
    #                 y = j
    #                 y_low = j

    #             if j < y :
    #                 y = j
                
    #             if j > y_low :
    #                 y_low = j

    #     if flag :
    #         if x != -1 and y != -1 :
    #             box = (x, y, i - x, y_low - y)
    #             x = -1
    #             y = -1
    #             y_low = -1
    #             rects.append(box)
    
    return rects

# Method to perform the recognition
def recog(img, use_MSER = True) :
    # Create an empty list to store the cropped images of the letters
    letters = []

    # Convert image to cv2 format from Pillow
    img = np.array(img)
    (h, w) = img.shape[: 2]
    image_size = h * w

    # Convert to grayscale and binarize with otsu method
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    rects = []

    if use_MSER :
        # Create an Maximally Stable External Region Extractor
        # More on https://docs.opencv.org/4.x/d3/d28/classcv_1_1MSER.html
        mser = cv2.MSER_create()
        mser.setMaxArea(int(image_size / 2))
        mser.setMinArea(10)

        # Detect letters
        regions, rects = mser.detectRegions(bw)
    else :
        rects = altMSER(bw)
    
    # Empty list to store the coordinates of each rectangle
    rects2 = []
    for (x, y, w, h) in rects :
        points = []
        points.append(x)
        points.append(y)
        points.append(x + w)
        points.append(y + h)
            
        rects2.append(points)

    rects3 = []

    if use_MSER :
        # Stores the coords but removes coords that are present within another bounding box.
        # This prevents loops in letters being detected separately    
        for line in rects2 :
                flag = False
                for line2 in rects2 :
                    if line[0] > line2[0] and line[1] > line2[1] and line[2] < line2[2] and line[3] < line2[3] :
                        flag = True
                if not flag :
                    rects3.append(line)

        # Sort the coords from left to right
        rects3.sort(key= lambda x : x[0])
    else :
        rects3 = rects2

    # Crop each letter and store them
    for (x1, y1, x2, y2) in rects3 :
        cropped = []
        if use_MSER :
            cropped = img[y1:y2, x1:x2]
        else :
            cropped = img[y2:y1, x1:x2]
        letters.append(cropped)

    # Detect spaces between multiple words
    ## Calculate and store spacing between each character in a list
    spaces = []
    for i in range(len(letters) - 1) :
        space = rects3[i + 1][0] - rects3[i][0]
        spaces.append(space)

    ## Find out the mean space
    avg_spacing = 0
    if len(spaces) > 0 :
        avg_spacing = sum(spaces) / len(spaces)

    ## If a space is greater than the mean space then it would mean a space between two words
    spaceCount = 1
    for i in range(len(spaces)) :
        if spaces[i] > avg_spacing :
            letters.insert(i + spaceCount, "SPACE")
            spaceCount += 1

    # Define a string to store the recognized letters
    word_letters = ""

    # Iterate through the cropped images
    for images in letters :

        if isinstance(images, str) :
            word_letters += " "
            continue

        # Preprocessing
        ## Strip channel info
        images = images[:, :, 0]

        ## Padding the images to become square before resizing
        h, w = images.shape

        if h > w :
            diff = int((h - w) / 2)
            images = np.pad(images, ((0, 0), (diff, diff)), 'constant', constant_values= 255)
        elif w > h :
            diff = int((w - h) / 2)
            images = np.pad(images, ((diff, diff), (0, 0)), 'constant', constant_values= 255)

        ## Reduce size to 20x20 as that's the dimension in which the letters are focused.
        images = cv2.resize(images, (20, 20), interpolation= cv2.INTER_AREA)

        # Rotate and flip image because the images in the dataset are transposed.
        images = cv2.rotate(images, cv2.ROTATE_90_COUNTERCLOCKWISE)
        images = cv2.flip(images, 0)

        # Negate images to invert the colors.
        # Make background black and text white, because that's how the dataset is.
        images = cv2.bitwise_not(images)

        # Extend the image's boundary by 4 pixels on all sides to make the dimension 28x28.
        images = np.pad(images, ((4, 4), (4, 4)), "constant", constant_values= 0)

        # Predict the output values from the image and store the array in a variable
        pred = model.predict(np.array([images]))

        # Find the label with the highest value.
        predIndex = np.argmax(pred)
        
        # Add the label value to the final output string
        word_letters += LabelDict[predIndex]

    return word_letters