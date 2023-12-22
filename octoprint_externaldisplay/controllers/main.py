import logging
from octoprint.printer import PrinterInterface
from octoprint_externaldisplay.backlight import Backlight
from octoprint_externaldisplay.canvas import Canvas
from octoprint_externaldisplay.controllers.print import PrintController
from octoprint_externaldisplay.controllers.sleep import SleepController
from octoprint_externaldisplay.controllers.manager import Manager
from octoprint_externaldisplay import events


class MainController:
    def __init__(self, printer: PrinterInterface, canvas: Canvas, backlight: Backlight, logger: logging.Logger):
        self.printer = printer
        self.canvas = canvas
        self.backlight = backlight
        self.logger = logger

        self.manager = Manager()
        self.manager.register("print", PrintController(
            self.printer, self.canvas, self.manager, self.logger))
        self.manager.register("sleep", SleepController(
            self.printer, self.canvas, self.backlight, self.manager, self.logger))
        self.manager.navigate("print")

    def draw(self):
        self.manager.current.draw()

    def handle(self, event: events.Event):
        self.manager.current.handle(event)
