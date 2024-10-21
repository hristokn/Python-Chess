from pygame.event import custom_type, post, Event
from enum import Enum, auto

class AutoEvent(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return custom_type()

class CustomEvent(AutoEvent):
    PLAYED_MOVE = auto()

def post_event(event: CustomEvent, **kwargs):
    event = Event(event.value)
    for keyword, arg in kwargs.items():
        if not hasattr(event, keyword):
            setattr(event, keyword, arg)
        else:
            raise ValueError
    post(event)


class EventListener:
    def receive_event(self, event):
        pass