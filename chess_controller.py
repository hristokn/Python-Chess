from mouse import Clickable, LEFTMOUSEBUTTON, RIGHTMOUSEBUTTON, MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION
from pygame.event import Event
from drawing import Drawable

class SquareController(Clickable, Drawable):
    def __init__(self, square, chess_game,
                x1, y1, x2, y2, priority,
                image):
        Clickable.__init__(self, x1, y1, x2, y2, priority)
        Drawable.__init__(self, x1,y1, image)
        self.square = square
        self.chess_game = chess_game

    def recieve_click(self, event: Event) -> bool:
        if event.button == LEFTMOUSEBUTTON:
            pass
        elif event.button == RIGHTMOUSEBUTTON:
            pass

    def recieve_mouse_motion(self, event: Event):
        pass

class PieceController(Clickable, Drawable):
    def __init__(self, piece, chess_game,
                x1, y1, x2, y2, priority,
                image):
        Clickable.__init__(self, x1, y1, x2, y2, priority)
        Drawable.__init__(self, x1, y1, image)
        self.piece = piece
        self.chess_game = chess_game

    def recieve_click(self, event: Event) -> bool:
        if event.type == MOUSEBUTTONUP and event.button == LEFTMOUSEBUTTON:
            return self.mouse_up_left()
        elif event.type == MOUSEBUTTONUP and event.button == RIGHTMOUSEBUTTON:
            return self.mouse_up_left()
        elif event.type == MOUSEBUTTONDOWN and event.button == LEFTMOUSEBUTTON:
            return self.mouse_up_left()
        elif event.type == MOUSEBUTTONDOWN and event.button == RIGHTMOUSEBUTTON:
            return self.mouse_up_left()
        else: 
            raise ValueError

    def mouse_down_left(self):
        held_piece = self.chess_game.get_held_piece()
        if held_piece == None:
            self.chess_game.set_held_piece(self.piece)
            #make it some the piece follows the mouse cursor
            return True
        return True
    def mouse_down_right(self):
        return False
    def mouse_up_left(self):
        held_piece = self.chess_game.get_held_piece()
        if held_piece == None:
            return False
        elif held_piece == self.piece:
            return True
        elif held_piece != None:
            #create a move with the square of the held piece and this piece and try to play it??
            return True
        return True
    def mouse_up_right(self):
        return False

    def recieve_mouse_motion(self, event: Event):
        pos = event.pos
        