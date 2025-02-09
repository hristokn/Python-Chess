from view.view import View
from pygame import Surface
from pygame.font import SysFont, get_default_font

class Text(View):
    def __init__(self, x1, y1, x2, y2, priority, img_lib, text):
        super().__init__(x1, y1, priority, img_lib, '')
        width = x2 - x1
        height = y2 - y1
        self.resize(width, height)
        self.text = text
        self.font = SysFont(get_default_font(), 40)
        self.prepare_text(width, height)

    def draw(self, surface: Surface):
        super().draw(surface)
        surface.blit(self.font_img, (self.text_x+self.draw_x1, self.text_y + self.draw_y1))

    def prepare_text(self):
        width = self.x2 - self.x1
        height = self.y2 - self.y1
        self.prepare_text(width, height)

    def prepare_text(self, width, height):
        self.text_width, self.text_height = self.font.size(self.text)
        self.button_width = width
        self.button_height = height
        self.text_x = (self.button_width - self.text_width)/2
        self.text_y = (self.button_height - self.text_height)/2
        self.font_img = self.font.render(self.text, 0, 'black')

