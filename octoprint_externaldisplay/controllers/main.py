from octoprint.printer import PrinterInterface
from octoprint_externaldisplay.canvas import Canvas
from octoprint_externaldisplay.controllers.print import PrintController
from octoprint_externaldisplay.controllers.manager import Manager
from octoprint_externaldisplay import events


class MainController:
    def __init__(self, printer: PrinterInterface, canvas: Canvas):
        self.printer = printer
        self.canvas = canvas

        self.manager = Manager()
        self.manager.register("print", PrintController(self.printer, self.canvas, self.manager))
        self.manager.navigate("print")

    def draw(self):
        self.manager.current.draw()

    def handle(self, event: events.Event):
        self.manager.current.handle(event)
