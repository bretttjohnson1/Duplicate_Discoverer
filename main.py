import xxhash, os, sys
from tkinter import Tk,Listbox,Button
from tkinter import filedialog
#from tkFileDialog import askdirectory
import subprocess
#import ttk
from tkinter.ttk import Treeview
from tkinter.filedialog import askdirectory
import ast

class Search:
    def hashdirectories(self,directories,map):
        for dir in directories:
            self.hashdirectory(dir,map)
        return map

    def hashdirectory(self,directory,map):
        hashfunc = xxhash.xxh32()
        for file in os.listdir(directory):
            if(os.path.isdir(os.path.join(directory,file))):
                #print os.path.join(directory,file)
                key = self.hashdirectory(os.path.join(directory,file),map)
                if key in map:
                    map[key] = map[key] + "?"+os.path.join(directory,file)
                else:
                    map[key] = os.path.join(directory,file)
                hashfunc.update(key)
            if(os.path.isfile(os.path.join(directory,file))):
                hf = xxhash.xxh64()
                f = open(os.path.join(directory,file),'rb').read()
                byts = bytes(f)
                #mem = memoryview(byts)
                buffersize = 1048576
                bytesize = sys.getsizeof(byts)
                if bytesize-buffersize>0:
                    for i in range(0,bytesize-buffersize,buffersize):
                        if bytesize-i>buffersize:
                            hf.update(byts[i:(i+buffersize)])
                        else:
                            hf.update(byts[i:])
                else:
                    hf.update(byts[0:])

                key = hf.digest()
                if key in map:
                    map[key] = map[key] + "?"+os.path.join(directory,file)
                else:
                    map[key] = os.path.join(directory,file)
                hashfunc.update(key)
        key = hashfunc.digest()
        return key

class Window:
    def fillTree(self,path, parent, list):
        for file in os.listdir(path):
            abspath = os.path.join(path,file)
            color = ""
            treelist = None
            for mini in list:
                if abspath in mini:
                    color = 'red'
                    treelist = mini
                else:
                    for lk in mini:
                        if abspath in lk:
                            color = 'yellow'
            child = None
            if color == 'red':
                child = self.tree.insert(parent,'end',text=(file+" matches "+str(treelist[1:])),open=False,tags=(abspath,'red',str(treelist)))
            elif color == 'yellow':
                child = self.tree.insert(parent,'end',text=file,open=False,tags=(abspath,'yellow'))
            else:
                child = self.tree.insert(parent,'end',text=file,open=False,tags=(abspath,'white'))
            if(os.path.isdir(abspath)):
                self.tree.insert(child,'end',text='',open=False)
    def __init__(self,list,dirlist):
        self.root = Tk()
        self.list = list
        self.root.geometry('600x600')
        self.tree = Treeview(self.root ,height=15)
        self.tree.pack(expand='yes',fill='both')
        self.tree.heading('#0',text="files")
        self.tree.tag_configure('red',background='red',foreground='white')
        self.tree.tag_configure('yellow',background='yellow')
        self.tree.bind("<Double-1>",self.onDoubleClick)
        self.tree.bind("<<TreeviewOpen>>",self.onOpen)
        self.tree.bind("<<TreeviewClose>>",self.onClose)
        for path in dirlist:
            branch = self.tree.insert('','end',text=path,open=True,tags=(path,'white'))
            self.fillTree(path,branch,list)
        self.root.mainloop()

    def onDoubleClick(self,event):
        item = self.tree.selection()[0]
        print ("clicked" + str(self.tree.item(item,'tags')[0]))
        if str(self.tree.item(item,'tags')[1]) == "red":
            for link in ast.literal_eval(str(self.tree.item(item,'tags')[2])):
                filedir =  os.path.dirname(link)
                if os.name == 'nt':
                    os.startfile(filedir)
                elif os.name == 'posix':
                    subprocess.Popen(["xdg-open",filedir])

    def onOpen(self,event):
        item = self.tree.selection()[0]
        if self.tree.parent(item) != '':
            if len(self.tree.get_children(item))>0:
                self.tree.delete(self.tree.get_children(item))
            abspath = str(self.tree.item(item,'tags')[0])
            if(os.path.isdir(abspath)):
                self.fillTree(abspath, item,self.list)
    def onClose(self,event):
        item = self.tree.selection()[0]
        if self.tree.parent(item) != '':
            self.tree.delete(self.tree.get_children(item))

dirlist = []

hh = Search()
map = {}

def addDir():
    global listview
    dir = askdirectory()
    if os.path.isdir(dir):
        dirlist.append(dir)
        listview.insert('end',str(dir))
def Done():
    global filechooser
    filechooser.destroy()

filechooser = Tk()
filechooser.geometry('500x500')
button  = Button(filechooser,text="Add Directory",command=addDir)
listview = Listbox(filechooser)
closebutton = Button(filechooser,text="Done",command=Done)
button.pack(fill='x')
listview.pack(fill="both")
closebutton.pack()
filechooser.mainloop()

hh.hashdirectories(dirlist,map)

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

for minilist in list:
    print (minilist)



root = Window(list,dirlist)
