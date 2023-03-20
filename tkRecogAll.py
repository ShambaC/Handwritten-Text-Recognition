'''
This script detects complete words by splitting the word into letters and then recognizing individual letters.
'''

import tensorflow as tf
import numpy as np
import cv2

from tkinter import messagebox

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

# Method to perform the recognition
def recog(img) :
    # Create an empty list to store the cropped images of the letters
    letters = []

    # Convert image to cv2 format from Pillow
    img = np.array(img)
    (h, w) = img.shape[: 2]
    image_size = h * w

    # Create an Maximally Stable External Region Extractor
    # More on https://docs.opencv.org/4.x/d3/d28/classcv_1_1MSER.html
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

    #Define a string to store the recognized letters
    word_letters = ""

    # Iterate through the cropped images
    for images in letters :

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

    # Display the results
    messagebox.showinfo(title= "Result", message= f"The word is {word_letters}")

# PAINT APP USING tkinter
from tkinter import *
import PIL.ImageGrab as ImageGrab

class Draw() :
    def __init__(self, root) :
        # Initial config values
        self.root = root
        # Window title
        self.root.title("MyPaint")
        # Window resolution
        self.root.geometry("1024x576")
        # Window background color
        self.root.configure(background = "black")
        # Do not let the window to be resizable on both axes
        self.root.resizable(0, 0)

        # Define the colors
        self.pointer = "black"
        self.erase = "white"

        # Size or width of the drawing pen
        self.pointer_size = 17.5

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
        self.rec_btn = Button(self.root, text = "Recognise", bd = 4, bg = 'white', command = self.rec_drawing, width = 9, relief = RIDGE)
        self.rec_btn.place(x = 0, y = 257)

        # Defining a background color for the Canvas
        self.background = Canvas(self.root, bg = 'white', bd = 5, relief = FLAT, height = 510, width = 850)
        self.background.place(x = 80, y = 20)
 
 
        # Bind the background Canvas with mouse click
        self.background.bind("<B1-Motion>",self.paint)

    def eraser(self) :
        self.pointer = self.erase
        self.pointer_size = 22

    def pen(self) :
        self.pointer = 'black'
        self.pointer_size = 17.5

    def paint(self, event) :
        x1, y1 = (event.x - 2), (event.y - 2)
        x2, y2 = (event.x + 2), (event.y + 2)

        self.background.create_oval(x1, y1, x2, y2, fill = self.pointer, outline = self.pointer, width = self.pointer_size)
    
    
    def rec_drawing(self):
        # Get the coordinate values of the canvas
        x = self.root.winfo_rootx() + self.background.winfo_x()
        y = self.root.winfo_rooty() + self.background.winfo_y()
 
        x1 = x + self.background.winfo_width()
        y1 = y + self.background.winfo_height()

        # Screenshot the whole display and then crop out the canvas
        img = ImageGrab.grab().crop((x + 7 , y + 7, x1 - 7, y1 - 7))

        recog(img)

root = Tk()
p = Draw(root)
root.mainloop()