import pygame
from chess_controller import *
from mouse import Mouse
from chess.chess import ChessBoard
from chess.enums import Color
from drawing import ImageLibrary, IMAGES

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
        self.image_library = ImageLibrary(self._get_images())

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
        self.selected_piece = None
        self.held_piece = None

    def run(self):
        game = ChessBoard(Color.WHITE)
        game.start()
        self.board_controller = BoardController(game, self.image_library, self.color, self.board_x, self.board_y)
        self.board_controller.setup(self.mouse)
        self.add_object(self.board_controller)
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
        for obj in self.objects:
            obj.update()

    def _get_images(self):
        return IMAGES



'''
def a piece is held if it follows the mouse

if a piece is pressed, we could do a few things
    if we have no selected piece, select it, tell it that it is held
    if the pressed piece is the selected piece, do nothing?
    if we have a selected piece, create the move and try it, also unselect the selected piece

if a piece is uppressed, we could do a few things
    if we have no selected piece, do nothing
    if we have a selected piece, and its the same one, let it go
    if we have a selected and held piece, and its a different piece, make move

if a square is pressed, we could do a few things
    if we have a selected piece, make move
    if we have no selected piece, nothing

if a square is uppressed, we do:
    if we have no selected piece, nothing
    if we have a seleced piece, but it's NOT held, unselect it
    if we have a seleced piece, but it's held, try the move, unheld it, do not unselect it,  

we have introduced one piece of state in the game, selected piece ()
we have introduced one piece of state in the game, held piece    

'''


        