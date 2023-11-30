from octoprint.printer import PrinterInterface
from octoprint_externaldisplay.canvas import Canvas
from octoprint_externaldisplay.views import print


class PrintController:
    def __init__(self, printer: PrinterInterface, canvas: Canvas):
        self.printer = printer
        self.view = print.PrintView(canvas)

    def draw(self):
        self.view.draw(self.get_view_data())

    def get_view_data(self):
        temperatures = self.printer.get_current_temperatures()
        current_data = self.printer.get_current_data()

        bed_temp, extruder_temp = None, None

        if "bed" in temperatures:
            bed_temp = print.Temperature(
                current=temperatures["bed"]["actual"],
                target=temperatures["bed"]["target"]
            )
        if "tool0" in temperatures:
            extruder_temp = print.Temperature(
                current=temperatures["tool0"]["actual"],
                target=temperatures["tool0"]["target"]
            )

        return print.PrintViewData(
            bed=bed_temp,
            extruder=extruder_temp,
            progress=current_data["progress"]["completion"],
            time_elapsed=current_data["progress"]["printTime"],
            time_remaining=current_data["progress"]["printTimeLeft"],
        )
