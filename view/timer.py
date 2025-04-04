from pygame import Surface
from pygame.font import SysFont, get_default_font
from pygame.event import Event
from view.view import View
from time import time_ns
from game.custom_events import CustomEvent, post_event


class TimerBox(View):
    def __init__(self, x1, y1, priority, img_lib, img, seconds, color):
        View.__init__(self, x1, y1, priority, img_lib, img)
        self._timer = Timer(seconds)
        self._color = color
        self._font = SysFont(get_default_font(), 40)
        self._started = False
        self.low_time_warning_played = False

    def draw(self, surface: Surface):
        box = Surface((80, 200))
        box.fill("black")
        font_img = self._font.render(self.remaining_time_formated(), 0, "white")
        surface.blit(font_img, (self.draw_x1, self.draw_y1))

    def update(self):
        self._timer.update()
        if (
            self._timer.remaining() <= self._timer.LOW_TIME_THRESHOLD_NS
            and not self.low_time_warning_played
        ):
            self.low_time_warning_played = True
            post_event(CustomEvent.LOW_TIME, color=self._color)
        if self._timer.remaining() <= 0:
            self.finish_timer()

    def finish_timer(self):
        if self._timer.running():
            post_event(CustomEvent.TIMER_END, color=self._color)
        self._timer.pause_timer()

    def recieve_click(self, event: Event) -> bool:
        return False

    def receive_event(self, event):
        if event.type == CustomEvent.FINISHED_GAME.value:
            self._timer.pause_timer()
        elif event.type == CustomEvent.PLAYED_MOVE.value:
            if not self._started:
                if self._color != event.color:
                    self._timer.start_timer()
                    self._started = True
                return

            if self._timer.running() and event.color == self._color:
                self._timer.pause_timer()
            if not self._timer.running() and event.color.next() == self._color:
                self._timer.start_timer()

    def remaining_time_formated(self):
        seconds = self._timer.remaining_seconds()
        minutes = int(seconds / 60)
        seconds %= 60
        return "{0:02d}:{1:02d}".format(minutes, seconds)


class Timer:
    LOW_TIME_THRESHOLD_NS = 10 * 1_000_000_000

    def __init__(self, seconds):
        self._nanoseconds = seconds * 1_000_000_000
        self._remaining = seconds * 1_000_000_000
        self._start = 0
        self._elapsed = 0
        self._elapsed_total = 0
        self._running = False

    def start_timer(self):
        self._start = time_ns()
        self._running = True

    def pause_timer(self):
        self._elapsed_total += self._elapsed
        self._running = False

    def update(self):
        if not self._running:
            return
        self._elapsed = self._start - time_ns()
        self._remaining = self._nanoseconds + self._elapsed + self._elapsed_total

    def remaining(self):
        return self._remaining

    def remaining_seconds(self):
        return int(round(self._remaining / 1_000_000_000, 0))

    def running(self):
        return self._running
