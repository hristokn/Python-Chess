import pygame
from board_controller import BoardController
from mouse import Mouse
from chess.chess import ChessBoard
from chess.enums import Color
from drawing import ImageLibrary, IMAGES
from custom_events import EventAnnouncer
from main_menu import MainMenu 
from chess_screen import ChessScreen 
from screen import Screen 

class Game:
    def __init__(self, width: int, height: int, framerate: int = 30):
        pygame.init()
        self.display = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.timestep = 1000 / framerate
        self.running = False
        self.objects = []
        self.mouse = Mouse()
        self.image_library = ImageLibrary(self._get_images())
        self.screen: Screen = None
        self.event_announcer = EventAnnouncer()
        self.event_announcer.register_observer(self.mouse)

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
            else:
                self.event_announcer.announce_event(event)

        pygame.event.pump()
        for obj in self.objects:
             obj.update()

    def draw(self):
        self.display.fill("gray")

        for obj in self.objects:
            try:
                obj.draw(self.display)
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

    def open_screen(self, screen:Screen):
        if self.screen != None:
            self.remove_object(self.screen)
        self.screen = screen
        self.add_object(screen)


class ChessGame(Game):
    def __init__(self, width: int, height: int, framerate: int = 30):
        super().__init__(width, height, framerate)
        self.board_x = 20
        self.board_y = 80
        self.color = Color.WHITE

    def run(self):
        main_menu = MainMenu(self.mouse, self.image_library, [self.start_chess_game], self.event_announcer)

        self.open_screen(main_menu)
        super().run()

    def start_chess_game(self):
        self.open_screen(ChessScreen(self.mouse, self.image_library, self.event_announcer, self.color))

    def _get_images(self):
        return IMAGES
  