from tkinter import *
from PIL import ImageTk,Image
import matplotlib
#from mrc import *
import numpy as np
sys.path.append('/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages')
import mrcfile
import io, os, sys, types
from IPython import get_ipython
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell
import shutil
import tempfile
import warnings
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2TkAgg)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from six.moves import tkinter as Tk
from tkinter.font import Font

class LoadImage:
    def __init__(self,s,height,width, row, column, span):
        self.canvas = Canvas(DisplayFrame,width=width,height=height)
        File = s
        self.orig_img = Image.open(File).resize((width, height), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.orig_img)
        self.canvas.create_image(0,0, image=self.img, anchor="nw")
        self.canvas.grid(row=row, column=column, rowspan=span, columnspan=span, sticky = W)
        if s != "place.jpg": 
            self.canvas.bind("<Button-1>", lambda event, arg=self.orig_img.load(): callback(event, arg))

        self.zoomcycle = 0
        self.zimg_id = None

        self.canvas.bind("<MouseWheel>",self.zoomer)
        self.canvas.bind("<Motion>",self.crop)

    def zoomer(self,event):
        if (event.delta > 0):
            if self.zoomcycle != 4: self.zoomcycle += 1
        elif (event.delta < 0):
            if self.zoomcycle != 0: self.zoomcycle -= 1
        self.crop(event)

    def crop(self,event):
        if self.zimg_id: self.canvas.delete(self.zimg_id)
        if (self.zoomcycle) != 0:
            x,y = event.x, event.y
            if self.zoomcycle == 1:
                tmp = self.orig_img.crop((x-45,y-30,x+45,y+30))
            elif self.zoomcycle == 2:
                tmp = self.orig_img.crop((x-30,y-20,x+30,y+20))
            elif self.zoomcycle == 3:
                tmp = self.orig_img.crop((x-15,y-10,x+15,y+10))
            elif self.zoomcycle == 4:
                tmp = self.orig_img.crop((x-6,y-4,x+6,y+4))
            size = 300,200
            self.zimg = ImageTk.PhotoImage(tmp.resize(size))
            self.zimg_id = self.canvas.create_image(event.x,event.y,image=self.zimg)

def display(s):
    OutputBox.delete('1.0',END)
    OutputBox.insert(END, s)
    
def showgraph():
    a= tkvar.get()
    r = 0
    if a == "X vs Y":
        r = 2
    elif a == "Y vs Z":
        r = 3
    else:
        r = 4
    fig = Figure(figsize=(4.1, 2.1), dpi=100)
    t = np.arange(0, 3, .01)
    ax = fig.add_subplot(111).plot(t, 2 * np.sin(r * np.pi * t))

    canvas = FigureCanvasTkAgg(fig, master=DisplayFrame)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().grid(row=2,column=0, columnspan=2)
    
def load_mrc(s):
    with mrcfile.open(s, mode='r+', permissive=True) as mrc:
            mrc.header.map = mrcfile.constants.MAP_ID
            return (mrc.data)
    
def clicked(s):
    #for mrc files, final version
    if s.endswith('.mrcs'):
        #if os.path.isfile('current5.tif'):
        #    os.remove('current5.tif')
        #mrcs = []
        #final = [] #make size equal to mrc size, fill with zeros
        #get list of mrcs, plug into mrcs
        #for mrc in mrcs:
        #    a = load_mrc(s)
        #    final += a
        #img = Image.new('F', (250, 250))
        #img.putdata(final)
        #img.save('current5.tif')
        pass
    elif s.endswith('.mrc'):
        c = load_mrc(s)
        b = (255*(c-c.min())/(c.max()-c.min()))
        a = b.astype(np.uint8)
        img = Image.fromarray(a)
        img.save('current.png',Overwrite= True)
        
        #uncorrected
        App = LoadImage('current.png',200,200,0,0,1)
        
        #uncorrected, fourier transform
        ft = np.fft.rfft2(a, s=None, axes=(-2, -1), norm=None).astype(np.uint8)
        img2 = Image.fromarray(ft)
        img2.save('current2.png', Overwrite= True)
        App = LoadImage('current2.png',200,200,0,1,1)
        
        #corrected
        #print_input(4)
        f= open("text.txt","w+")
        for entry in entries:
            f.write(entry.get()+"\n")
        f.close()
        with open("text.txt") as f:
            content = f.readlines()
            content = [x.strip() for x in content] 
        if (content[0]!=names[0]):
            !../Downloads/unblur_1.0.2/src/unblur < text.txt
        else:
            !../Downloads/unblur_1.0.2/src/unblur < defaults.txt
        f.close()
        App = LoadImage('current.png',200,200,1,0,1)

        #corrected, fourier transform
        ft2 = np.fft.rfft2(a, s=None, axes=(-2, -1), norm=None).astype(np.uint8)
        img4 = Image.fromarray(ft2)
        img4.save('current4.png', Overwrite= True)
        App = LoadImage("current4.png",200,200,1,1,1)
    
    else:
        #for non-mrcs, for testing
        App = LoadImage(s,200,200,0,0,1)
        App = LoadImage(s,200,200,0,1,1)
        App = LoadImage(s,200,200,1,0,1)
        App = LoadImage(s,200,200,1,1,1)        
    
def callback(event,arg):
    display("Pixel value:\n" + str(arg[event.x, event.y]) + 
            "\nAt location:\n(" + str(event.x) + "), (" + str(event.y)+")")
    
def print_input(num):
    print(entries[num].get())

#First
root = Tk.Tk()
root.title("Relion DoubleCheck")
root.geometry("620x650")

#font
#text = Tk.Text(root)
#myFont = Font(family="Times New Roman", size=16)

#Body
OptionsFrame = Frame(root)
OptionsFrame.grid(row=0, column=0, sticky=W)

w = Label(root, text="Uncorrected & Corrected           Fourier Transform").grid(row=0,column=1,sticky=W)

frame = Frame(root, width=100, height=100)
frame.bind("<Button-1>", callback)
frame.grid(row=2, column=0, sticky=W)

SelectionFrame = Frame(root)
SelectionFrame.grid(row=1, column=0, sticky=W)

DisplayFrame = Frame(root)
DisplayFrame.grid(row=1, column=1, sticky=W)

#popup menu
mainframe = SelectionFrame
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.grid(row=1, column=0)
# Create a Tkinter variable
tkvar = StringVar(SelectionFrame)
# Dictionary with options
choices = {'Y vs Z','X vs Y','Z vs B',}
tkvar.set('X vs Y') # set the default option
popupMenu = OptionMenu(mainframe, tkvar, *choices)
Label(mainframe, text="Select Graph Type").grid(row = 7, column = 0)
popupMenu.grid(row = 6, column= 0)
 
# on change dropdown value
def change_dropdown(*args):
    pass
 
# link function to change dropdown
tkvar.trace('w', change_dropdown)

s= "place.jpg"
App = LoadImage(s,200,200,0,0,1)
App = LoadImage(s,200,200,0,1,1)
App = LoadImage(s,200,200,1,0,1)
App = LoadImage(s,200,200,1,1,1) 
App = LoadImage(s,200,406,2,0,2) 

Button(SelectionFrame, text = "Load Images", width = 12, command= lambda:  clicked(InputBox.get())).grid(row=2,column=0,sticky=W+E+N+S)
Button(SelectionFrame, text = "Load Graph", width = 12, command=lambda:  showgraph()).grid(row=3,column=0,sticky=W+E+N+S)

InputBox = Entry(SelectionFrame, width = 20, bg = "light grey")
InputBox.insert(0, "Oct19_10.00.55_DW.mrc")
InputBox.grid(row=0, column=0, sticky=W)

OutputBox = Text(SelectionFrame, width = 20, height = 5, bg = "light grey")
OutputBox.insert(END, "Pixel value:\n\nAt location:\n\n")
OutputBox.grid(row=1, column=0, sticky=W+E+N+S)

#unblur input
w = Label(SelectionFrame, text="Unblur Input").grid(row=9,column=0,sticky=N+E+S+W)
w = Label(SelectionFrame, text="\n\n\n\n\n\n\n\n").grid(row=8,column=0,sticky=N+E+S+W)

x = 10
names = ["Input stack filename","Number of frames per movie","Output aligned sum file","Output shifts file",
         "Pixel size of images (A)","Apply Dose filter?","Save Aligned Frames?","Set Expert Options?"]
entries = [Entry(SelectionFrame, width = 20, bg = "light grey") for _ in range(8)]

for entry in entries:
    entry.grid(row=x, column=0, sticky=W)
    entry.insert(0, names[x-10])
    x+=1

#Last
root.mainloop()
