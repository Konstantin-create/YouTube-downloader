    # Imports #
import time
import checkNet
from tkinter import *
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinter import messagebox as mb
from win32api import GetSystemMetrics


# Functions #
def close(event):
    if mb.askquestion("Exit?", "Do you realy want to exit?"):
        root.destroy()
        sys.exit()


def loadingAnim():
    for i in range(101):
        try:
            pr.configure(value=i)
            pr.update()
            loadingProgressLabel["text"] = "{}%".format(i)
            if i < 50:
                time.sleep(0.05)
            elif i == 51:
                if checkNet.connected_to_internet():
                    pass
                else:
                    mb.showerror("Connection error", "Please connect to Internet!")
                    root.destroy()
                    sys.exit()
            elif i > 50 and i <= 80:
                time.sleep(0.1)
            elif i > 80 and i <= 90:
                time.sleep(0.2)
            elif i > 90:
                time.sleep(0.5)
        except:
            pass

    try:
        root.destroy()
        import main
    except:
        pass


# Variables #
WinWIDTH = GetSystemMetrics(0)
WinHEIGHT = GetSystemMetrics(1)


# Window settings #
root = Tk()
root['border'] = 1
root.overrideredirect(1)
root.iconbitmap("static/icons/icon.ico")
root.call("wm", "attributes", ".", "-topmost", "true")
root.call("wm", "attributes", ".", "-transparent")
root.geometry("800x400+{}+{}".format(str((WinWIDTH // 2) - 400), str((WinHEIGHT // 2) - 200)))


# Objects #
# Images
screenImage = ImageTk.PhotoImage(file="static/img/startBg/screen.png")

# Label
screenLabel = Label(root, image=screenImage)
loadingProgressLabel = Label(root, text="0%", font=("Impact", 35), bg="#1e1e1e", fg="#fff")

# Progress bar
pr = ttk.Progressbar(root, orient=HORIZONTAL, mode="determinate", length=700)


# Pack #
screenLabel.pack()
loadingProgressLabel.place(x=640, y=165)
pr.place(x=50, y=350)

loadingAnim()

# Bindings #
try:
    root.bind("<Escape>", close)
except:
    pass


# Main loop #
root.mainloop()
