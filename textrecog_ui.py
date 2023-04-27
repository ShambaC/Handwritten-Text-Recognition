# Frontend UI

from recogScript import *

from tkinter import *
import PIL.ImageGrab as ImageGrab
# from PIL import Image, ImageTk   #for jpeg or jpg image

class Draw() :
    def __init__(self, root) :
        # Initial config values
        self.root = root
        # Window title
        self.root.title("Handwritten Text Recognition")
        # Window resolution
        self.root.geometry("1500x700")
        # Window background color
        self.root.configure(background = "#242424")
        # Do not let the window to be resizable on both axes
        self.root.resizable(0, 0)

        # Define the colors
        self.pointer = "black"
        self.erase = "white"

        # Size or width of the drawing pen
        self.pointer_size = 17.5

        # Pen Button(it's modified)
        # bg1=Image.open("bg_example.jpg")  #image and text not working together rn
        # pen_bg1=ImageTk.PhotoImage(bg1)   #this is for jpg image
        # pen_bg1=PhotoImage("filename")  check this for png

        # Pen Button
        self.pen_btn = Button(self.root, text = "Pen", bd = 4, fg='black', font=("Arial",16,"bold"), bg= "#23c47d", command = self.pen, width = 14, relief = RAISED)
        self.pen_btn.place(x = 180, y = 10)

        # Eraser button
        self.eraser_btn = Button(self.root, text = "Eraser", bd = 4, fg='black', font=("Arial",16,"bold"), bg= "#23c47d", command = self.eraser, width = 14, relief = RAISED)
        self.eraser_btn.place(x = 600, y = 10)

        # Reset Button to clear the entire screen
        self.clear_screen = Button(self.root, text = "Clear Screen", bd = 4, fg='black', font=("Arial",16,"bold"), bg= "#23c47d", width = 14, relief = RAISED, command = self.clearScreen)
        self.clear_screen.place(x = 1050, y = 10)
 
        # # Button to recognise the drawn number
        # self.rec_btn = Button(self.root, text = "Recognise", bd = 4, bg = 'white', command = self.rec_drawing, width = 9, relief = RIDGE)
        # self.rec_btn.place(x = 0, y = 257)

        # Defining a background color for the Canvas
        self.background = Canvas(self.root, bg = 'white', bd = 5, relief = FLAT, height = 510, width = 1390)
        self.background.place(x = 45, y = 60)

        #output box
        self.outbox = Label(self.root, text="RESULT TEXT HERE ...", font=("Calibri",20,"bold"), fg='black', bg="#23c47d", width=16)
        self.outbox.place(x = 742, y = 640)

        # Bind the background Canvas with mouse click
        self.background.bind("<B1-Motion>", self.paint)
        #bind the rec_drawing method with mouse click release
        self.background.bind("<ButtonRelease-1>", self.rec_drawing)

    def eraser(self) :
        self.pointer = self.erase
        self.pointer_size = 22

    def pen(self) :
        self.pointer = 'black'
        self.pointer_size = 17.5

    def clearScreen(self) :
        self.background.delete('all')
        self.output("RESULT TEXT HERE ...")

    def paint(self, event) :
        x1, y1 = (event.x - 2), (event.y - 2)
        x2, y2 = (event.x + 2), (event.y + 2)

        self.background.create_oval(x1, y1, x2, y2, fill = self.pointer, outline = self.pointer, width = self.pointer_size)

    # Update out[ut Box]
    def output(self, word) :
        self.outbox.config(text=word)

    def rec_drawing(self, event):
        # Get the coordinate values of the canvas
        x = self.root.winfo_rootx() + self.background.winfo_x()
        y = self.root.winfo_rooty() + self.background.winfo_y()
 
        x1 = x + self.background.winfo_width()
        y1 = y + self.background.winfo_height()

        # Screenshot the whole display and then crop out the canvas
        img = ImageGrab.grab().crop((x + 7 , y + 7, x1 - 7, y1 - 7))

        res = recog(img)
        self.output(res)

root = Tk()
p = Draw(root)
root.mainloop()