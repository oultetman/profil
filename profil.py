from tkinter import *
from PIL import ImageTk, Image
from geo2d import *


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("640x480")
        self.image = Image.open("photo.jpg")
        self.photo = ImageTk.PhotoImage(self.image)
        print(self.image.size[0])
        self.canvas = Canvas(self, width=self.image.size[0], height=self.image.size[1])
        self.canvas.create_image(0, 0, anchor=NW, image=self.photo)
        self.canvas.pack()
        self.segment = Segment(Point(100, 200), Point(800, 300))
        self.ligne = self.canvas.create_line(self.seg_to_tuple(self.segment))

    def seg_to_tuple(self, seg: Segment):
        return (seg.p1.x, seg.p1.y, seg.p2.x, seg.p2.y)

    def croix(self):
        pass
