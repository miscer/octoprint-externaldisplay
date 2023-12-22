import logging
from octoprint.printer import PrinterInterface
from octoprint_externaldisplay.backlight import Backlight
from octoprint_externaldisplay.canvas import Canvas
from octoprint_externaldisplay import events, utils
from octoprint_externaldisplay.controllers.manager import Manager


class SleepController:
    def __init__(self, printer: PrinterInterface, canvas: Canvas, backlight: Backlight, manager: Manager,
                 logger: logging.Logger):
        self.printer = printer
        self.canvas = canvas
        self.backlight = backlight
        self.manager = manager
        self.logger = logger

    def draw(self):
        self.canvas.draw.rectangle(
            ((0, 0), (self.canvas.image.width, self.canvas.image.height)),
            fill="white")

    def handle(self, event: events.Event):
        if isinstance(event, events.OctoPrintEvent):
            self.handle_octoprint_event(event)

    def handle_octoprint_event(self, event: events.OctoPrintEvent):
        if event.name == "PrinterStateChanged":
            self.handle_printer_state_changed(event.payload['state_id'])

    def handle_printer_state_changed(self, state: str):
        if state not in utils.sleep_printer_states:
            self.manager.navigate("print")

    def enter(self):
        self.backlight.turn_off()

    def leave(self):
        self.backlight.turn_on()
