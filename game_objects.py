import pygame.surface
import pygame.event
from tuple_n import TupleN


class GameObject:
    def __init__(self, depth: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.depth = depth

    def update(self):
        """Update"""


class Drawable:
    def __init__(
        self, pos: TupleN[int, int], image: pygame.surface.Surface = None, **kwargs
    ):
        super().__init__(**kwargs)
        self.image = image
        self.move_drawable(pos)

    def draw(self, surface: pygame.Surface):
        if self.image != None:
            surface.blit(self.image, self.pos)

    def move_drawable(self, pos: TupleN[int, int]):
        self.pos = pos


class Collider:

    def __init__(
        self, coords: TupleN[int, int], dimensions: TupleN[int, int], **kwargs
    ):
        super().__init__(**kwargs)
        self.move_collider(coords, dimensions)

    def move_collider(
        self, coords: TupleN[int, int], dimensions: TupleN[int, int] = None
    ):
        self.coords = coords
        self.dimensions = dimensions if dimensions != None else self.dimensions

    def clicked(self, coords: TupleN[int, int]):
        x = coords[0]
        y = coords[1]
        self_x = self.coords[0]
        self_y = self.coords[1]
        self_width = self.dimensions[0]
        self_height = self.dimensions[1]
        if (
            x <= self_x
            or (x >= self_x + self_width)
            or y <= self_y
            or y >= (self_y + self_height)
        ):
            return False
        return True

    def handle_click(self, click: pygame.event.Event):
        if click.type == pygame.MOUSEBUTTONDOWN and click.button == 1:
            self.handle_left_button_down()
        if click.type == pygame.MOUSEBUTTONUP and click.button == 1:
            self.handle_left_button_up()
        if click.type == pygame.MOUSEBUTTONUP and click.button == 2:
            self.handle_right_button_up()
        if click.type == pygame.MOUSEBUTTONDOWN and click.button == 2:
            self.handle_right_button_down()
        raise ValueError

    def handle_left_button_down(self):
        pass

    def handle_left_button_up(self):
        pass

    def handle_right_button_up(self):
        pass

    def handle_right_button_down(self):
        pass


class ChessBoardObjectCollider(Collider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clicks = []

    def handle_click(self, click: pygame.event.Event):
        self.clicks.append(click)

    def peek_click(self) -> None | pygame.event.Event:
        try:
            return self.clicks[0]
        except IndexError:
            return None

    def pop_click(self) -> None | pygame.event.Event:
        try:
            return self.clicks.pop(0)
        except IndexError:
            return None


class ChessBoardObject(ChessBoardObjectCollider, GameObject, Drawable):
    def __init__(self, square: TupleN[int, int], **kwargs):
        super().__init__(**kwargs)
        self.selected = False
        self.square: TupleN[int, int] = square

    def is_empty(self):
        return True

    def move(self, square: TupleN[int, int], screen_coords: TupleN[int, int]):
        self.square = square
        self.move_collider(screen_coords)
        self.move_drawable(screen_coords)
