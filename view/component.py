from game.drawing import Drawable
from game.custom_events import EventObserver


class Component(Drawable, EventObserver):
    def __init__(self, x1, y1, img_lib, img):
        Drawable.__init__(self, x1, y1, img_lib, img)
    
    def update(self):
        pass

    def destroy(self):
        pass

    def receive_event(self, event):
        return super().receive_event(event)