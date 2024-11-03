from screen import Screen
from view import View
from view import Button
from pygame.display import get_surface
from custom_events import EventAnnouncer
import pygame

class MainMenu(Screen):
    def __init__(self, mouse, image_library, button_func: list, event_announcer: EventAnnouncer):
        super().__init__(mouse, image_library, event_announcer)
        background_surface = pygame.Surface(get_surface().get_size())
        background_surface.fill('gray')
        background = View(0,0,-10,self.image_library,background_surface)
        self.add_element(background)


        button_up = pygame.Surface((300,50))
        button_up.fill('blue')
        button_down = pygame.Surface((300,50))
        button_down.fill('green')

        button = Button(500,300,1,self.image_library, button_up, button_down, button_func[0])
        self.add_element(button)
        self.mouse.register_button_observer(button)
        