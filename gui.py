from tkinter import *
from PIL import ImageTk,Image

#Subroutines
def display():
    OutputBox.delete('1.0',END)
    temp = InputBox.get()
    OutputBox.insert(END, temp)
    InputBox.delete(0,END)
    
def clicked(s):
    
    #uncorrected (convert mrc to showable image)
    image = Image.open(s)
    image = image.resize((250, 250), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    label = Label(DisplayFrame, image=photo)
    label.image = photo
    label.grid(row=0, column=0, sticky = W)
    
    #uncorrect with Fourier Transform (fourier transform)
    image = Image.open(s)
    image = image.resize((250, 250), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    label = Label(DisplayFrame, image=photo)
    label.image = photo
    label.grid(row=0, column=1, sticky = W)
    
    #corrected (use unblur to correct the mrc file)
    image = Image.open(s)
    image = image.resize((250, 250), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    label = Label(DisplayFrame, image=photo)
    label.image = photo
    label.grid(row=1, column=0, sticky = W)
    
    #corrected with Fourier Transform (fourier transform)
    image = Image.open(s)
    image = image.resize((250, 250), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    label = Label(DisplayFrame, image=photo)
    label.image = photo
    label.grid(row=1, column=1, sticky = W)

#First
root = Tk()
root.title("Relion DoubleCheck")
root.geometry("800x1000")

#Body
OptionsFrame = Frame(root)
OptionsFrame.grid(row=0, column=0, sticky=W)

SelectionFrame = Frame(root)
SelectionFrame.grid(row=1, column=0, sticky=W)

DisplayFrame = Frame(root)
DisplayFrame.grid(row=1, column=1, sticky=W)

Label(OptionsFrame, text = "Options | Go | Here", font = 16).grid(row=0,column=0,sticky=W)


InputBox = Entry(SelectionFrame, width = 20, bg = "light grey")
InputBox.grid(row=2, column=0, sticky=W)

Button(SelectionFrame, text = "Load Images", width = 12, command= lambda:  clicked(InputBox.get())).grid(row=0,column=0,sticky=W)
Button(SelectionFrame, text = "Load Graph", width = 12, command=display).grid(row=1,column=0,sticky=W)

OutputBox = Text(SelectionFrame, width = 20, height = 5, bg = "light grey")
OutputBox.grid(row=3, column=0, sticky=W)

#Last
root.mainloop()
