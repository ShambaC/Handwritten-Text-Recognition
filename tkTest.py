'''
This script is used to check individual letter detection in an image with multiple letters.
It detects letters, creates bounding boxes around them.
Sorts the letters from left to right and then displays them.
'''

import numpy as np
import cv2

def detect(img) :
    
    # Create an empty list to store the cropped images of the letters
    letters = []

    img = np.array(img)
    (h, w) = img.shape[: 2]
    image_size = h * w
    mser = cv2.MSER_create()
    mser.setMaxArea(int(image_size / 2))
    mser.setMinArea(10)

    # Convert to grayscale and binarize with otsu method
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Detect letters
    regions, rects = mser.detectRegions(bw)

    # Empty list to store the coordinates of each rectangle
    rects2 = []
    for (x, y, w, h) in rects :
        points = []
        points.append(x)
        points.append(y)
        points.append(x + w)
        points.append(y + h)
        
        rects2.append(points)

    # Stores the coords but removes coords that are present within another bounding box.
    # This prevents loops in letters being detected separately
    rects3 = []
    for line in rects2 :
            flag = False
            for line2 in rects2 :
                if line[0] > line2[0] and line[1] > line2[1] and line[2] < line2[2] and line[3] < line2[3] :
                    flag = True
            if not flag :
                rects3.append(line)

    # Sort the coords from left to right
    rects3.sort(key= lambda x : x[0])

    # Crop each letter and store them
    for (x1, y1, x2, y2) in rects3 :
        cropped = img[y1:y2, x1:x2]
        letters.append(cropped)

    # Display each letter
    for images in letters :
        cv2.imshow('window', images)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
    

# PAINT Logic
from tkinter import *
import PIL.ImageGrab as ImageGrab

class Draw() :
    def __init__(self, root) :
        self.root = root
        self.root.title("MyPaint")
        self.root.geometry("1024x576")
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
        self.background = Canvas(self.root, bg = 'white', bd = 5, relief = FLAT, height = 510, width = 850)
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

        detect(img)
        

root = Tk()
p = Draw(root)
root.mainloop()