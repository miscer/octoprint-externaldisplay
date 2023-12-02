import logging

from gpiozero import Button
from octoprint_externaldisplay import events


class GPIOButtons:
    def __init__(self, keymap: dict[str, int], handle_event: callable, logger: logging.Logger):
        self.keymap = keymap
        self.handle_event = handle_event
        self.logger = logger

        self.buttons = []
        self.init_buttons()

    def init_buttons(self):
        for key, pin in self.keymap.items():
            button = Button(pin)
            button.when_pressed = lambda k=key: self.on_button_press(k)
            self.buttons.append(button)

    def on_button_press(self, key):
        self.handle_event(events.ButtonPressEvent(key))
