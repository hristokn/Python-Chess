from pygame.event import custom_type, post, Event
from enum import Enum, auto

class AutoEvent(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return custom_type()

class CustomEvent(AutoEvent):
    PLAYED_MOVE = auto()
    TIMER_END = auto()
    CHANGE_SCREEN = auto()
    UNDID_MOVE = auto()
    FINISHED_GAME = auto()
    LOW_TIME = auto()

def post_event(event: CustomEvent, **kwargs):
    event = Event(event.value)
    for keyword, arg in kwargs.items():
        if not hasattr(event, keyword):
            setattr(event, keyword, arg)
        else:
            raise ValueError
    post(event)


class EventObserver:
    def receive_event(self, event):
        pass


class EventAnnouncer:
    def __init__(self) -> None:
        self.observers : list[EventObserver]  = []

    def announce_event(self, event: Event):
        for observer in self.observers:
            observer.receive_event(event)

    def register_observer(self, observer: EventObserver):
        self.observers.append(observer)

    def unregister_observer(self, observer: EventObserver):
        try:
            self.observers.remove(observer)
        except ValueError:
            pass

