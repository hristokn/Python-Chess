from pygame import Surface
from mouse import Clickable
from pygame.event import Event
from drawing import Drawable

class View(Clickable, Drawable):
    def __init__(self, x1, y1, priority, img_lib, img):
        x2 = x1
        y2 = y1
        try:
            _x2, _y2 = img_lib[img].get_size()
            x2 += _x2 
            y2 += _y2 
        except KeyError:
            pass
        Clickable.__init__(self, x1, y1, x2, y2, priority)
        Drawable.__init__(self, x1, y1, img_lib, img)

    def update(self):
        pass



class Button(View):
    def __init__(self, x1, y1, priority, img_lib, button_img,
                pressed_button_img, click_function):
        View.__init__(self, x1, y1, priority, img_lib, button_img)
        self._pressed_button_img = pressed_button_img
        self._is_held = False
        self._click_function = click_function

    def recieve_click(self, event: Event) -> bool:
        super().recieve_click(event)
        x,y = event.pos

        if self.collides(x,y):
            if self.left_buttop_down:
                self.hold_button()
            if self.left_buttop_up and self._is_held:
                self.release_button()
                self.click()
            self.clear()
            return True
        else:
            self.clear()
            self.release_button() 
            return False


    def hold_button(self):
        self._is_held = True

    def release_button(self):
        self._is_held = False

    def _click(self, **kwargs):
        self._click_function(**kwargs)

    def click(self):
        self._click()

    def draw(self, surface: Surface):
        if not self._is_held:
          return super().draw(surface)
        else:
            try:    
                surface.blit(self.image_library[self._pressed_button_img], (self.draw_x1, self.draw_y1))
            except KeyError:
                pass

    def update(self):
        pass

    def recieve_mouse_motion(self, event: Event):
        return super().recieve_mouse_motion(event)
    