from pygame.event import Event
from game.custom_events import EventObserver
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION

LEFTMOUSEBUTTON = 1
RIGHTMOUSEBUTTON = 2


class Clickable:
    def __init__(self, x1, y1, x2, y2, priority):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.priority = priority
        self.left_buttop_down = False
        self.left_buttop_up = False
        self.right_buttop_down = False
        self.right_buttop_up = False

    def collides(self, x, y):
        return not (x <= self.x1 or x >= self.x2 or y <= self.y1 or y >= self.y2)

    def recieve_click(self, event: Event) -> bool:
        x, y = event.pos
        if self.collides(x, y):
            if event.type == MOUSEBUTTONUP and event.button == LEFTMOUSEBUTTON:
                self.left_buttop_up = True
            elif event.type == MOUSEBUTTONUP and event.button == RIGHTMOUSEBUTTON:
                self.right_buttop_up = True
            elif event.type == MOUSEBUTTONDOWN and event.button == LEFTMOUSEBUTTON:
                self.left_buttop_down = True
            elif event.type == MOUSEBUTTONDOWN and event.button == RIGHTMOUSEBUTTON:
                self.right_buttop_down = True

        return False

    def recieve_mouse_motion(self, event: Event):
        pass

    def clear(self):
        self.left_buttop_up = False
        self.right_buttop_up = False
        self.left_buttop_down = False
        self.right_buttop_down = False

    def move(self, x, y):
        width = self.x2 - self.x1
        height = self.y2 - self.y1
        self.x1 = x
        self.x2 = x + width
        self.y1 = y
        self.y2 = y + height

    def resize(self, width, height):
        self.x2 = self.x1 + width
        self.y2 = self.y1 + height

    def width(self):
        return self.x2 - self.x1

    def height(self):
        return self.y2 - self.y1


class Mouse(EventObserver):
    def __init__(self) -> None:
        self.button_observer: list[Clickable] = []
        self.motion_observer: list[Clickable] = []

    def receive_event(self, event):
        if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP:
            self.mouse_button(event)
        elif event.type == MOUSEMOTION:
            self.mouse_motion(event)

    def mouse_button(self, event):
        for clickable in self.button_observer:
            if clickable.recieve_click(event):
                break

    def mouse_motion(self, event):
        for clickable in self.motion_observer:
            clickable.recieve_mouse_motion(event)

    def register_button_observer(self, clickable: Clickable):
        self.button_observer.append(clickable)
        self.button_observer.sort(key=lambda c: c.priority, reverse=True)

    def unregister_button_observer(self, clickable: Clickable):
        try:
            self.button_observer.remove(clickable)
        except ValueError:
            pass

    def register_motion_observer(self, clickable: Clickable):
        self.motion_observer.append(clickable)

    def unregister_motion_observer(self, clickable: Clickable):
        try:
            self.motion_observer.remove(clickable)
        except ValueError:
            pass
