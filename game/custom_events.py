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


CUSTOM_EVENTS_ATTRIBUTES = {
    CustomEvent.PLAYED_MOVE: ["color"],
    CustomEvent.TIMER_END: ["color"],
    CustomEvent.CHANGE_SCREEN: ["screen_name"],
    CustomEvent.UNDID_MOVE: [],
    CustomEvent.FINISHED_GAME: ["color"],
    CustomEvent.LOW_TIME: ["color"],
}


def post_event(event_type: CustomEvent, **kwargs):
    for attribute in CUSTOM_EVENTS_ATTRIBUTES[event_type]:
        if attribute not in kwargs.keys():
            raise ValueError()
    event = Event(event_type.value)
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
        self.observers: list[EventObserver] = []

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
