from PIL import Image, ImageTk
import tkinter as tk
from tkinter.filedialog import asksaveasfilename
from random import random as ran, choice
from os import listdir, mkdir
from os.path import isdir
from subprocess import Popen
# Fetch sprites

if not isdir("./assets"):
    mkdir("./assets")
characters = listdir("./assets")

vis = tk.Tk()
vis.attributes("-fullscreen", 1)

rows = min(len(characters)+1, 16)
columns = (len(characters)+1) / 16
if columns % 1 != 0:
    columns = int(columns) + 1
else:
    columns = int(columns)

root = tk.Tk()
root.geometry(f"{columns*300+50}x{60 + min(16, len(characters)+1)*30}")
root.title("Deltarune Wallpaper Maker")
root.attributes("-topmost", 1)
root.attributes("-alpha", 0.8)
root.bind("")

wid = root.winfo_screenwidth()
hei = root.winfo_screenheight()
img = Image.new("RGBA", (wid, hei), "#000F")
tkimg = ImageTk.PhotoImage(img)
imgdisplay = tk.Label(vis, image=tkimg)
imgdisplay.place(relwidth=1, relheight=1)


chances:dict[str, tk.IntVar] = {}
scales:dict[str, tk.Scale] = {}

for c in range(len(characters)):
    chances[characters[c]] = tk.IntVar(root, int(ran()*51))
    scales[characters[c]] = tk.Scale(root, from_=0, to=50, width=8, variable=chances[characters[c]], orient="horizontal", showvalue=False, resolution=1, label=characters[c].capitalize() + " chance")
    scales[characters[c]].place(width=-10-90/columns, relwidth=1/columns, x=90 + c//16*290, y=55+(c%16)*30)

addimgbtn = tk.Button(root, text="Open image folder...")
addimgbtn.place(width=-10-90/columns, relwidth=1/columns, x=90 + len(characters)//16*290, y=58+(len(characters)%16)*30)

def openfolder(event):
    global addimgbtn
    Popen('explorer .\\assets')
    addimgbtn.config(text="Restart program to update")

addimgbtn.bind("<Button-1>", openfolder)
spriteamount = tk.IntVar(root,100)
currentspriteamount = 0
spriteamountscale = tk.Scale(root, from_=1, to=10000, width=15, variable=spriteamount)
spriteamountscale.place(y=15, x=10, height=-30, relheight=1)
spritescale = tk.IntVar(root, 1+int(ran()*10))
spritescalescale = tk.Scale(root, from_=1, to=10, variable=spritescale, orient="horizontal", label="Scale")
spritescalescale.place(width=-200, relwidth=1, x=80)
countinglabel = tk.Label(root, text="", fg="#00F", font="DeterminationMonoWeb", justify="center")
countinglabel.place(relwidth=0.4, relx=0.5, rely=-0.5, anchor=tk.CENTER)

def generate(event):
    global characters, chances, spriteamount, spritescale, tkimg, wid, hei, imgdisplay, img, countinglabel
    countinglabel.place(rely=0.5)
    spramount = spriteamount.get()
    chancelist = []
    img = Image.new("RGBA", (wid, hei), "#000F")
    for c in characters:
        chancelist += [c]*chances[c].get()
    for i in range(spramount):
        char = choice(chancelist)
        aux = Image.open("./assets/" + char + "/" + choice(listdir("./assets/" + char)))
        aux = aux.resize((aux.size[0]*spritescale.get(), aux.size[1]*spritescale.get()), Image.Resampling.NEAREST)
        img.alpha_composite(aux, (int(ran()*(wid+aux.size[0]))-aux.size[0], int(ran()*(hei+aux.size[1]))-aux.size[1]))
        if i % 10 == 0:
            countinglabel.config(text=str(i) + "/" + str(spramount))
            root.update()
            if i % 200 == 0:
                tkimg = ImageTk.PhotoImage(img)
                imgdisplay.config(image=tkimg)
                vis.update()
    tkimg = ImageTk.PhotoImage(img)
    imgdisplay.config(image=tkimg)
    vis.update()
    countinglabel.place(rely=-0.5)

def save(event):
    global img, root
    root.attributes("-topmost", 0)
    root.attributes("-alpha", 1)
    img.save(asksaveasfilename(title="Save new background", initialfile="background.png"))
    root.attributes("-topmost", 1)
    root.attributes("-alpha", 0.8)

generatebtn = tk.Button(root, text="Generate")
generatebtn.bind("<Button-1>", generate)
generatebtn.place(x=-115, y=15, width=55, relx=1, height=20)

savebtn = tk.Button(root, text="Save...")
savebtn.bind("<Button-1>", save)
savebtn.place(x=-60,y=15, width=45, relx=1, height=20)

def killbg(event):
    global vis
    vis.destroy()

def killroot(event):
    global root
    root.destroy()

root.bind("<Destroy>", killbg)
vis.bind("<Destroy>", killroot)
root.mainloop()
