from pygame.event import Event
from game.custom_events import EventAnnouncer
from view.component import Component
from view.button import Button
from game.drawing import ImageLibrary
from game.mouse import Mouse

# class abstract
# class Node:
#     contains the observers and leaves
# class Leaf:
#     doesn't hold observers,

class Screen(Component):
    def __init__(self, mouse: Mouse, image_library: ImageLibrary, event_announcer: EventAnnouncer,
                 x1, y1, img):
        super().__init__(x1, y1, image_library, img)
        self.image_library = image_library 
        self.mouse = mouse
        self.event_announcer = event_announcer
        self.elements: list[Component] = []
        self.priority = 0     

    def add_element(self, element):
        self.elements.append(element)
        self.elements.sort(key=lambda e: e.priority, reverse=True)

    def remove_element(self, element):
        self.elements.remove(element)
        self.destroy_element(element)
        if isinstance(element, Screen):
            element.destroy_elements()

    def update(self):
        for element in self.elements:
            element.update()

    def draw(self, surface):
        for element in reversed(self.elements):
            element.draw(surface)

    def destroy_element(self, element: Component):
        self.mouse.unregister_button_observer(element)
        self.mouse.unregister_motion_observer(element)
        self.event_announcer.unregister_observer(element)
        element.destroy()

    def destroy_elements(self):
        for element in self.elements:
            self.destroy_element(element)

    def destroy(self):
        self.destroy_elements()
        super().destroy()