from pygame import Surface
from mouse import Clickable
from view.component import Component

class View(Clickable, Component):
    def __init__(self, x1, y1, priority, img_lib, img):
        x2 = x1
        y2 = y1
        try:
            if(issubclass(img.__class__, Surface)):
                _x2, _y2 = img.get_size()
            else:
                _x2, _y2 = img_lib[img].get_size()
            x2 += _x2 
            y2 += _y2 
        except KeyError:
            pass
        Clickable.__init__(self, x1, y1, x2, y2, priority)
        Component.__init__(self, x1, y1, img_lib, img)

    def move(self, x, y):
        Clickable.move(self, x, y)
        Component.move(self, x, y)

    def change_image(self, img):
        self.image = img
        width = 0
        heigth = 0
        try:
            if(issubclass(img.__class__, Surface)):
                width, heigth = img.get_size()
            else:
                width, heigth = self.image_library[img].get_size()
        except KeyError:
            pass
        Clickable.resize(self, width, heigth)