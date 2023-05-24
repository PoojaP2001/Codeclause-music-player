import os
import pygame
from tkinter import *
from tkinter.filedialog import askdirectory
from mutagen.id3 import ID3
from PIL import ImageTk, Image

root = Tk()
root.minsize(500, 500)

# Create a frame to hold the content
frame = Frame(root)
frame.pack()

# Load the image
image = Image.open("images.jpg")

# Resize the image to fit the window
#image = image.resize((500, 500), Image.ANTIALIAS)
image = image.resize((500, 500), Image.LANCZOS)


# Convert the image to Tkinter-compatible format
tk_image = ImageTk.PhotoImage(image)

# Create a label to display the image
image_label = Label(frame, image=tk_image)
image_label.place(x=0, y=0, relwidth=1, relheight=1)

listofsongs = []
realnames = []

v = StringVar()
songlabel = Label(frame, textvariable=v, width=35)

index = 0

def updatelabel():
    global index
    global songname
    v.set(realnames[index])
    
def directorychooser():
    directory = askdirectory()
    if directory:
        os.chdir(directory)
        for files in os.listdir(directory):
            if files.endswith(".mp3"):
                realdir = os.path.join(directory, files)

                audio = ID3(realdir)
                if 'TIT2' in audio:
                  realnames.append(audio['TIT2'].text[0])
                else:
                   print("Key 'TIT2' does not exist in the audio dictionary.")

                
                listofsongs.append(files)

        pygame.mixer.init()
        pygame.mixer.music.load(listofsongs[0])
        pygame.mixer.music.play()
        updatelabel()
directorychooser()



def nextsong(event):
    global index
    index += 1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()

def prevsong(event):
    global index
    index -= 1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()

def unpausesong(event):
    pygame.mixer.music.unpause()
    v.set("Song unpaused")

def pausesong(event):
    pygame.mixer.music.pause()
    v.set("Song Paused")

def stopsong(event):
    pygame.mixer.music.stop()
    v.set("")

label = Label(frame, text='Music Player')
label.pack()

listbox = Listbox(frame)
listbox.pack()

realnames.reverse()

for items in realnames:
    listbox.insert(0, items)

realnames.reverse()

nextbutton = Button(frame, text='Next Song')
nextbutton.pack()

previousbutton = Button(frame, text='Previous Song')
previousbutton.pack()

pausebutton = Button(frame, text='Pause Song')
pausebutton.pack()

unpausebutton = Button(frame, text='Unpause Song')
unpausebutton.pack()

stopbutton = Button(frame, text='Stop Music')
stopbutton.pack()

nextbutton.bind("<Button-1>", nextsong)
previousbutton.bind("<Button-1>", prevsong)
pausebutton.bind("<Button-1>", pausesong)
unpausebutton.bind("<Button-1>", unpausesong)
stopbutton.bind("<Button-1>", stopsong)

songlabel.pack()


root.mainloop()
