# Imports
import time
import checkURL
import checkNet
import requests
from tkinter import *
from pytube import YouTube
from PIL import Image, ImageTk
from tkinter import messagebox as mb
from tkinter.filedialog import askdirectory


# Functions #
def close(event):
    root.destroy()
    sys.exit()


def changeFocus(event, entry_num):
    if entry_num == 0:
        saveEntry.focus_set()
        root.update()
        if len(urlEntry.get()) == 0:
            mb.showerror("Error", "Please fill link input field!")
            return

    elif entry_num == 1:
        urlEntry.focus_set()


def quality():
    try:
        global yt, videos
        yt = YouTube(urlEntry.get())
        videos = yt.streams.filter(mime_type="video/mp4")
        count = 1
        for v in videos:
            qualityList.insert(END,
                               (str(count) + ". " + str(v)[str(v).find("res="):str(v).find("fps=")] + '"\n\n').replace(
                                   '"',
                                   '').strip())
            count += 1
    except:
        mb.showerror("Error", "This isn't YouTube link.")


def browse():
    filePath = askdirectory()
    saveEntry.delete(0, END)
    saveEntry.insert(END, filePath)


def change(event, typeId):
    if typeId == 0:
        buttonLabel['image'] = buttonSkins[0]
        root.update()
        return
    elif typeId == 1:
        buttonLabel['image'] = buttonSkins[1]
        root.update()
        time.sleep(0.1)
    elif typeId == 2:
        buttonLabel['image'] = buttonSkins[0]
        root.update()
        time.sleep(0.1)


def download(event):
    buttonLabel['image'] = buttonSkins[2]
    root.update()
    buttonLabel.after(200, lambda: change(0, 0))
    if len(urlEntry.get()) == 0:
        mb.showerror("Error", "Please fill link entry.")
        return
    elif not checkNet.connected_to_internet():
        mb.showerror("Error", "Failed to connect to Net.")
        return
    elif not checkURL.check_url(urlEntry.get()):
        mb.showerror("Error", "Failed to find this Web site.")
        return
    elif len(onClickList) == 0:
        mb.showerror("Error", "Failed to choose quality. Please fill this entry.")
        return
    try:
        video = yt.streams.filter(progressive=True, file_extension='mp4',
                                  resolution=onClickList[onClickList.find("=") + 1:])
        path = saveEntry.get()
        video = video[-1]
        video.download(path)
    except Exception as e:
        mb.showerror("Error", "Failed to select this quality. Please select another.")


def CurSelet(event):
    global onClickList
    value = str((qualityList.get(qualityList.curselection())))
    onClickList = value


# Window #
root = Tk()
root.title("YoutubeDownloader")
root.geometry("600x1000")
root['bg'] = "#1E1E1E"
root.resizable(False, False)
root.iconbitmap("static/icons/icon.ico")

# Variables #

onClickList = ""

# Fonts
fonts = [("Impact", "40"), ("Impact", "30"),
         ("Impact", "24"), ("Impact", "18")]
# Colors
WHITE = "#fff"
BLACK = "#000"
GREY = "#1e1e1e"

# Objects #
# Images
buttonSkins = [ImageTk.PhotoImage(file="static/img/downloadButton/downloadImage.png"),
               ImageTk.PhotoImage(file="static/img/downloadButton/downloadAimImage.png"),
               ImageTk.PhotoImage(file="static/img/downloadButton/downloadOnPressedImage.png")]

browseSkins = [ImageTk.PhotoImage(file="static/img/findFolder/findImage.png")]

openSkins = [ImageTk.PhotoImage(file="static/img/openFolder/openImage.png")]

infoSkins = [ImageTk.PhotoImage(file="static/img/videoInfo/infoImage.png")]

# Frame
urlFrame = Frame(bg=GREY)
qualityFrame = Frame(bg=GREY)
saveFrame = Frame(bg=GREY)

# Scrollbar
scroll1 = Scrollbar(qualityFrame)

# Label
titleLabel = Label(root, text="YouTube Download", font=fonts[0], bg=GREY, fg=WHITE)
urlLabel = Label(urlFrame, text="Link to video:", font=fonts[1], bg=GREY, fg=WHITE)
qualityLabel = Label(qualityFrame, text="Quality:", font=fonts[1], bg=GREY, fg=WHITE)
saveLabel = Label(saveFrame, text="Where save:", font=fonts[1], bg=GREY, fg=WHITE)
buttonLabel = Label(root, image=buttonSkins[0], bg=GREY, activebackground=GREY)

# Entry
urlEntry = Entry(urlFrame, font=fonts[2], fg=BLACK)
saveEntry = Entry(saveFrame, font=fonts[2], fg=BLACK, width=15)

# Lists
qualityList = Listbox(qualityFrame, font=fonts[2], height=5, width=25)
qualityList.config(yscrollcommand=scroll1.set)
scroll1.config(command=qualityList.yview)

# Buttons
browseButton = Button(root, image=browseSkins[0], bg=GREY, border=0, command=browse)
getQuality = Button(root, text="Get quality!", font=("Impact", "15"), bg=WHITE, fg=BLACK, height=1,
                    command=quality)

# Pack #
titleLabel.pack(pady=50)

urlFrame.pack(anchor=NW, pady=50, padx=20)
urlLabel.pack(side=LEFT)
urlEntry.pack(side=LEFT, padx=20)

qualityFrame.pack(anchor=NW, padx=20)
qualityLabel.pack(anchor=NW, side=LEFT)
scroll1.pack(side=RIGHT, fill=Y)
qualityList.pack(padx=20)

saveFrame.pack(anchor=NW, side=LEFT, pady=50, padx=20)
saveLabel.pack(side=LEFT)
saveEntry.pack(side=LEFT, padx=20)
browseButton.place(x=505, y=585)

buttonLabel.place(x=100, y=665)

getQuality.place(x=455, y=275)

# Bindings #
root.bind("<Escape>", close)
root.bind("<Control-w>", close)
buttonLabel.bind('<Button-1>', download)
buttonLabel.bind('<Motion>', lambda a: change(a, 1))
buttonLabel.bind('<Leave>', lambda a: change(a, 2))

urlEntry.bind("<Return>", lambda a: changeFocus(a, 0))
saveEntry.bind("<Return>", lambda a: changeFocus(a, 1))

qualityList.bind('<<ListboxSelect>>', CurSelet)

urlEntry.focus_set()
# urlEntry.insert(END, "https://www.youtube.com/watch?v=J1y_EDVnJDE")
saveEntry.insert(END, "D://")

root.mainloop()
