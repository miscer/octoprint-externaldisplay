from octoprint.printer import PrinterInterface
from octoprint_externaldisplay.canvas import Canvas
from octoprint_externaldisplay.controllers.print import PrintController
from octoprint_externaldisplay import events


class MainController:
    def __init__(self, printer: PrinterInterface, canvas: Canvas):
        self.printer = printer
        self.canvas = canvas

        self.print_controller = PrintController(self.printer, self.canvas)
        self.current = self.print_controller

    def draw(self):
        self.current.draw()

    def handle(self, event: events.Event):
        self.current.handle(event)
