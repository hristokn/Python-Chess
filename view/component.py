from game.drawing import Drawable


class Component(Drawable):
    def __init__(self, x1, y1, img_lib, img):
        Drawable.__init__(self, x1, y1, img_lib, img)
    
    def update(self):
        pass

    def destroy(self):
        pass