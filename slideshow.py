from itertools import cycle
from PIL import ImageTk, Image
from os import walk
import pyinotify
import thread

try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk

class App(tk.Tk, pyinotify.ProcessEvent):
    '''Tk window/label adjusts to size of image'''
    def __init__(self, delay, folder):
        # the root will be self
        tk.Tk.__init__(self)
        # set x, y position only
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry('{0}x{1}+0+0'.format(w, h))
        self.configure(background='black')
        self.attributes('-fullscreen', True)
        self.delay = delay
        self.w = w
        self.h = h
        self.folder = folder
        self.pictures = []
        self.picCount = 0
        self.picture_display = tk.Label(self, height=h, width=w)
        self.picture_display.configure(background='black')
        self.picture_display.pack()
        self.curImage = None
        self.focus_force()
        self.bind('q', self.exitapp)
        # Start file monitor
        self.wm = pyinotify.WatchManager()
        self.wm.add_watch(self.folder, pyinotify.IN_CLOSE_WRITE)
        self.notifier = pyinotify.Notifier(self.wm, self)
        thread.start_new_thread(self.notifier.loop, ())
        self.getInitialPics()

    def exitapp(self, e):
        self.destroy()

    def getInitialPics(self):
        for (dirPath, dirNames, filenames) in walk(self.folder):
            for filename in filenames:
                self.pictures.append(self.folder + "/" + filename)

    def show_slides(self):
        '''cycle through the images and show them'''
        # CHeck if pictures is empty
        if self.pictures:
            self.curImage = ImageTk.PhotoImage(Image.open(self.pictures[self.picCount]))
            self.picCount += 1
            if self.picCount >= len(self.pictures):
                self.picCount = 0
            self.picture_display.config(image=self.curImage)
        
        self.after(self.delay, self.show_slides)

    def run(self):
        self.mainloop()

    def process_IN_CLOSE_WRITE(self, event):
        self.pictures = self.pictures[:self.picCount + 1] \
            + [event.pathname] \
            + self.pictures[self.picCount + 1:]
    
    def update_cycle(self):
        self.after(5000, self.update_cycle)
