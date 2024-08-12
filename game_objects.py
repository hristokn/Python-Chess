import pygame


class GameObject:
    def __init__(self, depth: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.depth = depth

    def update(self):
        """Update"""


class Drawable:
    def __init__(self, pos: tuple[int, int], image: pygame.surface = None, **kwargs):
        super().__init__(**kwargs)
        self.image = image
        self.move_drawable(pos)

    def draw(self, surface: pygame.surface):
        if self.image != None:
            surface.blit(self.image, self.pos)

    def move_drawable(self, pos: tuple[int, int]):
        self.pos = pos


class Collider:

    def __init__(self, coords: tuple[int, int], dimensions: tuple[int, int], **kwargs):
        super().__init__(**kwargs)
        self.move_collider(coords, dimensions)

    def move_collider(self, coords: tuple[int, int], dimensions: tuple[int, int]):
        self.coords = coords
        self.dimensions = dimensions

    def clicked(self, coords: tuple[int, int]):
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

    def handle_click(self, click: pygame.event):
        if click.type == pygame.MOUSEBUTTONDOWN and click.button == 1:
            self.handle_left_button_down()
        if click.type == pygame.MOUSEBUTTONUP and click.button == 1:
            self.handle_left_button_up()
        if click.type == pygame.MOUSEBUTTONUP and click.button == 2:
            self.handle_right_button_up()
        if click.type == pygame.MOUSEBUTTONDOWN and click.button == 2:
            self.handle_right_button_down()

    def handle_left_button_down(self):
        pass

    def handle_left_button_up(self):
        pass

    def handle_right_button_up(self):
        pass

    def handle_right_button_down(self):
        pass


class ChessBoardObject(Collider, GameObject, Drawable):
    def __init__(self, board, **kwargs):
        super().__init__(**kwargs)
        self.board = board
        self.selected = False

    def is_empty(self):
        return True
