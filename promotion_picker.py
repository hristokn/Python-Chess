from pygame.event import Event
from view import View, Button
from drawing import SQUARE_SIZE, get_piece_image_name, ImageLibrary
from pygame import Surface
from chess.enums import PieceType, Color

class PromotionPicker(View):
    def __init__(self, x1, y1, priority, img_lib: ImageLibrary, color: Color, draw_down, click_function):
        self.background = Surface((SQUARE_SIZE, SQUARE_SIZE*4))
        self.background.fill('grey')
        super().__init__(x1, y1, priority, img_lib, '')
        self.x2 = x1 + SQUARE_SIZE
        self.y2 = y1 + SQUARE_SIZE * 4
        self._buttons = [
        PromotionButton(x1, y1, 5, img_lib,
                        get_piece_image_name(color, PieceType.QUEEN),
                        click_function, PieceType.QUEEN),
        PromotionButton(x1, y1 + SQUARE_SIZE, 5, img_lib,
                        get_piece_image_name(color, PieceType.ROOK),
                        click_function, PieceType.ROOK),
        PromotionButton(x1, y1 + SQUARE_SIZE * 2, 5, img_lib,
                        get_piece_image_name(color, PieceType.KNIGHT),
                        click_function, PieceType.KNIGHT),
        PromotionButton(x1, y1 + SQUARE_SIZE * 3, 5, img_lib,
                        get_piece_image_name(color, PieceType.BISHOP),
                        click_function, PieceType.BISHOP)]

        if not draw_down:
            self.order_queen_on_bottom()

    def rotate(self):
        self._draw_down = not self._draw_down
        half_chess_board = SQUARE_SIZE * 4
        if not self._draw_down:
            half_chess_board = half_chess_board * -1
        self.y1 += half_chess_board
        self.y2 += half_chess_board
        self.draw_y1 += half_chess_board
        
        if self._draw_down:
            self.order_queen_on_top()
        else:
            self.order_queen_on_bottom()

    def order_queen_on_bottom(self):
            i = len(self._buttons) - 1
            for button in self._buttons:
                button.y1 = self.y1 + SQUARE_SIZE * i
                button.y2 = button.y1 + SQUARE_SIZE     
                button.draw_y1 = button.y1
                i -= 1

    def order_queen_on_top(self):
            i = 0
            for button in self._buttons:
                button.y1 = self.y1 + SQUARE_SIZE * i
                button.y2 = button.y1 + SQUARE_SIZE     
                button.draw_y1 = button.y1
                i += 1

    def recieve_click(self, event: Event) -> bool:
        return False
    
    def recieve_mouse_motion(self, event: Event):
        return super().recieve_mouse_motion(event)
    
    def update(self):
        for button in self._buttons:
            button.update()
    
    def draw(self, surface: Surface):
        surface.blit(self.background, (self.draw_x1, self.draw_y1))
        for button in self._buttons:
            button.draw(surface)
    

class PromotionButton(Button):
    def __init__(self, x1, y1, priority, img_lib, piece_img, click_function, piece_type):
        super().__init__(x1, y1, priority, img_lib, piece_img, piece_img, click_function)
        self._piece_type = piece_type

    def click(self):
        self._click(piece_type=self._piece_type)
