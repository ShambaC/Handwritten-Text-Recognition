import numpy as np
import cv2

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

            if y == -1 or t1 < y :
                y = t1

            if y_low == -1 or t2 > y_low :
                y_low = t2

            if x == -1 :
                x = rowCount

        elif nonZeroCount <= 0 :
            if x != -1 and y != -1 :
                area = (rowCount - x) * (y_low - y)

                if area > minArea and area < maxArea :
                    box = (x, y, rowCount - x, y_low - y)
                    rects.append(box)
                    print(box)

                x = -1
                y = -1
                y_low = -1
                
        if rowCount == h - 1 :
            if x != -1 and y != -1 :
                area = (rowCount - x) * (y_low - y)

                if area > minArea and area < maxArea :
                    box = (x, y, rowCount - x, y_low - y)
                    rects.append(box)

                x = -1
                y = -1
                y_low = -1
    
    return rects

def detect(imgIn) :
    
    # Create an empty list to store the cropped images of the letters
    letters = []
    
    img = np.copy(imgIn)
    img = np.array(img)

    # Convert to grayscale and binarize with otsu method
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    rects = []
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

    # Crop each letter and store them
    for (x1, y1, x2, y2) in rects2 :
        cropped = []
        cropped = img[y1:y2, x1:x2]
        letters.append(cropped)
        cv2.rectangle(img, (x1, y1), (x2, y2), color= (255, 0, 255), thickness= 1)

    # Detect spaces between multiple words
    ## Calculate and store spacing between each character in a list
    spaces = []
    for i in range(len(letters) - 1) :
        space = rects2[i + 1][0] - rects2[i][0]
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

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import PIL.ImageGrab as ImageGrab
# from recogScript import *

import time

pointer="black"
erase="white"
pointer_size=17.5

def pen(event):
    root.configure(cursor="pencil")
    global pointer
    pointer="black"
    pointer_size=17.5

def eraser(event):
    root.configure(cursor="circle")
    global pointer
    pointer="white"
    pointer_size=22

def clearScreen(event):
    sketch.delete('all')
    outbox.config(text="RESULT TEXT HERE ...")

def output(word):
    print("outbox edit called")
    if word == "" :
        outbox.config(text="RESULT TEXT HERE ...")
    else :
        outbox.config(text=word)

def paint(event) :
    x1, y1 = (event.x - 2), (event.y - 2)
    x2, y2 = (event.x + 2), (event.y + 2)
    sketch.create_oval(x1, y1, x2, y2, fill=pointer, outline = pointer, width = pointer_size)

def rec_drawing(event):
    # print("Rec drawing event fired")

    # Get the coordinate values of the canvas
    # print(root.winfo_rootx(), root.winfo_rooty(), sketch.winfo_x(), sketch.winfo_y())
    # x = root.winfo_rootx() + sketch.winfo_x()
    # y = root.winfo_rooty() + sketch.winfo_y()

    # print(sketch.winfo_width(), sketch.winfo_height())
    # x1 = x + sketch.winfo_width()
    # y1 = y + sketch.winfo_height()

    print(root.winfo_rootx(), root.winfo_rooty(), frame2.winfo_x(), frame2.winfo_y())
    x = root.winfo_rootx() + frame2.winfo_x()
    y = root.winfo_rooty() + frame2.winfo_y()

    print(frame2.winfo_width(), frame2.winfo_height())
    x1 = x + frame2.winfo_width()
    y1 = y + frame2.winfo_height()

    # Screenshot the whole display and then crop out the canvas
    img = ImageGrab.grab(all_screens= True).crop((x + 24 , y + 17, x1 - 28, y1 - 198))

    detect(img)

    # print("recog method called")
    # start = time.perf_counter()
    # res = recog(img)
    # print(time.perf_counter() - start)
    # output(res)



# defining the window
root = Tk()
root.title("Handwritten Text Recognition")
rooticon=PhotoImage(file= ".\icons\icons8-home-screen-100.png")
root.iconphoto(False, rooticon)
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)
# root.minsize(800,500)
root.configure(background="#D2DAFF" )
# root['background']='#D2DAFF'
# root.attributes("-fullscreen", True)
# defining a style
# s = ttk.Style()
# s.configure('TButton', borderwidth=0, padding=6)

Grid.rowconfigure(root,0,weight=1)
Grid.columnconfigure(root,0,weight=1)
# defining the main frame to contain all contents
mainframe=Frame(root, background='#D2DAFF')
mainframe.grid(column=0, row=0, sticky=(N,E,W,S))

# Frame to contain buttons
frame1= Frame(mainframe, background='#D2DAFF')
frame1.grid(column=0, row=0,sticky=(N,E,W,S))


# opening and resizing images of buttons
pen_img=Image.open(".\Buttons\pen-light-final.png")
pen_img_resized=pen_img.resize((271,53))
pen_img1=ImageTk.PhotoImage(pen_img_resized)

eraser_img=Image.open(".\Buttons\eraser-light-final.png")
eraser_img_resized=eraser_img.resize((271,53))
eraser_img1=ImageTk.PhotoImage(eraser_img_resized)

clear_img=Image.open(".\Buttons\clear-light-final.png")
clear_img_resized=clear_img.resize((271,53))
clear_img1=ImageTk.PhotoImage(clear_img_resized)

# creating buttons
pen_button = Button(frame1, image=pen_img1, borderwidth=0, cursor="arrow", background='#D2DAFF')
pen_button.bind("<Button-1>", pen)
eraser_button = Button(frame1, image=eraser_img1, borderwidth=0, cursor="arrow",  background='#D2DAFF')
eraser_button.bind("<Button-1>", eraser)
clear_button = Button(frame1, image=clear_img1, borderwidth=0, cursor="arrow",  background='#D2DAFF')
clear_button.bind("<Button-1>", clearScreen)

# placing buttons on grid
pen_button.grid(row=0, column=0, padx=120, pady=30)
eraser_button.grid(row=0, column=1, padx=120, pady=30)
clear_button.grid(row=0, column=2, padx=120, pady=30)

# Frame to contain the Canvas and Result text Box
frame2= Frame(mainframe, background='#D2DAFF')
frame2.grid(row=1, column=0,rowspan=2, sticky=(S))

# placing image under canvas 
whiteboard=Image.open(".\Buttons\whiteboard.png")
whiteboard_resized=whiteboard.resize((1400,500))
whiteboard=ImageTk.PhotoImage(whiteboard_resized)

#label to display the image
label = Label(frame2, image = whiteboard)
label.grid(row=1, column=0)



# Canvas example
# class Sketchpad(Canvas):
#     def __init__(self, parent, **kwargs):
#         super().__init__(parent, **kwargs)
#         self.bind("<ButtonRelease-1>", self.save_posn)
#         self.bind("<B1-Motion>", self.draw)
        
#     def save_posn(self, event):
#         self.lastx, self.lasty = event.x, event.y

#     def draw(self, event):
#         x1, y1 = (event.x - 2), (event.y - 2)
#         x2, y2 = (event.x + 2), (event.y + 2)
#         self.create_oval(x1, y1, x2, y2, fill = self.pointer, outline = self.pointer, width = self.pointer_size)
#         self.save_posn(event)


sketch = Canvas(frame2)
sketch.grid(column=0, row=1,columnspan=3)
sketch.configure(background='White', height=465, width=1353, relief="raised")
sketch.bind("<B1-Motion>", paint)
sketch.bind("<Button-2>", rec_drawing)


# Output Box
outbox = Label(frame2, text="RESULT TEXT HERE ...", font=("Kristen ITC",20,"bold"), fg='black', bg='#99E6EC', borderwidth= 5, relief= 'solid')
outbox.grid(row=2, column=0, sticky=(E,W), pady=30)
outbox.configure(height=3, width=16)

# pen_button.grid(row=0, column=3, columnspan=2 , padx=115, pady=30)
# eraser_button.grid(row=0, column=7,columnspan=2, padx=115, pady=30)
# clear_button.grid(row=0, column=11, columnspan=2, padx=115, pady=30)

# def pen() :
#     pointer = 'black'
#     pointer_size = 17.5



# mainframe = ttk.Frame(root, padding="3 3 12 12")
# mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)

col_no=0
weight_val=1
button_list=[pen_button, eraser_button, clear_button]
for buttons in button_list:
    Misc.grid_columnconfigure(mainframe,col_no,weight=weight_val)
    col_no+=1


root.mainloop()