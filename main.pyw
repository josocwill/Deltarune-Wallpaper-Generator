from PIL import Image, ImageTk
from PIL.ImageEnhance import Brightness
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

vis = tk.Tk()
vis.attributes("-fullscreen", 1)
vis.title("Super cool wallpaper visualizer")

rows = min(len(characters)+1, 16)
columns = (len(characters)+1) / 16
if columns % 1 != 0:
    columns = int(columns) + 1
else:
    columns = int(columns)

root = tk.Tk()
root.geometry(f"{columns*300+50}x{60 + min(16, len(characters)+1)*60}")
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
entries:dict[str, tk.Entry] = {}

style = {
    "font":("Determination Mono Web", 13),
    "background":"#000",
    "foreground":"#FFF",
    "relief":tk.FLAT,
    "border":2,
}
scalestyle = {
    "activebackground":"#000",
    "sliderlength":15,
    "troughcolor":"#000",
    "highlightthickness":0
}
btnstyle = {
    "activebackground":"#000",
    "activeforeground":"#FFF"
}

for c in range(len(characters)):
    chances[characters[c]] = tk.IntVar(root, 0)
    scales[characters[c]] = tk.Scale(
        root,
        from_=0,
        to=10000,
        width=8,
        variable=chances[characters[c]],
        orient="horizontal",
        showvalue=False,
        label=characters[c].capitalize(),
        **style,
        **scalestyle
        )
    scales[characters[c]].place(
        width=-110,
        relwidth=1/columns,
        relx = (c//16)/columns,
        x=80,
        y=70+(c%16)*42
        )
    entries[characters[c]] = tk.Entry(
        root,
        textvariable=chances[characters[c]],
        insertbackground="#FF0",
        highlightthickness=2,
        highlightcolor="#FFF",
        justify=tk.RIGHT,
        **style
        )
    entries[characters[c]].place(
        width = 60,
        
        x = 20,
        relx = (c//16)/columns,
        y=80+(c%16)*42
    )

addimgbtn = tk.Button(
    root,
    text="* Open image folder...",
    **style
    )
addimgbtn.place(width=-20, relwidth=1/columns, x=20, y=70+(len(characters)%16)*42, relx=(len(characters)//16)/columns)

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
root.bind_class("Entry", "<Enter>", onenterscale)
root.bind_class("Entry", "<Leave>", onleavescale)
vis.bind_class("Scale", "<Enter>", onenterscale)
vis.bind_class("Scale", "<Leave>", onleavescale)
vis.bind_class("Button", "<Enter>", onenterbtn)
vis.bind_class("Button", "<Leave>", onleavebtn)
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
darkness = tk.Variable(vis, 0)
def setdarkness(*args):
    global img, tkimg
    aux = Brightness(img).enhance(1-float(darkness.get()))
    tkimg = ImageTk.PhotoImage(aux)
    
    imgdisplay.config(image=tkimg)
    #vis.update()
darknessbar = tk.Scale(
    vis,
    from_=0,
    to= 1,
    resolution=0.01,
    label="Darkness",
    showvalue=True,
    variable = darkness,
    command = setdarkness,
    orient= "horizontal",
    **style,
    **scalestyle
)
darknessbar.place(x=0, rely=1, anchor=tk.SW, relwidth=1)
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

cancelbtn = tk.Button(
    vis,
    text="* Cancel",
    **style,
    **btnstyle
)

cancelbtn.place(y=-100, height=30, width=80, x=150)
def cancelgeneration(event):
    global running
    running = False
cancelbtn.bind("<Button-1>", cancelgeneration)

running = False

def generate(event):
    global characters, chances, spritescale, tkimg, wid, hei, imgdisplay, img, countinglabel, pbar, root, running
    countinglabel.place(y=15)
    cancelbtn.place(y=15)
    generatebtn.config(fg="#888")
    generatebtn.unbind("<Enter>")
    generatebtn.unbind("<Leave>")
    generatebtn.unbind("<Button-1>")
    root.iconify()
    #root.geometry(f"{columns*300+50}x0")
    chancelist = []
    scale = spritescale.get()
    img = Image.new("RGBA", (wid, hei), "#000F")
    for c in characters:
        chancelist += [c]*chances[c].get()
    if len(chancelist) == 0:
        chancelist = characters.copy()

    spramount = len(chancelist)
    pbar.config(maximum=spramount, value=0)
    pbar.place(y=0)
    running = True
    for i in range(spramount):
        if not running:
            break
        char = chancelist.pop(int(ran()*len(chancelist)))
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
    
    setdarkness()
    countinglabel.place(y=-100)
    cancelbtn.place(y=-100)
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
    darkimg = Brightness(img).enhance(darkness.get())
    darkimg.save(asksaveasfilename(title="Save new background", initialfile="background.png"))
    root.attributes("-topmost", 1)

generatebtn = tk.Button(
    root,
    text="* Generate",
    justify=tk.LEFT,
    anchor=tk.W,
    **style,
    **btnstyle
    )
generatebtn.bind("<Button-1>", generate)
generatebtn.place(x=-115, y=15, width=110, relx=1, height=20)

savebtn = tk.Button(
    root,
    text="* Save...",
    justify=tk.LEFT,
    anchor=tk.W,
    **style
    )
savebtn.bind("<Button-1>", save)
savebtn.place(x=-115,y=35, width=110, relx=1, height=20)

def killbg(event):
    global vis
    vis.destroy()

def killroot(event):
    global root
    root.destroy()

root.bind("<Destroy>", killbg)
vis.bind("<Destroy>", killroot)
root.mainloop()