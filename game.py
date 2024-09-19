import pygame
from chess_controller import *
from mouse import Mouse
from chess.chess import ChessBoard
from chess.enums import Color
from drawing import get_square_pos, get_square_color, SQUARE_SIZE, ImageLibrary, IMAGES, get_piece_image_name

class Game:
    def __init__(self, width: int, height: int, framerate: int = 30):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.timestep = 1000 / framerate
        self.running = False
        self.custom_events = {}
        self.objects = []
        self.mouse = Mouse()

        self._add_custom_events()

    def run(self):
        self.running = True
        self._run()

    def _run(self):
        while self.running:
            self.update()
            self.draw()
            self.clock.tick(self.timestep)
        self.quit()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif (
            event.type == pygame.MOUSEBUTTONDOWN 
            or event.type == pygame.MOUSEBUTTONUP
            or event.type == pygame.MOUSEMOTION):
                self.handle_click(event)

        pygame.event.pump()
        for obj in self.objects:
             obj.update()

    def draw(self):
        self.screen.fill("purple")

        for obj in self.objects:
            try:
                obj.draw(self.screen)
            except AttributeError:
                pass
        pygame.display.flip()

    def quit(self):
        pygame.quit()

    def add_object(self, obj):
        self.objects.append(obj)
        self.objects.sort(key=lambda obj: obj.priority)

    def remove_object(self, obj):
        self.objects.remove(obj)

    def handle_click(self, click: pygame.event):
        self.mouse.process_mouse_event(click)

    def _add_custom_events(self):
        self.custom_events["object_created"] = pygame.event.custom_type()
        self.custom_events["object_removed"] = pygame.event.custom_type()


class ChessGame(Game):
    def __init__(self, width: int, height: int, framerate: int = 30):
        super().__init__(width, height, framerate)
        self.board_x = 100
        self.board_y = 100
        self.color = Color.WHITE
        self.image_library = ImageLibrary(self._get_images())

    def run(self):
        self.chess = ChessBoard()
        for square, piece in self.chess.board.items():
            sq_img = self.image_library.get('white_square')
            if get_square_color(square):
                sq_img = self.image_library.get('black_square')
            pos = get_square_pos(self.board_x, self.board_y, square, self.color)
            sc = SquareController(square, self, pos[0], pos[1], pos[0] + SQUARE_SIZE, pos[1] + SQUARE_SIZE, 1, sq_img)
            self.add_object(sc)
            self.mouse.register_button_observer(sc)
            if piece != None:
                pc = PieceController(piece, self, pos[0], pos[1], pos[0] + SQUARE_SIZE, pos[1] + SQUARE_SIZE, 2 , self.image_library.get(get_piece_image_name(piece.color, piece.type)))
                self.add_object(pc)
                self.mouse.register_button_observer(pc)
        self.chess.start()
        super().run()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif (
            event.type == pygame.MOUSEBUTTONDOWN 
            or event.type == pygame.MOUSEBUTTONUP
            or event.type == pygame.MOUSEMOTION):
                self.handle_click(event)

        pygame.event.pump()
        # for obj in self.objects:
        #      obj.update()

    def _get_images(self):
        return IMAGES
