from pygame.event import custom_type, post, Event
from enum import Enum, auto

class AutoEvent(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return custom_type()

class CustomEvent(AutoEvent):
    PLAYED_MOVE = auto()

def post_event(event: CustomEvent):
    post(Event(event.value))


class EventListener:
    def receive_event(self, event):
        pass