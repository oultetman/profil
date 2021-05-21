from tkinter import *
from PIL import ImageTk, Image
from geo2d import *


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.image = Image.open("photo.jpg")
        self.photo = ImageTk.PhotoImage(self.image)
        print(self.image.size[0])
        self.canvas = Canvas(self, width=self.image.size[0], height=self.image.size[1])
        self.canvas.create_image(0, 0, anchor=NW, image=self.photo)
        self.segment = Segment(Point(100, 200), Point(800, 300))
        self.x = self.segment.p1.x
        self.y = self.segment.p1.y
        self.ch = self.canvas.create_line(self.segment.p1.x - 5, self.segment.p1.y, self.segment.p1.x + 5,
                                          self.segment.p1.y)
        self.cv = self.canvas.create_line(self.segment.p1.x, self.segment.p1.y - 5, self.segment.p1.x,
                                          self.segment.p1.y + 5)
        self.canvas.pack()
        self.ligne = self.canvas.create_line(self.seg_to_tuple(self.segment))
        self.geometry(f"{self.image.size[0]}x{self.image.size[1]}")
        self.key_down = False
        self.bind('<KeyPress>', self.down, add='+')
        self.bind('<KeyRelease>', self.up)
        self.increment = 1

    def down(self, event):
        if not self.key_down:
            print(event.keysym ,self.increment)
            if event.keysym == "Right" and self.x < self.segment.get_xmax():
                self.x += self.increment
                self.x = min(self.x,self.segment.get_xmax())
            elif event.keysym == "Left" and self.x > self.segment.get_xmin():
                self.x -= self.increment
                self.x = max(self.x, self.segment.get_xmin())
            elif event.keysym == "Shift_L":
                self.increment = 30
            self.y = self.segment.get_y(self.x)
            self.croix()

    def up(self, event):
        self.key_down = False
        if event.keysym == "Shift_L":
            self.increment = 1


    def seg_to_tuple(self, seg: Segment):
        return (seg.p1.x, seg.p1.y, seg.p2.x, seg.p2.y)

    def croix(self):
        self.canvas.coords(self.ch, self.x - 5, self.y, self.x + 5, self.y)
        self.canvas.coords(self.cv, self.x, self.y - 5, self.x, self.y + 5)
