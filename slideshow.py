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
        self.delay = delay
        self.w = w
        self.h = h
        self.folder = folder
        self.pictures = []
        self.picCount = 0
        # allows repeat cycling through the pictures
        # store as (img_object, img_name) tuple
        # self.pictures = cycle((ImageTk.PhotoImage(Image.open(image).resize((w, h), Image.ANTIALIAS)), image)
        #                       for image in image_files)
        self.picture_display = tk.Label(self)
        self.picture_display.pack()
        self.filenames = set()

    def show_slides(self):
        '''cycle through the images and show them'''
        # CHeck if pictures is empty
        if self.pictures:
            img_object = self.pictures[self.picCount]
            self.picCount += 1
            if self.picCount >= len(self.pictures):
                self.picCount = 0
            self.picture_display.config(image=img_object)
        # next works with Python26 or higher
        #img_object, img_name = next(self.pictures)
        
        # shows the image filename, but could be expanded
        # to show an associated description of the image
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
                    + [ImageTk.PhotoImage(Image.open(self.folder + "/" + filename).resize((self.w, self.h), Image.ANTIALIAS))] \
                    + self.pictures[self.picCount + 1:]
            break
        self.after(5000, self.update_cycle)

# set milliseconds time between slides
delay = 3500

# get a series of gif images you have in the working folder
# or use full path, or set directory to where the images are
folder = 'Pictures/'

app = App(delay, folder)
app.show_slides()
app.update_cycle()
app.run()