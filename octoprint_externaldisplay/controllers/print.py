import logging
from octoprint.printer import PrinterInterface
from octoprint_externaldisplay.canvas import Canvas
from octoprint_externaldisplay import events, controls, utils
from octoprint_externaldisplay.views import print
from octoprint_externaldisplay.views.controls import ControlsView
from octoprint_externaldisplay.controllers.manager import Manager


class PrintController:
    def __init__(self, printer: PrinterInterface, canvas: Canvas, manager: Manager, logger: logging.Logger):
        self.printer = printer
        self.manager = manager
        self.logger = logger

        action_bar_size = 16 * canvas.scale
        self.print_view = print.PrintView(canvas, (0, 0), (canvas.image.width - action_bar_size, canvas.image.height))
        self.controls_view = ControlsView(canvas, action_bar_size=action_bar_size)

    def draw(self):
        self.print_view.draw(self.get_view_data())
        self.controls_view.draw(self.get_actions())

    def handle(self, event: events.Event):
        if isinstance(event, events.ButtonPressEvent):
            self.handle_button_press(event)
        if isinstance(event, events.OctoPrintEvent):
            self.handle_octoprint_event(event)

    def handle_button_press(self, event: events.ButtonPressEvent):
        if event.button == controls.BUTTON_A:
            if self.printer.is_ready():
                self.printer.start_print()
            elif self.printer.is_printing():
                self.printer.cancel_print()
        if event.button == controls.BUTTON_B:
            if self.printer.is_paused():
                self.printer.resume_print()
            else:
                self.printer.pause_print()

    def handle_octoprint_event(self, event: events.OctoPrintEvent):
        if event.name == "PrinterStateChanged":
            self.handle_printer_state_changed(event.payload['state_id'])

    def handle_printer_state_changed(self, state: str):
        if state in utils.sleep_printer_states:
            self.manager.navigate("sleep")

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

    def get_actions(self):
        actions = []

        if self.printer.is_paused():
            actions += [ControlsView.Action(color=ControlsView.COLOR_DANGER, label="Restart")]
        elif self.printer.is_printing():
            actions += [ControlsView.Action(color=ControlsView.COLOR_DANGER, label="Cancel")]
        elif self.printer.is_ready():
            actions += [ControlsView.Action(color=ControlsView.COLOR_DEFAULT, label="Start")]
        else:
            actions += [ControlsView.Action(color=ControlsView.COLOR_DISABLED, label="Start")]

        if self.printer.is_paused():
            actions += [ControlsView.Action(color=ControlsView.COLOR_DEFAULT, label="Resume")]
        elif self.printer.is_printing():
            actions += [ControlsView.Action(color=ControlsView.COLOR_DEFAULT, label="Pause")]
        else:
            actions += [ControlsView.Action(color=ControlsView.COLOR_DISABLED, label="Pause")]

        actions += [ControlsView.Action(color=ControlsView.COLOR_DISABLED, label="Menu")]

        return actions

