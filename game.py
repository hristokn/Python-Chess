import pygame
from operator import attrgetter
from game_objects import GameObject
from pygame_extra import loadImage
from chess_board import ChessBoard


class Game:
    def __init__(self, width: int, height: int, framerate: int = 30):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.timestep = 1000 / framerate
        self.running = False
        self.image_library = {}
        self.custom_events = {}
        self.objects = []

        self._load_images()
        self._add_custom_events()

    def run(self):

        self.running = True

        board = ChessBoard(
            (100, 100),
            (512, 512),
            self.image_library["board"],
            (100, 100),
            self.image_library,
            self.custom_events,
        )
        self.objects.append(board)
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
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                or event.type == pygame.MOUSEBUTTONUP
            ):
                self.handle_click(event)
            if event.type == self.custom_events["object_created"]:
                self.add_object(event.object)
            if event.type == self.custom_events["object_removed"]:
                self.remove_object(event.object)

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

    def add_object(self, obj: GameObject):
        self.objects.append(obj)
        self.objects.sort(key=attrgetter("depth"))  # lazy solution

    def remove_object(self, obj: GameObject):
        self.objects.remove(obj)

    def handle_click(self, click: pygame.event):
        for obj in reversed(self.objects):
            try:
                if obj.clicked(click.pos):
                    obj.handle_click(click)
                    return
            except AttributeError:
                pass

    def _load_images(self):
        self.image_library["board"] = loadImage("images/chess_board_1_white_side.png")
        self.image_library["black_pawn"] = loadImage("images/black_pawn.png")
        self.image_library["black_rook"] = loadImage("images/black_rook.png")
        self.image_library["black_knight"] = loadImage("images/black_knight.png")
        self.image_library["black_bishop"] = loadImage("images/black_bishop.png")
        self.image_library["black_king"] = loadImage("images/black_king.png")
        self.image_library["black_queen"] = loadImage("images/black_queen.png")
        self.image_library["white_pawn"] = loadImage("images/white_pawn.png")
        self.image_library["white_rook"] = loadImage("images/white_rook.png")
        self.image_library["white_knight"] = loadImage("images/white_knight.png")
        self.image_library["white_bishop"] = loadImage("images/white_bishop.png")
        self.image_library["white_king"] = loadImage("images/white_king.png")
        self.image_library["white_queen"] = loadImage("images/white_queen.png")
        self.image_library["valid_move"] = loadImage("images/valid_move.png")
        self.image_library["valid_take"] = loadImage("images/take.png")

    def _add_custom_events(self):
        self.custom_events["object_created"] = pygame.event.custom_type()
        self.custom_events["object_removed"] = pygame.event.custom_type()


class ChessGame(Game):
    def __init__():
        """
        Set up Game
        Add the pieces to the chess board in an initialize method
        both the game engine and the chess board should have the pieces maybe???
        or the pieces have access to the board and tell it what happens



        Piece has access to board
        Piece is in objects
        Board is in objects
        Board stores location of all pieces

        Click is detected. it clicks on the board and a pawn
        board ignores it
        if click is to select pawn, it asks the board for info to decide moves
        then it tells the board to











        mouse down on piece = piece is activeted and should show moves
        mouse up on a piece while activated = leave it in place and activated or move it and deactivate
        """
