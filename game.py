import pygame
from custom_events import CustomEvent, post_event
from board_controller import BoardController
from mouse import Mouse
from chess.enums import Color
from drawing import ImageLibrary, IMAGES
from custom_events import EventAnnouncer
from screen.main_menu import MainMenu 
from screen.chess_screen import ChessScreen 
from screen.practice_chess_screen import PracticeChessScreen 
from screen.screen import Screen 

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
            elif event.type == CustomEvent.CHANGE_SCREEN.value:
                self.open_screen(event)
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

    def handle_click(self, click: pygame.event.Event):
        self.mouse.process_mouse_event(click)

    def open_screen(self, event: pygame.event.Event):
        screen_name = event.screen_name
        new_screen = None
        match(screen_name):
            case 'main_menu':
                new_screen = MainMenu(self.mouse, self.image_library, self.event_announcer)
            case 'chess_game':
                new_screen = ChessScreen(self.mouse, self.image_library, self.event_announcer, event.color)
            case 'practice_game':
                new_screen = PracticeChessScreen(self.mouse, self.image_library, self.event_announcer, event.color)

        if self.screen != None:
            self.screen.destroy()
            self.remove_object(self.screen)
        self.screen = new_screen
        self.add_object(new_screen)


class ChessGame(Game):
    def __init__(self, width: int, height: int, framerate: int = 30):
        super().__init__(width, height, framerate)
        self.board_x = 20
        self.board_y = 80
        self.color = Color.WHITE

    def run(self):
        post_event(CustomEvent.CHANGE_SCREEN, screen_name='main_menu')
        super().run()

    def _get_images(self):
        return IMAGES
  