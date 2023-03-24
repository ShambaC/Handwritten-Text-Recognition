'''
This script is used to recognize individual elements.
Letters and digits.
'''

import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt

from tkinter import messagebox

LabelDict = {
    0 : "0", 1 : "1", 2 : "2", 3 : "3", 4 : "4", 5 : "5", 6 : "6", 7 : "7", 8 : "8", 9 : "9",

    10 : "A", 11 : "B", 12 : "C", 13 : "D", 14 : "E", 15 : "F", 16 : "G", 17 : "H", 18 : "I", 19 : "J", 20 : "K", 21 : "L", 22 : "M",
    23 : "N", 24 : "O", 25 : "P", 26 : "Q", 27 : "R", 28 : "S", 29 : "T", 30 : "U", 31 : "V", 32 : "W", 33 : "X", 34 : "Y", 35 : "Z",

    36 : "a", 37 : "b", 38 : "c", 39 : "d", 40 : "e", 41 : "f", 42 : "g", 43 : "h", 44 : "i", 45 : "j", 46 : "k", 47 : "l", 48 : "m",
    49 : "n", 50 : "o", 51 : "p", 52 : "q", 53 : "r", 54 : "s", 55 : "t", 56 : "u", 57 : "v", 58 : "w", 59 : "x", 60 : "y", 61 : "z"
}

unixTime = 1679036461
ModelPath = f"Models/{unixTime}/model.meow"

model = tf.keras.models.load_model(ModelPath)

def recog(img) :
    try :
        img = np.array(img)
        img = cv2.resize(img, (20, 20), interpolation= cv2.INTER_AREA)
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        img = cv2.flip(img, 0)
        img = img[:, :, 0]
        img = np.pad(img, ((4, 4), (4, 4)), "constant", constant_values= 0)
        pred = model.predict(np.array([img]))
        predIndex = np.argmax(pred)
        messagebox.showinfo(title= "Result", message= f"The letter is {LabelDict[predIndex]}, index : {predIndex}")
        plt.imshow(img, cmap= plt.cm.binary)
        plt.title("Processed Image")
        plt.show()
    except :
        print("ERROR")

from tkinter import *
import PIL.ImageGrab as ImageGrab

class Draw() :
    def __init__(self, root) :
        self.root = root
        self.root.title("MyPaint")
        self.root.geometry("512x512")
        self.root.configure(background = "white")
        self.root.resizable(0, 0)

        self.pointer = "white"

        # Reset Button to clear the entire screen
        self.clear_screen = Button(self.root, text = "Clear Screen", bd = 4, bg = 'white', command = lambda : self.background.delete('all'), width = 9, relief = RIDGE)
        self.clear_screen.place(x = 0, y = 227)
 
        # Button to recognise the drawn number
        self.rec_btn = Button(self.root, text = "Recognise", bd = 4, bg = 'white', command = self.rec_drawing, width = 9, relief = RIDGE)
        self.rec_btn.place(x = 0, y = 257)

        #Defining a background color for the Canvas
        self.background = Canvas(self.root, bg = 'black', bd = 5, relief = FLAT, height = 400, width = 400)
        self.background.place(x = 80, y = 40)
 
 
        #Bind the background Canvas with mouse click
        self.background.bind("<B1-Motion>",self.paint)

    def paint(self, event) :
        x1, y1 = (event.x - 2), (event.y - 2)
        x2, y2 = (event.x + 2), (event.y + 2)

        self.background.create_oval(x1, y1, x2, y2, fill = self.pointer, outline = self.pointer, width = 24.5)
    
    
    def rec_drawing(self):
        try:
            # self.background update()
            x = self.root.winfo_rootx() + self.background.winfo_x()
            y = self.root.winfo_rooty() + self.background.winfo_y()
 
            x1 = x + self.background.winfo_width()
            y1 = y + self.background.winfo_height()
            img = ImageGrab.grab().crop((x + 7 , y + 7, x1 - 7, y1 - 7))

            recog(img)
        except:
            print("Error in screenshot execution") 

root = Tk()
p = Draw(root)
root.mainloop()