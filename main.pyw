from PIL import Image, ImageTk
import tkinter as tk
from tkinter.ttk import Progressbar, Style
from tkinter.filedialog import asksaveasfilename
from random import random as ran, choice
from os import listdir, mkdir, remove
from os.path import isdir
from subprocess import Popen
from zipfile import ZipFile
from json import load
# Fetch sprites

if not isdir("./assets"):
    mkdir("./assets")
characters = listdir("./assets")
for c in characters:
    if c[-4:] == ".zip":
        zip = ZipFile("./assets/" + c, 'r')
        zip.extractall("./assets/")
        zip.close()
        remove("./assets/" + c)

characters = listdir("./assets/")

palette = load(open("./palette.json", "r"))

vis = tk.Tk()
#vis.attributes("-fullscreen", 1)
vis.geometry(f"{vis.winfo_screenwidth()}x{vis.winfo_screenheight()}+0+0")
vis.state("zoomed")
vis.title("Super cool wallpaper visualizer")

rows = min(len(characters)+1, 16)
columns = (len(characters)+1) / 16
if columns % 1 != 0:
    columns = int(columns) + 1
else:
    columns = int(columns)

root = tk.Tk()
root.geometry(f"{columns*300+50}x{60 + min(16, len(characters)+1)*50}")
root.title("Deltarune Wallpaper Maker")
root.attributes("-topmost", 1)
root.bind("")
root.config(bg="#000")

wid = root.winfo_screenwidth()
hei = root.winfo_screenheight()
img = Image.new("RGBA", (wid, hei), "#000F")
tkimg = ImageTk.PhotoImage(img)
imgdisplay = tk.Label(vis, image=tkimg)
imgdisplay.place(relwidth=1, relheight=1)


chances:dict[str, tk.IntVar] = {}
scales:dict[str, tk.Scale] = {}

style = {
    "font":("Determination Mono Web", 13),
    "background":"#000",
    "foreground":"#FFF",
    "activebackground":"#000",
    "relief":tk.FLAT,
    "border":2,
}
scalestyle = {
    "sliderlength":15,
    "resolution":1,
    "troughcolor":"#000",
    "highlightthickness":0
}
btnstyle = {
    "activeforeground":"#FFF"
}
for c in range(len(characters)):
    chances[characters[c]] = tk.IntVar(root, int(ran()*51))
    scales[characters[c]] = tk.Scale(
        root,
        from_=0,
        to=50,
        width=8,

        variable=chances[characters[c]],
        orient="horizontal",
        showvalue=False,
        label=characters[c].capitalize() + " chance",
        **style,
        **scalestyle
        )
    scales[characters[c]].place(width=-10-90/columns, relwidth=1/columns, x=90 + c//16*290, y=70+(c%16)*50)

addimgbtn = tk.Button(
    root,
    text="Open image folder...",
    **style
    )
addimgbtn.place(width=-10-90/columns, relwidth=1/columns, x=90 + len(characters)//16*290, y=76+(len(characters)%16)*50)

def openfolder(event):
    root.attributes("-topmost", 0)
    addimgbtn.config(text="Restart program to update", state="normal", fg="#F00")
    Popen("explorer ./assets")

def onenterbtn(event:tk.Event):
    event.widget.config(fg="#FF0", activeforeground="#FF0")
def onenterscale(event:tk.Event):
    event.widget.config(fg="#FF0")
def onleavebtn(event:tk.Event):
    event.widget.config(fg="#FFF", activeforeground="#FFF")
def onleavescale(event:tk.Event):
    event.widget.config(fg="#FFF")
addimgbtn.bind("<Button-1>", openfolder)
root.bind_class("Button", "<Enter>", onenterbtn)
root.bind_class("Button", "<Leave>", onleavebtn)
root.bind_class("Scale", "<Enter>", onenterscale)
root.bind_class("Scale", "<Leave>", onleavescale)

spriteamount = tk.IntVar(root, int(ran()*10001))
currentspriteamount = 0
spriteamountscale = tk.Scale(
    root,
    from_=1,
    to=10000,
    width=15,
    variable=spriteamount,
    **style,
    **scalestyle
    )
spriteamountscale.place(y=15, x=10, height=-30, relheight=1)
spritescale = tk.IntVar(root, 1+int(ran()*10))
spritescalescale = tk.Scale(
    root,
    from_= 1,
    to= 10,
    variable= spritescale,
    orient= "horizontal",
    label= "Scale",
    **style,
    **scalestyle
    )
spritescalescale.place(width=-200, relwidth=1, x=80)
countinglabel = tk.Label(
    vis,
    text="",
    fg="#FF0",
    bg="#000",
    highlightthickness=3,
    highlightcolor="#FFF",
    font=("Determination Mono Web", 17),
    justify="center")
countinglabel.place(width=150, x=0, y=-100, height=40)
pbar = Progressbar(vis, style="success.Striped.Horizontal.TProgressbar")
pbar.place(y=-100, relwidth=1, x=0, height=15)

def generate(event):
    global characters, chances, spriteamount, spritescale, tkimg, wid, hei, imgdisplay, img, countinglabel, pbar, root
    countinglabel.place(y=15)
    generatebtn.config(fg="#888")
    generatebtn.unbind("<Enter>")
    generatebtn.unbind("<Leave>")
    generatebtn.unbind("<Button-1>")
    spramount = spriteamount.get()
    root.iconify()
    #root.geometry(f"{columns*300+50}x0")
    pbar.config(maximum=spramount, value=0)
    pbar.place(y=0)
    chancelist = []
    scale = spritescale.get()
    img = Image.new("RGBA", (wid, hei), "#000F")
    for c in characters:
        chancelist += [c]*chances[c].get()
    if len(chancelist) == 0:
        chancelist = characters.copy()

    for i in range(spramount):
        char = choice(chancelist)
        aux = Image.open("./assets/" + char + "/" + choice(listdir("./assets/" + char)))
        aux = aux.resize((aux.size[0]*scale, aux.size[1]*scale), Image.Resampling.NEAREST)
        img.alpha_composite(aux, ((int(ran()*(wid+aux.size[0]))-aux.size[0])//scale*scale, (int(ran()*(hei+aux.size[1]))-aux.size[1])//scale*scale))
        if i % 10 == 0:
            countinglabel.config(text=str(i) + "/" + str(spramount))
            pbar.config(value=i)
            root.update()
            if i % 200 == 0:
                tkimg = ImageTk.PhotoImage(img)
                imgdisplay.config(image=tkimg)
                vis.update()
    tkimg = ImageTk.PhotoImage(img)
    imgdisplay.config(image=tkimg)
    vis.update()
    countinglabel.place(rely=-0.5)
    pbar.place(y=-100)
    root.deiconify()
    #root.geometry(f"{columns*300+50}x{60 + min(16, len(characters)+1)*50}")
    generatebtn.config(fg="#FFF")
    generatebtn.bind("<Enter>", onenterbtn)
    generatebtn.bind("<Leave>", onleavebtn)
    generatebtn.bind("<Button-1>", generate)


def save(event):
    global img, root
    root.attributes("-topmost", 0)
    img.save(asksaveasfilename(title="Save new background", initialfile="background.png"))
    root.attributes("-topmost", 1)

generatebtn = tk.Button(
    root,
    text="Generate",
    **style,
    **btnstyle
    )
generatebtn.bind("<Button-1>", generate)
generatebtn.place(x=-115, y=15, width=100, relx=1, height=20)

savebtn = tk.Button(
    root,
    text="Save...",
    **style
    )
savebtn.bind("<Button-1>", save)
savebtn.place(x=-115,y=35, width=100, relx=1, height=20)

def killbg(event):
    global vis
    vis.destroy()

def killroot(event):
    global root
    root.destroy()

root.bind("<Destroy>", killbg)
vis.bind("<Destroy>", killroot)
root.mainloop()
