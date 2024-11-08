from pygame import Surface
from pygame.font import SysFont, get_default_font
from mouse import Clickable
from pygame.event import Event
from drawing import Drawable

class View(Clickable, Drawable):
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
        Drawable.__init__(self, x1, y1, img_lib, img)

    def update(self):
        pass

    def move(self, x, y):
        Clickable.move(self, x, y)
        Drawable.move(self, x, y)

