from view.view import View
from pygame import Surface
from pygame.event import Event
from chess.chess import ChessBoard
from chess.enums import PieceType, Color
from drawing import get_piece_image_name_tiny
from custom_events import EventObserver, CustomEvent

class TakenPiecesDisplay(View, EventObserver):
    def __init__(self, x1, y1, priority, img_lib, img, game, color):
        View.__init__(self, x1, y1, priority, img_lib, img)
        self._game: ChessBoard = game
        self._color: Color = color
        self._display: dict[PieceType, int] = {}
        self._margin = 30

    
    def draw(self, surface: Surface):
        offset = 0
        for type, count in self._display:
            for i in range(count):
                offset += self._margin
                surface.blit(self.image_library[get_piece_image_name_tiny(self._color, type)], (self.draw_x1 + offset, self.draw_y1))


    def update(self):
        pass


    def recieve_mouse_motion(self, event: Event):
        return super().recieve_mouse_motion(event)
    

    def recieve_click(self, event: Event) -> bool:
        return False
    

    def update_display(self):
        display = {}
        for piece in self._game.taken_pieces:
            if piece.color == self._color:
                try:
                    display[piece.type] += 1
                except KeyError:
                    display[piece.type] = 1
        
        self._display = sorted(display.items(), key = lambda i: i[0].value)


    def receive_event(self, event):
        if event.type == CustomEvent.PLAYED_MOVE.value or event.type == CustomEvent.UNDID_MOVE.value:
            self.update_display()