import pygame
from chess_controller import *
from mouse import Mouse
from chess.chess import ChessBoard
from chess.enums import Color
from drawing import ImageLibrary, IMAGES
from view import Button
from custom_events import CustomEvent
from taken_pieces_display import TakenPiecesDisplay

class Game:
    def __init__(self, width: int, height: int, framerate: int = 30):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.timestep = 1000 / framerate
        self.running = False
        self.objects = []
        self.mouse = Mouse()
        self.image_library = ImageLibrary(self._get_images())


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
            else:
                for event_listener in self.objects:
                    try:
                        event_listener.receive_event(event)
                    except AttributeError:
                        pass

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


class ChessGame(Game):
    def __init__(self, width: int, height: int, framerate: int = 30):
        super().__init__(width, height, framerate)
        self.board_x = 100
        self.board_y = 100
        self.color = Color.WHITE

    def run(self):
        game = ChessBoard(Color.WHITE)
        game.start()
        self.board_controller = BoardController(game, self.image_library, self.color, self.board_x, self.board_y)
        self.board_controller.setup(self.mouse)
        self.add_object(self.board_controller)
        button = Button(0, 0, 1, self.image_library, 'button_rotate', 'button_rotate_pressed')
        self.add_object(button)
        self.mouse.register_button_observer(button)
        taken_white_pieces_display = TakenPiecesDisplay(30, 30, 1, self.image_library, '', game, Color.WHITE)
        self.add_object(taken_white_pieces_display)
        super().run()


    def _get_images(self):
        return IMAGES
  