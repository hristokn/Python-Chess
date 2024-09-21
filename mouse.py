from abc import ABC, abstractmethod
from pygame.event import Event
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION

LEFTMOUSEBUTTON = 1
RIGHTMOUSEBUTTON = 2

class Clickable(ABC):
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

    @abstractmethod
    def recieve_click(self, event: Event) -> bool:
        if event.type == MOUSEBUTTONUP and event.button == LEFTMOUSEBUTTON:
            self.left_buttop_up = True
        elif event.type == MOUSEBUTTONUP and event.button == RIGHTMOUSEBUTTON:
            self.right_buttop_up = True
        elif event.type == MOUSEBUTTONDOWN and event.button == LEFTMOUSEBUTTON:
            self.left_buttop_down = True
        elif event.type == MOUSEBUTTONDOWN and event.button == RIGHTMOUSEBUTTON:
            self.right_buttop_down = True
        return True

    @abstractmethod
    def recieve_mouse_motion(self, event: Event):
        pass

class Mouse:
    def __init__(self) -> None:
        self.button_observer : list[Clickable]  = []
        self.motion_observer : list[Clickable]  = []

    def process_mouse_event(self, event: Event):
        if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP:
            self.mouse_button(event)
        elif event.type == MOUSEMOTION:
            self.mouse_motion(event)
        else:
            raise ValueError

    def mouse_button(self, event):
        x = event.pos[0]
        y = event.pos[1]
        
        for clickable in self.button_observer:
            if clickable.collides(x, y):
                if clickable.recieve_click(event):
                    break

    def mouse_motion(self, event):
        for clickable in self.motion_observer:
            clickable.recieve_mouse_motion(event)

    def register_button_observer(self, clickable: Clickable):
        self.button_observer.append(clickable)
        self.button_observer.sort(key=lambda c: c.priority, reverse=True)

    def unregister_button_observer(self,clickable: Clickable):
        self.button_observer.remove(clickable)

    def register_motion_observer(self, clickable: Clickable):
        self.motion_observer.append(clickable)
    
    def unregister_motion_observer(self, clickable: Clickable):
        self.motion_observer.remove(clickable)