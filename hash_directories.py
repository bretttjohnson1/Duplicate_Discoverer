import xxhash, os, sys
from tkinter import Tk
from tkinter.ttk import Progressbar
from threading import Thread

class Hasher:
    def hash(self,directories,map,size):
            self.ldb = Loadbar(size)
            t = Thread(target=self.hashdirectories,args=(directories,map))
            t.start()
            self.ldb.start()

    def hashdirectories(self,directories,map):
        for dir in directories:
            self.hashdirectory(dir,map)
        self.ldb.kill()


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
                self.ldb.pgb.step(bytesize/1024)
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

class Loadbar:
    def __init__(self,size):
        self.loadbar = Tk()
        self.loadbar.wm_title('Loading')
        self.pgb = Progressbar(self.loadbar,orient='horizontal',length='500',maximum=int(size))
        self.pgb.pack()
        self.pgb.start()
    def start(self):
        self.loadbar.mainloop()
    def kill(self):
        self.loadbar.destroy()
