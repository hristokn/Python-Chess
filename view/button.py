from view.view import View
from view.text import Text
from pygame import Surface
from pygame.event import Event


class Button(View):
    def __init__(
        self, x1, y1, priority, img_lib, button_img, pressed_button_img, click_function
    ):
        View.__init__(self, x1, y1, priority, img_lib, button_img)
        self._unpressed_button_img = button_img
        self._pressed_button_img = pressed_button_img
        self._is_held = False
        self._click_function = click_function

    def recieve_click(self, event: Event) -> bool:
        super().recieve_click(event)
        x, y = event.pos

        if self.collides(x, y):
            if self.left_buttop_down:
                self.hold_button()
            if self.left_buttop_up and self._is_held:
                self.release_button()
                self.click()
            self.clear()
            return True
        else:
            self.clear()
            self.release_button()
            return False

    def hold_button(self):
        self._is_held = True

    def release_button(self):
        self._is_held = False

    def _click(self, **kwargs):
        self._click_function(**kwargs)

    def click(self):
        self._click()

    def draw(self, surface: Surface):
        if not self._is_held:
            self.image = self._unpressed_button_img
        else:
            self.image = self._pressed_button_img
        super().draw(surface)

    def update(self):
        pass

    def recieve_mouse_motion(self, event: Event):
        return super().recieve_mouse_motion(event)


class TextButton(Button):
    def __init__(
        self,
        x1,
        y1,
        priority,
        img_lib,
        text,
        click_function,
        button_img="text_button",
        pressed_button_img="text_button_pressed",
    ):
        super().__init__(
            x1, y1, priority, img_lib, button_img, pressed_button_img, click_function
        )
        self.text: Text = Text(
            self.x1, self.y1, self.x2, self.y2, priority, self.image_library, text
        )

    def draw(self, surface: Surface):
        super().draw(surface)
        self.text.draw(surface)


class SmallTextButton(TextButton):
    def __init__(self, x1, y1, priority, img_lib, text, click_function):
        super().__init__(
            x1,
            y1,
            priority,
            img_lib,
            text,
            click_function,
            "text_button_small",
            "text_button_pressed_small",
        )


class SwitchButton(Button):
    def __init__(
        self, x1, y1, priority, img_lib, button_images: list[str], button_values: list
    ):
        super().__init__(
            x1,
            y1,
            priority,
            img_lib,
            button_images[0],
            button_images[0],
            self.next_value,
        )
        self.button_images = button_images
        self.button_values = button_values
        self.value_count = len(self.button_values)
        self.index = 0
        self.image = self.button_images[self.index]

    def next_value(self):
        self.index = (self.index + 1) % self.value_count
        self._pressed_button_img = self.button_images[self.index]
        self._unpressed_button_img = self.button_images[self.index]

    def draw(self, surface: Surface):
        super().draw(surface)

    def get_value(self):
        return self.button_values[self.index]
