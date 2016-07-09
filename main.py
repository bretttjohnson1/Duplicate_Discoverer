import os
from hash_directories import Hasher
from window import Window
from tkinter import filedialog
from tkinter import Tk,Listbox,Button,Label
from tkinter.filedialog import askdirectory

dirlist = []



class FileChooser:
    def __init__(self):
        self.filechooser = Tk()
        self.filechooser.geometry('500x500')
        self.button  = Button(self.filechooser,text="Add Directory",command=self.addDir)
        self.listview = Listbox(self.filechooser)
        self.closebutton = Button(self.filechooser,text="Scan",command=self.Done)
        self.listview.pack(fill="both")
        self.button.pack(fill='x')
        helptext = """Select directories by pressing the "Add Directory" Button, then press Scan.
                        \n When the file tree appears, red text means the file or folder is a duplicate.
                        \n purple means the folder contains duplicates but itself is not a duplicate.
                        \n Double Click on red text entries to view matches"""
        self.instructions = Label(self.filechooser, text=helptext)
        self.instructions.pack(fill='both')
        self.closebutton.pack()


        self.filechooser.mainloop()
    def Done(self):
        self.filechooser.destroy()
    def addDir(self):
        dir = askdirectory()
        if os.path.isdir(dir):
            dirlist.append(dir)
            self.listview.insert('end',str(dir))
fc = FileChooser()
hh = Hasher()

map = {}
size = 0
for dir in dirlist:
    for d,n,filenames in os.walk(dir):
        for f in filenames:
            if os.path.isfile(os.path.join(d,f)):
                size += os.path.getsize(os.path.join(d,f))/1024

hh.hash(dirlist,map,size)

list = []
for key in map:
    if '?' in map[key]:
        items = []
        index = 0
        old_index = 0
        for i,char in enumerate(map[key]):
            if(char is '?'):
                index = i
                if old_index != 0:
                    items.append(map[key][old_index+1:index])
                else:
                    items.append(map[key][old_index:index])

                old_index=index

        items.append(map[key][index+1:])
        list.append(items)

root = Window(list,dirlist)
