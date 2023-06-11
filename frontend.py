from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import PIL.ImageGrab as ImageGrab
from recogScript import *


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
    if word == "" :
        outbox.config(text="RESULT TEXT HERE ...")
    else :
        outbox.config(text=word)

def paint(event) :
    x1, y1 = (event.x - 2), (event.y - 2)
    x2, y2 = (event.x + 2), (event.y + 2)
    sketch.create_oval(x1, y1, x2, y2, fill=pointer, outline = pointer, width = pointer_size)

def rec_drawing(event):

    # # Get the coordinate values of the canvas
    # x = root.winfo_rootx() + sketch.winfo_x()
    # y = root.winfo_rooty() + sketch.winfo_y()

    # x1 = x + sketch.winfo_width()
    # y1 = y + sketch.winfo_height()

    # # Screenshot the whole display and then crop out the canvas
    # img = ImageGrab.grab().crop((x + 7 , y + 7, x1 - 7, y1 - 7))

    # Get the coordinate values of the canvas
    x = root.winfo_rootx() + frame2.winfo_x()
    y = root.winfo_rooty() + frame2.winfo_y()

    x1 = x + frame2.winfo_width()
    y1 = y + frame2.winfo_height()

    # Screenshot the whole display and then crop out the canvas
    img = ImageGrab.grab().crop((x + 24 , y + 17, x1 - 28, y1 - 185))

    
    res = recog(img)
    output(res)



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
sketch.bind("<ButtonRelease-1>", rec_drawing)


# Output Box
outbox = Label(frame2, text="RESULT TEXT HERE ...", font=("Calibri",20,"bold"), fg='black', bg='#D8D3CD')
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