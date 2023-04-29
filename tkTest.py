'''
This script is used to check individual letter detection in an image with multiple letters.
It detects letters, creates bounding boxes around them.
Sorts the letters from left to right and then displays them.
'''

import numpy as np
import cv2

def manualMSER(img) :
    image = np.copy(img)

    h, w = image.shape
    img_size = h * w

    maxArea = int(img_size / 2)
    minArea = 10
    
    rects = []

    x = -1
    y = -1
    y_low = -1


    # Optimized method
    image  = np.transpose(image)
    image = cv2.bitwise_not(image)
    h, w = image.shape

    rowCount = -1
    for rows in image :
        rowCount += 1
        nonZeroCount = np.count_nonzero(rows)
        if nonZeroCount > 0 :
            t1 = np.nonzero(rows)[0][0]
            t2 = np.nonzero(rows)[0][-1]

            if y_low == -1 or t1 < y_low :
                y_low = t1

            if y == -1 or t2 > y :
                y = t2

            if x == -1 :
                x = rowCount

        elif nonZeroCount <= 0 :
            if x != -1 and y != -1 :
                box = (x, y, rowCount - x, y_low - y)
                x = -1
                y = -1
                y_low = -1
                rects.append(box)

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


def detect(imgIn, use_MSER = True) :
    
    # Create an empty list to store the cropped images of the letters
    letters = []
    
    img = np.copy(imgIn)
    img = np.array(img)
    (h, w) = img.shape[: 2]
    image_size = h * w

    # Convert to grayscale and binarize with otsu method
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    rects = []

    import time

    if use_MSER :
        # Init MSER
        mser = cv2.MSER_create()
        mser.setMaxArea(int(image_size / 2))
        mser.setMinArea(10)

        # Detect letters
        start = time.process_time()
        regions, rects = mser.detectRegions(bw)
        print(f"MSER time : {time.process_time() - start}")
    else :
        start = time.process_time()
        rects = manualMSER(bw)
        print(f"alt time (opti) : {time.process_time() - start}")        

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
        cv2.rectangle(img, (x1, y1), (x2, y2), color= (255, 0, 255), thickness= 1)

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

    index = -1
    # Display each letter
    for images in letters :
        index += 1

        if isinstance(images, str) :
            print("space ", index)
            continue
        
        images = images[:, :, 0]
        h, w = images.shape

        if h > w :
            diff = int((h - w) / 2)
            images = np.pad(images, ((0, 0), (diff, diff)), 'constant', constant_values= 255)
        elif w > h :
            diff = int((w - h) / 2)
            images = np.pad(images, ((diff, diff), (0, 0)), 'constant', constant_values= 255)

        cv2.imshow('window', images)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
    
    cv2.imshow('window', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

# PAINT Logic
from tkinter import *
import PIL.ImageGrab as ImageGrab

class Draw() :
    def __init__(self, root) :
        self.root = root
        self.root.title("MyPaint")
        self.root.geometry("1500x576")
        self.root.configure(background = "black")
        self.root.resizable(0, 0)

        self.pointer = "black"
        self.erase = "white"

        # Pen Button
        self.pen_btn = Button(self.root, text = "Pen", bd = 4, bg = 'white', command = self.pen, width = 9, relief = RIDGE)
        self.pen_btn.place(x = 0, y = 167)

        # Eraser button
        self.eraser_btn = Button(self.root, text = "Eraser", bd = 4, bg = 'white', command = self.eraser, width = 9, relief = RIDGE)
        self.eraser_btn.place(x = 0, y = 197)

        # Reset Button to clear the entire screen
        self.clear_screen = Button(self.root, text = "Clear Screen", bd = 4, bg = 'white', command = lambda : self.background.delete('all'), width = 9, relief = RIDGE)
        self.clear_screen.place(x = 0, y = 227)
 
        # Button to recognise the drawn number
        self.det_btn = Button(self.root, text = "Detect", bd = 4, bg = 'white', command = self.det_drawing, width = 9, relief = RIDGE)
        self.det_btn.place(x = 0, y = 257)

        # Defining a background color for the Canvas
        self.background = Canvas(self.root, bg = 'white', bd = 5, relief = FLAT, height = 510, width = 1370)
        self.background.place(x = 80, y = 20)
 
 
        #Bind the background Canvas with mouse click
        self.background.bind("<B1-Motion>",self.paint)

    def eraser(self) :
        self.pointer = self.erase

    def pen(self) :
        self.pointer = 'black'

    def paint(self, event) :
        x1, y1 = (event.x - 2), (event.y - 2)
        x2, y2 = (event.x + 2), (event.y + 2)

        self.background.create_oval(x1, y1, x2, y2, fill = self.pointer, outline = self.pointer, width = 17.5)
    
    
    def det_drawing(self):
        
        # self.background update()
        x = self.root.winfo_rootx() + self.background.winfo_x()
        y = self.root.winfo_rooty() + self.background.winfo_y()
 
        x1 = x + self.background.winfo_width()
        y1 = y + self.background.winfo_height()
        img = ImageGrab.grab().crop((x + 7 , y + 7, x1 - 7, y1 - 7))

        detect(img, False)
        

root = Tk()
p = Draw(root)
root.mainloop()