from pygame.event import Event
from custom_events import EventAnnouncer
from view import View, Button
from drawing import ImageLibrary
from mouse import Mouse

class Screen:
    def __init__(self, mouse:Mouse, image_library: ImageLibrary, event_announcer: EventAnnouncer):
        self.image_library = image_library 
        self.mouse = mouse
        self.event_announcer = event_announcer
        self.elements = []
        self.priority = 0     

    def add_element(self, element):
        self.elements.append(element)
        self.elements.sort(key=lambda e: e.priority, reverse=True)

    def remove_element(self, element):
        self.elements.remove(element)

    def update(self):
        for element in self.elements:
            element.update()

    def draw(self, surface):
        for element in reversed(self.elements):
            element.draw(surface)
