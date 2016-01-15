from itertools import cycle
from PIL import ImageTk, Image
from os import walk

try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk

class App(tk.Tk):
    '''Tk window/label adjusts to size of image'''
    def __init__(self, delay, folder):
        # the root will be self
        tk.Tk.__init__(self)
        # set x, y position only
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.overrideredirect(1)
        self.geometry('{0}x{1}+0+0'.format(w, h))
        self.configure(background='black')
        self.delay = delay
        self.w = w
        self.h = h
        self.folder = folder
        self.pictures = []
        self.picCount = 0
        self.picture_display = tk.Label(self)
        self.picture_display.configure(background='black')
        self.picture_display.pack()
        self.filenames = set()
        self.curImage = None

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

    def update_cycle(self):
        ''' Checks if new file has been added and then adds it'''
        notSeen = set()
        for (dirpath, dirnames, filenames) in walk(self.folder):
            for filename in filenames:
                if ".DS_Store" not in filename and filename not in self.filenames:
                    self.filenames.add(filename)
                    self.pictures = self.pictures[:self.picCount + 1] \
                    + [self.folder + "/" + filename] \
                    + self.pictures[self.picCount + 1:]
            break
        self.after(5000, self.update_cycle)
