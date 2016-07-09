import os
from tkinter import Tk,Listbox,Button,Toplevel,Label
from tkinter.ttk import Treeview, Progressbar
import subprocess
import ast

class MiniWindow:
    def __init__(self,root,list):
        self.list = list
        self.mini = Toplevel(root)
        self.mini.wm_title("Matches")
        self.mini.geometry("%dx%d+%d+%d" %(500,200,root.winfo_x()+root.winfo_screenwidth(),root.winfo_y()+root.winfo_height()-root.winfo_screenheight()))
        self.filelist = Listbox(self.mini)
        for item in self.list:
            self.filelist.insert('end',str(item))
        self.filelist.bind("<<ListboxSelect>>",self.onClick)
        self.filelist.pack(fill="both")
    def onClick(self,event):
        print(self.filelist.curselection())
        index = int(self.filelist.curselection()[0])
        link = self.list[index]
        filedir = os.path.dirname(link)
        if os.name == 'nt':
            os.startfile(filedir)
        elif os.name == 'posix':
            subprocess.Popen(["xdg-open",filedir])

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
                            color = 'purple'
            child = None
            if color == 'red':
                child = self.tree.insert(parent,'end',text=file,open=False,tags=(abspath,'red',str(treelist)),)
            elif color == 'purple':
                child = self.tree.insert(parent,'end',text=file,open=False,tags=(abspath,'purple'))
            else:
                child = self.tree.insert(parent,'end',text=file,open=False,tags=(abspath,'white'))
            if(os.path.isdir(abspath)):
                self.tree.insert(child,'end',text='',open=False)
    def __init__(self,list,dirlist):
        self.root = Tk()
        self.root.wm_title("Duplicate_Files")
        self.min = None
        self.list = list
        self.root.geometry('600x600')
        self.tree = Treeview(self.root ,height=15)
        self.tree.pack(expand='yes',fill='both')
        self.tree.heading('#0',text="files")
        self.tree.tag_configure('red',foreground='red')
        self.tree.tag_configure('purple',foreground='#cc00ff')
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
            list_of_files = ast.literal_eval(str(self.tree.item(item,'tags')[2]))
            if self.min != None:
                if self.min.mini.winfo_exists():
                    self.min.mini.destroy()
            self.min = MiniWindow(self.root,list_of_files)

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
            if len(self.tree.get_children(item))>0:
                self.tree.delete(self.tree.get_children(item))
