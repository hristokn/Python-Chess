from view.view import View
from game.drawing import (
    ImageLibrary,
    get_piece_image_name,
    get_square_image,
    SQUARE_SIZE,
)
from pygame import Surface
from pygame.event import Event


class SquareController(View):
    def __init__(self, square, image_library: ImageLibrary, x1, y1, priority):
        super().__init__(x1, y1, priority, image_library, get_square_image(square))
        self.square = square
        self.move_image = "valid_move"
        self.selected_square_image = "selected_square"
        self.selected = False
        self.has_move = False

    def draw(self, surface: Surface):
        super().draw(surface)
        if self.selected:
            surface.blit(
                self.image_library[self.selected_square_image],
                (self.draw_x1, self.draw_y1),
            )
        if self.has_move:
            surface.blit(
                self.image_library[self.move_image], (self.draw_x1, self.draw_y1)
            )

    def recieve_click(self, event: Event) -> bool:
        super().recieve_click(event)
        x, y = event.pos
        if self.collides(x, y):
            return True
        return False

    def recieve_mouse_motion(self, event: Event):
        pass


class PieceController(View):
    def __init__(self, piece, image_library: ImageLibrary, x1, y1, priority):
        image = get_piece_image_name(piece.color, piece.type)
        super().__init__(x1, y1, priority, image_library, image)
        self.piece = piece
        self.take_image = "valid_take"
        self.is_held = False
        self.can_be_taken = False
        self._default_priority = priority
        self.hidden = False

    def recieve_click(self, event: Event) -> bool:
        if self.hidden:
            return False
        super().recieve_click(event)
        x, y = event.pos
        if self.collides(x, y):
            return True
        return False

    def recieve_mouse_motion(self, event: Event):
        if self.hidden:
            return
        x, y = event.pos
        if self.is_held:
            self.draw_x1 = x - SQUARE_SIZE / 2
            self.draw_y1 = y - SQUARE_SIZE / 2

    def draw(self, surface: Surface):
        if self.hidden:
            return
        super().draw(surface)
        if self.can_be_taken:
            surface.blit(
                self.image_library[self.take_image], (self.draw_x1, self.draw_y1)
            )

    def set_held_piece(self):
        self.is_held = True
        self.priority = self._default_priority + 1

    def clear_held_piece(self):
        self.is_held = False
        self.draw_x1 = self.x1
        self.draw_y1 = self.y1
        self.priority = self._default_priority

    def update_image(self):
        self.image = get_piece_image_name(self.piece.color, self.piece.type)

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False
